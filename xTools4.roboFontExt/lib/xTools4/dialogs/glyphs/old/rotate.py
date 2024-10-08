from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)

from vanilla import CheckBox, Button, TextBox
from mojo import drawingTools as ctx
from mojo.UI import getDefault
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.dialogs.misc.origin import OriginPoint
from hTools3.modules.glyphutils import getOriginPosition
from hTools3.dialogs.misc.numberEditText01 import NumberEditText_01


def rotateGlyphFactory():
    pass


class RotateGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to rotate selected glyphs in the current font.

    ::

        from hTools3.dialogs.glyphs.rotate import RotateGlyphsDialog
        RotateGlyphsDialog()

    '''

    title = "rotate"
    key = '%s.rotate' % GlyphsDialogBase.key
    settings = {
        'rotateValue' : 10,
    }

    def __init__(self):
        self.height  = self.width
        self.height += self.textHeight * 3
        self.height += self.padding * 3 + 2
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        self.w.origin = OriginPoint(
                (x, y, self.width, self.width),
                callback=self.updatePreviewCallback)
        self.w.origin.setPosition(None)

        y += self.w.origin.height - p
        self.w.angleLabel = TextBox(
                (x, y, col, self.textHeight),
                'angle',
                sizeStyle=self.sizeStyle)

        self.w.angleValue = NumberEditText_01(
                (x+col, y, -p, self.textHeight),
                text=self.settings['rotateValue'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                continuous=False)

        y += self.textHeight + p + 3
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
    def rotationAngle(self):
        return self.w.angleValue.get()

    @property
    def posName(self):
        return self.w.origin.selected

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
            self.drawPreview(g, previewGlyph, s)
        else:
            self.drawPreview(g, previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def getOriginPos(self, glyph):
        if self.posName:
            return getOriginPosition(glyph, self.posName)
        else:
            return 0, 0

    def drawPreview(self, srcGlyph, previewGlyph, previewScale, plain=False):
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

        ctx.drawGlyph(previewGlyph)

        if not plain:
            # draw origin
            r = self.previewOriginRadius * previewScale
            x, y = self.getOriginPos(srcGlyph)
            ctx.fill(None)
            ctx.line((x - r, y), (x + r, y))
            ctx.line((x, y - r), (x, y + r))
            ctx.oval(x - r, y - r, r * 2, r * 2)

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()

        # apply rotation
        originPos = self.getOriginPos(glyph)
        glyph.rotateBy(-self.rotationAngle, origin=originPos)

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
            print("rotating glyphs:\n")
            print(f"\tangle: {self.rotationAngle}")
            print(f"\torigin: {self.posName}")
            print(f"\tlayers: {', '.join(layerNames)}")
            print(f"\tglyphs: {', '.join(glyphNames)}")

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('rotate glyphs')
                self.makeGlyph(g)
                g.changed()
                g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    RotateGlyphsDialog()
