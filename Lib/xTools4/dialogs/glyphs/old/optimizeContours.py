from vanilla import ColorWell, Button, CheckBox, RadioGroup
from mojo import drawingTools as ctx
from mojo.UI import UpdateCurrentGlyphView, NumberEditText
from mojo.events import addObserver, removeObserver
from mojo.roboFont import RGlyph
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.optimize import equalizeCurves

KEY = 'com.xTools4.dialogs.glyphs.optimizeContours'
def optimizeContoursFactory(glyph, equalize=True, addExtremes=False, simplify=False, treshold=10):
    glyph = RGlyph(glyph).copy()
    glyph.clearComponents()
    equalizeCurves(glyph, roundPos=False)
    return glyph


class OptimizeContoursDialog(GlyphsDialogBase):

    title = 'optimize'
    key   = f'{GlyphsDialogBase.key}.optimize'
    settings = {
        # 'previewStrokeColor' : (1, 0.5, 0),
        # 'previewStrokeWidth' : 2,
        'previewPointRadius' : 4,
        'tresholdValue'      : 10,
    }

    def __init__(self):
        # self.height  = self.buttonHeight
        self.height = self.textHeight * 7
        self.height += self.padding * 4 - 3
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        # self.w.previewStrokeColor = ColorWell(
        #         (x, y, -p, self.buttonHeight),
        #         callback=self.updatePreviewCallback,
        #         color=rgb2nscolor(self.settings['previewStrokeColor']))
        self.w.balanceHandles = CheckBox(
                (x, y, -p, self.textHeight),
                "equalize",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.addExtremes = CheckBox(
                (x, y, -p, self.textHeight),
                "add extremes",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.simplify = CheckBox(
                (x, y, -p, self.textHeight),
                "simplify",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.tresholdValue = NumberEditText(
                (col, y, -p, self.textHeight),
                text=self.settings['tresholdValue'],
                # callback=self.gridSizeCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "apply",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        # self.setUpBaseWindowBehavior()
        # addObserver(self, "backgroundPreview", "drawBackground")
        # UpdateCurrentGlyphView()

        self.initGlyphsWindowBehaviour()
        registerRepresentationFactory(Glyph, "%s.preview" % self.key, optimizeContoursFactory)
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    # @property
    # def previewStrokeColor(self):
    #     return nscolor2rgb(self.w.previewStrokeColor.get())

    # @property
    # def previewStrokeWidth(self):
    #     return self.settings['previewStrokeWidth']

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        unregisterRepresentationFactory(Glyph, "%s.preview" % self.key)

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):
        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if not g:
            return

        if not g.bounds:
            return

        # make preview
        # previewGlyph = self.makeGlyph(g, preview=True)
        previewGlyph = g.getRepresentation("%s.preview" % self.key)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale):
        r = self.settings['previewPointRadius'] * previewScale

        ctx.save()
        ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)

        for contour in glyph.contours:
            for pt in contour.bPoints:
                x0, y0 = pt.anchor
                x1, y1 = pt.bcpIn
                x2, y2 = pt.bcpOut

                if not (x1 == 0 and y1 == 0):
                    x1, y1 = x0 + x1, y0 + y1

                    ctx.stroke(*self.previewStrokeColor)
                    ctx.line((x0, y0), (x1, y1))

                    ctx.fill(*self.previewStrokeColor)
                    ctx.stroke(None)
                    ctx.oval(x1 - r, y1 - r, r * 2, r * 2)

                if not (x2 == 0 and y2 == 0):
                    x2, y2 = x0 + x2, y0 + y2

                    ctx.stroke(*self.previewStrokeColor)
                    ctx.line((x0, y0), (x2, y2))

                    ctx.fill(*self.previewStrokeColor)
                    ctx.stroke(None)
                    ctx.oval(x2 - r, y2 - r, r * 2, r * 2)

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()
        equalizeCurves(glyph, roundPos=False)
        return glyph

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('equalizing glyphs:\n')
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName]
            g.prepareUndo('equalize curves')
            newGlyph = self.makeGlyph(g, preview=True)
            g.clear()
            g.appendGlyph(newGlyph)
            g.changed()
            g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

        UpdateCurrentGlyphView()

# -------
# testing
# -------

if __name__ == "__main__":

    OptimizeContoursDialog()
