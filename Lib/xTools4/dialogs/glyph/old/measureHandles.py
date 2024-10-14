import drawBot
from vanilla import CheckBox, ColorWell, Slider, TextBox, RadioGroup, HorizontalLine
from mojo import drawingTools as ctx
from mojo.roboFont import RGlyph
from mojo.UI import UpdateCurrentGlyphView
from mojo.events import addObserver, removeObserver
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.measureHandles import MeasureHandlesMaker, MeasureSegmentsMaker
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


### TODO: add min/max threshold values


def measureHandlesFactory(glyph):

    glyph = RGlyph(glyph).copy()
    glyph.clearComponents()

    M = MeasureHandlesMaker()
    M.build(glyph)

    return M.positions, M.lengths, M.angles


def measureSegmentsFactory(glyph):

    glyph = RGlyph(glyph).copy()
    glyph.clearComponents()

    M = MeasureSegmentsMaker()
    M.build(glyph)

    return M.positions, M.lengths, M.angles


class MeasureHandlesTool(GlyphsDialogBase):

    '''
    A drawing helper which shows measurements and angles of Bezier handles in the Glyph View.

    ::

        from hTools3.dialogs.glyph.measureHandles import MeasureHandlesTool
        MeasureHandlesTool()

    '''

    title = 'measure'
    key = '%s.measureHandles' % GlyphsDialogBase.key
    settings = {
        'captionFontSize'     : 11,
        'handlesCaptionDraw'  : True,
        'handlesColor'        : (1, 0, 0.5),
        'segmentsCaptionDraw' : True,
        'segmentsColor'       : (0, 0.5, 1),
    }
    ignoreZero = False

    def __init__(self):
        self.height  = self.textHeight * 7
        self.height += self.buttonHeight * 2
        self.height += self.padding * 8 -2
        self.w = self.window((self.width, self.height), self.title)

        x = p = self.padding
        y = p * 0.75

        self.w.captionMode = RadioGroup(
                (x, y, -p, self.textHeight * 2),
                ["length", "angle"],
                isVertical=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)
        self.w.captionMode.set(0)

        y += self.textHeight * 2 + p # * 0.75
        self.w.showHandles = CheckBox(
                (x, y, -p, self.textHeight),
                "handles",
                value=self.settings['handlesCaptionDraw'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.handlesColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['handlesColor']))

        y += self.buttonHeight + p # * 0.75
        self.w.showSegments = CheckBox(
                (x, y, -p, self.textHeight),
                "line segments",
                value=self.settings['segmentsCaptionDraw'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)
        y += self.textHeight + p # * 0.75

        self.w.segmentsColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['segmentsColor']))

        y += self.buttonHeight + p # * 0.75
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

        y += self.textHeight + p # * 0.75
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "show preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        # y += self.textHeight
        # self.w.selectionOnly = CheckBox(
        #         (x, y, -p, self.textHeight),
        #         "selection only",
        #         value=False,
        #         callback=self.updatePreviewCallback,
        #         sizeStyle=self.sizeStyle)

        # y += self.textHeight + p * 0.75
        # self.w.line1 = HorizontalLine((x, y, -p, 1))

        self.setUpBaseWindowBehavior()
        addObserver(self, "foregroundPreview", "draw")
        registerRepresentationFactory(Glyph, "%s.handles"  % self.key, measureHandlesFactory)
        registerRepresentationFactory(Glyph, "%s.segments" % self.key, measureSegmentsFactory)
        UpdateCurrentGlyphView()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def showHandles(self):
        return bool(self.w.showHandles.get())

    @property
    def showSegments(self):
        return bool(self.w.showSegments.get())

    @property
    def captionMode(self):
        return int(self.w.captionMode.get())

    # @property
    # def selectionOnly(self):
    #     return bool(self.w.selectionOnly.get())

    @property
    def handlesColor(self):
        r, g, b, a = nscolor2rgb(self.w.handlesColor.get())
        a = self.settings['strokeAlpha']
        return r, g, b, a

    @property
    def handlesCaptionColor(self):
        return nscolor2rgb(self.w.handlesColor.get())

    @property
    def segmentsCaptionColor(self):
        return nscolor2rgb(self.w.segmentsColor.get())

    @property
    def captionFontSize(self):
        return int(self.w.captionFontSize.get())

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "draw")
        unregisterRepresentationFactory(Glyph, "%s.handles" % self.key)
        unregisterRepresentationFactory(Glyph, "%s.segments" % self.key)

    # ---------
    # observers
    # ---------

    def foregroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if g is None:
            return

        # draw preview

        captionFontSize = self.captionFontSize * s
        ctx.save()
        ctx.fontSize(captionFontSize)

        if self.showHandles:
            measurements = g.getRepresentation("%s.handles" % self.key)
            if measurements:
                positions, lengths, angles = measurements
                captions = lengths if self.captionMode == 0 else angles
                ctx.fill(*self.handlesCaptionColor)
                for i, pos in enumerate(positions):
                    for j, (x, y) in enumerate(pos):
                        caption  = captions[i][j]
                        if self.ignoreZero and int(float(caption)) == 0:
                            continue
                        w, h = ctx.textSize(caption)
                        ctx.text(caption, (x - w * 0.5, y - h * 0.5))

        if self.showSegments:
            measurements = g.getRepresentation("%s.segments" % self.key)
            if measurements:
                positions, lengths, angles = measurements
                captions = lengths if self.captionMode == 0 else angles
                ctx.fill(*self.segmentsCaptionColor)
                for i, pos in enumerate(positions):
                    for j, (x, y) in enumerate(pos):
                        caption  = captions[i][j]
                        if self.ignoreZero and int(float(caption)) == 0:
                            continue
                        w, h = ctx.textSize(caption)
                        ctx.text(caption, (x - w * 0.5, y - h * 0.5))

        ctx.restore()


# -------
# testing
# -------

if __name__ == '__main__':

    MeasureHandlesTool()
