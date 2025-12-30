from vanilla import CheckBox, Button, TextBox
from mojo import drawingTools as ctx
from mojo.UI import NumberEditText
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


KEY = f'{GlyphsDialogBase.key}.move'


def moveGlyphFactory():
    pass


class MoveGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to move selected glyphs in the current font.

    ::

        from xTools4.dialogs.glyphs.old.move import MoveGlyphsDialog
        MoveGlyphsDialog()

    '''

    title = "move"
    key = KEY
    settings = {
        'moveValueX' : 70,
        'moveValueY' : 0,
    }

    def __init__(self):
        self.height = self.textHeight * 4
        self.height += self.padding * 5 # - 4
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        self.w.labelX = TextBox(
                (x, y, col, self.textHeight),
                'x delta',
                sizeStyle=self.sizeStyle)

        self.w.deltaX = NumberEditText(
                (x+col, y, -p, self.textHeight),
                text=self.settings['moveValueX'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.labelY = TextBox(
                (x, y, col, self.textHeight),
                'y delta',
                sizeStyle=self.sizeStyle)

        self.w.deltaY = NumberEditText(
                (x+col, y, -p, self.textHeight),
                text=self.settings['moveValueY'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                'apply',
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        y += self.textHeight + p #- 2
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
    def moveValues(self):
        dx = self.w.deltaX.get()
        dy = self.w.deltaY.get()
        return int(dx), int(dy)

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

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = h = 10000
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()

        # apply move
        glyph.moveBy(self.moveValues)

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
            print('moving glyphs:\n')
            print(f'\tdistance: {self.moveValues[0]}, {self.moveValues[1]}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print(f'\tglyphs: {", ".join(glyphNames)}')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('move glyphs')
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

    MoveGlyphsDialog()
