import math
from vanilla import CheckBox, Button, TextBox
from mojo import drawingTools as ctx
from mojo.UI import getDefault, NumberEditText
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase
from xTools4.dialogs.old.misc.numberEditText01 import NumberEditText_01


def skewGlyphFactory():
    pass


class SkewGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to skew selected glyphs in the current font.

    ::

        from hTools3.dialogs.glyphs.skew import SkewGlyphsDialog
        SkewGlyphsDialog()

    '''

    title = "skew"
    key   = f'{GlyphsDialogBase.key}.skew'
    settings = {
        'xOffset'   : True,
        'skewValue' : 7.0,
        'skewY'     : 0.0,
    }

    def __init__(self):
        # self.height  = self.spinnerHeight * 2
        self.height = self.textHeight * 5
        self.height += self.padding * 6
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        self.w.angleLabel = TextBox(
                (x, y, col, self.textHeight),
                'angle',
                sizeStyle=self.sizeStyle)

        self.w.angleValue = NumberEditText_01(
                (x+col, y, -p, self.textHeight),
                text=self.settings['skewValue'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                continuous=False)

        y += self.textHeight + p
        self.w.originLabel = TextBox(
                (x, y, col, self.textHeight),
                'origin',
                sizeStyle=self.sizeStyle)

        self.w.originValue = NumberEditText(
                (x+col, y, -p, self.textHeight),
                text=self.settings['skewY'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.setSlantAngle = CheckBox(
                (x, y, -p, self.textHeight),
                "set slant angle",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        # y += self.textHeight
        # self.w.setSlantOffset = CheckBox(
        #         (x, y, -p, self.textHeight),
        #         "set slant offset",
        #         value=True,
        #         callback=self.updatePreviewCallback,
        #         sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                'apply',
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def skewAngle(self):
        value = self.w.angleValue.get()
        return value, 0

    @property
    def originPos(self):
        value = self.w.originValue.get()
        return 0, value

    @property
    def setSlantAngle(self):
        value = self.w.setSlantAngle.get()
        return round(value, 2)

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
        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale, plain=False):

        ctx.save()

        # draw glyph
        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = getDefault("glyphViewDefaultWidth")
            h = getDefault("glyphViewDefaultHeight")
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        if not plain:
            # draw origin
            x, y = self.originPos
            r = self.previewOriginRadius * previewScale
            ctx.fill(None)
            ctx.line((x - r, y), (x + r, y))
            ctx.line((x, y - r), (x, y + r))
            ctx.oval(x - r, y - r, r * 2, r * 2)
            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)

            # draw margins
            x1 = 0
            x2 = glyph.width
            y1 = -10000
            y2 = 10000

            offsetX = math.tan(math.radians(self.skewAngle[0])) * self.originPos[1]
            x1 -= offsetX
            x2 -= offsetX

            ctx.save()
            ctx.skew(*self.skewAngle)
            ctx.line((x1, y1), (x1, y2))
            ctx.line((x2, y1), (x2, y2))
            ctx.restore()

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()

        # apply skew
        glyph.skewBy(self.skewAngle, origin=self.originPos)

        # done
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

        layerNames = self.getLayerNames()
        if not layerNames:
            layerNames = [font.defaultLayer.name]

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('skewing glyphs:\n')
            print(f'\tangle: {self.skewAngle[0]}, {self.skewAngle[1]}')
            print(f'\torigin: {self.originPos[0]}, {self.originPos[1]}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print(f'\tglyphs: {", ".join(glyphNames)}')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('skew')
                self.makeGlyph(g)
                g.changed()
                g.performUndo()

        # set slant angle
        if self.setSlantAngle:
            font.info.italicAngle = -self.skewAngle[0]

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    SkewGlyphsDialog()
