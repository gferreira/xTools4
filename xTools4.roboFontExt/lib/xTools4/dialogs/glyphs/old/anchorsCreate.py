from vanilla import TextBox, EditText, Button, RadioGroup, CheckBox, PopUpButton
from mojo import drawingTools as ctx
from mojo.UI import NumberEditText
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


class CreateAnchorsDialog(GlyphsDialogBase):

    '''
    A dialog to create anchors in the selected glyphs.

    ::

        from xTools4.dialogs.glyphs.old.anchorsCreate import CreateAnchorsDialog
        CreateAnchorsDialog()

    '''

    title = "anchors"
    key   = f'{GlyphsDialogBase.key}.anchorsCreate'
    settings = {
        # 'relativeToXHeight' : True,
        'posY' : 100,
        'posX' : 1,     # 0:left, 1:center, 2:right
    }

    def __init__(self):
        # self.height  = self.spinnerHeight
        self.height  = self.textHeight * 10
        self.height += self.padding * 6 - 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        y -= 2
        self.w.anchorNameLabel = TextBox(
                (x, y, -p, self.textHeight),
                'name',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.anchorName = EditText(
                (x, y, -p, self.textHeight),
                'top',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.labelY = TextBox(
                (x, y, col, self.textHeight),
                'y pos',
                sizeStyle=self.sizeStyle)
        self.w.posY = NumberEditText(
                (col, y, -p, self.textHeight),
                text=self.settings['posY'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.referenceMetrics = PopUpButton(
                (x, y, -self.padding, self.textHeight),
                ['baseline', 'xheight', 'capheight'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)
        self.w.referenceMetrics.set(1)

        y += self.textHeight + self.padding
        self.w.posXLabel = TextBox(
                (x, y, -p, self.textHeight),
                'x alignment',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.alignmentX = PopUpButton(
                (x, y, -self.padding, self.textHeight),
                ['left', 'center', 'right'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)
        self.w.alignmentX.set(self.settings['posX'])

        y += self.textHeight + p
        self.w.overwrite = CheckBox(
                (x, y, -p, self.textHeight),
                "overwrite",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.buttonApply = Button(
                (x, y, -p, self.textHeight),
                "create",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

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
    def anchorName(self):
        return self.w.anchorName.get()

    @property
    def alignmentX(self):
        items = self.w.alignmentX.getItems()
        i = self.w.alignmentX.get()
        return items[i]

    @property
    def posY(self):
        return self.w.posY.get()

    @property
    def anchorY(self):
        y, reference = self.posY, self.referenceMetrics
        if reference:
            font = self.getCurrentFont()
            if not font:
                return
            y += [font.info.xHeight, font.info.capHeight][reference - 1]
        return y

    @property
    def overwrite(self):
        return self.w.overwrite.get()

    @property
    def referenceMetrics(self):
        return self.w.referenceMetrics.get()

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

        # draw preview

        x, y = self.makeAnchor(g, self.alignmentX)
        r = self.previewOriginRadius * s

        ctx.save()

        ctx.fill(None)
        ctx.stroke(*self.previewStrokeColor)
        ctx.strokeWidth(self.previewStrokeWidth * s)

        ctx.line((x - r, y), (x + r, y))
        ctx.line((x, y - r), (x, y + r))
        ctx.oval(x - r, y - r, r * 2, r * 2)

        ctx.restore()

    # -------
    # methods
    # -------

    def makeAnchor(self, glyph, alignmentX):

        bounds = glyph.bounds

        if bounds is None:
            w = glyph.width
        else:
            L, B, R, T = bounds
            w = R - L

        if alignmentX == 'left':
            x = glyph.leftMargin if bounds else 0

        elif alignmentX == 'right':
            x = glyph.leftMargin + w if bounds else w

        else: # center
            x = (glyph.leftMargin + w / 2) if bounds else w / 2

        return x, self.anchorY

    def apply(self):
        '''
        Create a new anchor with the current settings in the selected glyphs.

        '''

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
            print('creating anchors:\n')
            print(f'\ty position: {self.anchorY}')
            print(f'\tx alignment: {self.alignmentX}')
            print(f"\tlayers: {', '.join(layerNames)}")
            print(f"\tglyphs: {', '.join(glyphNames)}")

        # --------------
        # create anchors
        # --------------

        for glyphName in glyphNames:
            for layerName in layerNames:

                g = font[glyphName].getLayer(layerName)
                anchorPos = self.makeAnchor(g, self.alignmentX)
                g.prepareUndo('create anchor')

                # remove existing anchors with the same name
                if self.overwrite:
                    for anchor in g.anchors:
                        if anchor.name == self.anchorName:
                            g.removeAnchor(anchor)

                g.appendAnchor(self.anchorName, anchorPos)
                g.changed()
                g.performUndo()

        # done
        font.changed()
        print('\n...done.\n')


if __name__ == "__main__":

    CreateAnchorsDialog()
