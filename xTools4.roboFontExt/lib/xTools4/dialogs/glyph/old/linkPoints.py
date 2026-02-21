from vanilla import *
from mojo import drawingTools as ctx
from mojo.roboFont import CurrentGlyph
from mojo.UI import UpdateCurrentGlyphView
from mojo.events import addObserver, removeObserver
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.linkPoints import *
from xTools4.modules.measureHandles import getVector
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


KEY = f'{GlyphsDialogBase.key}.old.linkPoints'


class LinkPointsTool(GlyphsDialogBase):

    '''
    A drawing helper which shows distance and angle of point links in the Glyph View.

    ::

        from hTools3.dialogs.glyph.linkPointsTool import LinkPointsTool
        LinkPointsTool()

    '''

    title = "links"
    key = KEY
    settings = {
        'captionFontSize' : 11,
        'linkStrokeWidth' : 3,
        'linkStrokeAlpha' : 0.2,
        'linkColor'       : (1.0, 0.0, 0.0),
    }

    def __init__(self):
        self.height  = self.textHeight * 9
        self.height += self.padding * 9
        self.height += self.buttonHeight - 6
        self.w = self.window((self.width, self.height), self.title)

        x = p = self.padding
        y = p * 0.75
        self.w.captionMode = RadioGroup(
                (x, y, -p, self.textHeight * 2),
                ["length", "angle"],
                isVertical=True,
                callback=self.toggleProjectionsCallback,
                sizeStyle=self.sizeStyle)
        self.w.captionMode.set(0)

        y += self.textHeight * 2 + p
        self.w.buttonSave = Button(
            (x, y, -p, self.textHeight),
            "link",
            callback=self.saveLinkCallback,
            sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.buttonClearSelectedLinks = Button(
            (x, y, -p, self.textHeight),
            "unlink",
            callback=self.deleteLinkCallback,
            sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.linkColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['linkColor']))

        y += self.buttonHeight + p * 0.75
        self.w.captionFontSizeLabel = TextBox(
                (x, y, -p, self.textHeight),
                "caption size",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        valueMin  = 9
        valueMax  = 18
        tickCount = valueMax - valueMin
        self.w.captionFontSize = Slider(
                (x, y, -p, self.textHeight),
                value=self.settings['captionFontSize'],
                minValue=valueMin,
                maxValue=valueMax,
                tickMarkCount=tickCount,
                stopOnTickMarks=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.projections = CheckBox(
            (x, y, -p, self.textHeight),
            "projections",
            sizeStyle=self.sizeStyle,
            callback=self.updatePreviewCallback,
            value=False)

        y += self.textHeight + p
        self.w.buttonClear = Button(
            (x, y, -p, self.textHeight),
            "clear all",
            callback=self.clearLinksCallback,
            sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
            (x, y, -p, self.textHeight),
            "show preview",
            sizeStyle=self.sizeStyle,
            callback=self.updatePreviewCallback,
            value=True)

        self.setUpBaseWindowBehavior()
        addObserver(self, "backgroundPreview", "drawBackground")
        UpdateCurrentGlyphView()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def linkColor(self):
        return nscolor2rgb(self.w.linkColor.get())

    @property
    def linkColorLine(self):
        return self.linkColor[:-1] + (self.linkStrokeAlpha,)

    @property
    def linkColorCaption(self):
        return self.linkColor

    @property
    def linkStrokeWidth(self):
        return self.settings['linkStrokeWidth']

    @property
    def linkStrokeAlpha(self):
        return self.settings['linkStrokeAlpha']

    @property
    def captionMode(self):
        return int(self.w.captionMode.get())

    @property
    def captionFontSize(self):
        return int(self.w.captionFontSize.get())

    @property
    def projectionsDraw(self):
        return int(self.w.projections.get())

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")

    def toggleProjectionsCallback(self, sender):
        self.w.projections.enable(not sender.get())
        UpdateCurrentGlyphView()

    def saveLinkCallback(self, sender):
        '''
        Create a link between two selected points, and save it in the glyph lib.

        '''
        g = CurrentGlyph()
        if not g:
            return
        linkPoints(g)
        UpdateCurrentGlyphView()

    def deleteLinkCallback(self, sender):
        '''
        Delete selected link.

        '''
        g = CurrentGlyph()
        if not g:
            return
        deleteSelectedLinks(g)
        UpdateCurrentGlyphView()

    def clearLinksCallback(self, sender):
        '''
        Delete all links in glyph.

        '''
        g = CurrentGlyph()
        if not g:
            return
        deleteAllLinks(g)
        UpdateCurrentGlyphView()

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if g is None:
            return

        # draw preview

        self.drawPreview(g, s)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale):

        links = getLinks(glyph)

        if not len(links):
            return

        captionFontSize = self.captionFontSize * previewScale

        def _drawLinkMeasurement(p1, p2):
            distance, angle = getVector((p1[0], p1[1]), (p2[0], p2[1]))
            value = angle if self.captionMode else distance
            if type(value) is int:
                txt = str(value)
            else:
                txt = '%.2f' % value if not value.is_integer() else str(int(value))
            if self.captionMode:
                txt += '°'
            w, h = ctx.textSize(txt)
            x = p1[0] + (p2[0] - p1[0]) * 0.5
            y = p1[1] + (p2[1] - p1[1]) * 0.5
            x -= w * 0.5
            y -= h * 0.4
            ctx.textBox(txt, (x, y, w, h), align='center')

        for ID1, ID2 in links:
            pt1 = getPoint(glyph, ID1)
            pt2 = getPoint(glyph, ID2)

            ctx.save()

            # draw link
            ctx.fill(None)
            ctx.stroke(*self.linkColorLine)
            ctx.strokeWidth(self.linkStrokeWidth * previewScale)
            if self.captionMode == 0 and self.projectionsDraw:
                ctx.line((pt1.x, pt1.y), (pt2.x, pt1.y))
                ctx.line((pt2.x, pt1.y), (pt2.x, pt2.y))
            else:
                ctx.line((pt1.x, pt1.y), (pt2.x, pt2.y))

            # draw measurements
            ctx.stroke(None)
            ctx.fill(*self.linkColorCaption)
            ctx.fontSize(captionFontSize)
            if self.captionMode == 0 and self.projectionsDraw:
                _drawLinkMeasurement((pt1.x, pt1.y), (pt2.x, pt1.y))
                _drawLinkMeasurement((pt2.x, pt1.y), (pt2.x, pt2.y))
            else:
                _drawLinkMeasurement((pt1.x, pt1.y), (pt2.x, pt2.y))

            ctx.restore()


# -------
# testing
# -------

if __name__ == '__main__':

    LinkPointsTool()
