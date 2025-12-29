from vanilla import TextBox, PopUpButton, CheckBox, Button
from mojo import drawingTools as ctx
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase
from xTools4.dialogs.old.misc.numberEditText001 import NumberEditText_001

KEY = 'com.xTools4.dialogs.glyphs.interpolationMasters'
class InterpolateGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to interpolate glyphs from two master fonts into selected glyphs in the current font.

    ::

        from hTools3.dialogs.glyphs.interpolationMasters import InterpolateGlyphsDialog
        InterpolateGlyphsDialog()

    '''

    title = 'interpolate'
    key   = f'{GlyphsDialogBase.key}.interpolationMasters'
    settings = {
        'factorX'      : 0.5,
        'factorY'      : 0.5,
        'proportional' : True,
    }
    allFonts = {}

    def __init__(self):
        self.height  = self.textHeight * 13
        self.height += self.padding * 10 + 3
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        y -= 2
        self.w.masterLabel1 = TextBox(
                (x, y, -p, self.textHeight),
                "master 1",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.masterFont1 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateLayersCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + 7
        self.w.masterLayer1 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.masterLabel2 = TextBox(
                (x, y, -p, self.textHeight),
                "master 2",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.masterFont2 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateLayersCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + 7
        self.w.masterLayer2 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.targetLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.targetLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                # callback=self.updateLayersCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 3
        self.w.labelX = TextBox(
                (x, y, col, self.textHeight),
                'x factor',
                sizeStyle=self.sizeStyle)
        self.w.factorX = NumberEditText_001(
                (x+col, y, -p, self.textHeight),
                text=self.settings['factorX'],
                callback=self.factorXCallback,
                sizeStyle=self.sizeStyle,
                continuous=False)

        y += self.textHeight + p
        self.w.labelY = TextBox(
                (x, y, col, self.textHeight),
                'y factor',
                sizeStyle=self.sizeStyle)

        self.w.factorY = NumberEditText_001(
                (x+col, y, -p, self.textHeight),
                text=self.settings['factorY'],
                callback=self.factorYCallback,
                sizeStyle=self.sizeStyle,
                continuous=False)

        y += self.textHeight + p
        self.w.proportional = CheckBox(
                (x, y, -p, self.textHeight),
                "proportional",
                value=self.settings['proportional'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.buttonApply = Button(
                (x, y, -p, self.textHeight),
                "interpolate",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.updateFonts()
        self.updateFontLists()
        self.updateLayerLists()
        self.initGlyphsWindowBehaviour()
        addObserver(self, "updateFontsCallback", "newFontDidOpen")
        addObserver(self, "updateFontsCallback", "fontDidOpen")
        addObserver(self, "updateFontsCallback", "fontDidClose")
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def masterName1(self):
        selection = self.w.masterFont1.get()
        items = self.w.masterFont1.getItems()
        return items[selection]

    @property
    def masterLayer1(self):
        selection = self.w.masterLayer1.get()
        items = self.w.masterLayer1.getItems()
        return items[selection] if items else None

    @property
    def master1(self):
        return self.allFonts[self.masterName1]

    @property
    def masterName2(self):
        selection = self.w.masterFont2.get()
        items = self.w.masterFont2.getItems()
        return items[selection] if items else None

    @property
    def masterLayer2(self):
        selection = self.w.masterLayer2.get()
        items = self.w.masterLayer2.getItems()
        return items[selection]

    @property
    def master2(self):
        return self.allFonts[self.masterName2]

    @property
    def factorX(self):
        return self.w.factorX.get()

    @property
    def factorY(self):
        return self.w.factorY.get()

    @property
    def proportional(self):
        return bool(self.w.proportional.get())

    @property
    def targetLayer(self):
        selection = self.w.targetLayer.get()
        items = self.w.targetLayer.getItems()
        return items[selection] if items else None

    # ---------
    # callbacks
    # ---------

    def factorXCallback(self, sender):
        if self.proportional:
            factorX = self.w.factorX.get()
            self.w.factorY.set(factorX)
        UpdateCurrentGlyphView()

    def factorYCallback(self, sender):
        if self.proportional:
            factorY = self.w.factorY.get()
            self.w.factorX.set(factorY)
        UpdateCurrentGlyphView()

    def updateFontsCallback(self, sender):
        self.updateFonts()
        self.updateFontLists()

    def updateLayersCallback(self, sender):
        self.updateLayerLists()
        UpdateCurrentGlyphView()

    def windowCloseCallback(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontWillClose")
        removeObserver(self, "drawBackground")
        super().windowCloseCallback(sender)

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

    def updateFonts(self):
        allFonts = {}
        for font in AllFonts():
            fontName = '%s %s' % (font.info.familyName, font.info.styleName)
            allFonts[fontName] = font
        # update fonts list
        self.allFonts = allFonts

    def updateFontLists(self):
        allFontsNames = sorted(self.allFonts.keys())
        self.w.masterFont1.setItems(allFontsNames)
        self.w.masterFont2.setItems(allFontsNames)

    def updateLayerLists(self):
        if self.master1 is not None:
            self.w.masterLayer1.setItems(self.master1.layerOrder)
        if self.master2 is not None:
            self.w.masterLayer2.setItems(self.master2.layerOrder)
        font = self.getCurrentFont()
        if font is not None:
            self.w.targetLayer.setItems(font.layerOrder)

    def drawPreview(self, glyph, previewScale, plain=False):
        w = h = 10000

        s  = previewScale
        x1 = 0
        x2 = glyph.width
        y1 = -h
        y2 = h

        ctx.save()

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth*s)
        else:
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * s, -h * s, w * s * 2, h * s * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        if not plain:
            ctx.lineDash(self.previewStrokeWidth*s, self.previewStrokeWidth*s)
            ctx.line((x1, y1), (x1, y2))
            ctx.line((x2, y1), (x2, y2))

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):

        factor = self.factorX, self.factorY

        if preview:
            glyph = glyph.copy()

        g1 = self.master1.getLayer(self.masterLayer1)[glyph.name]
        g2 = self.master2.getLayer(self.masterLayer2)[glyph.name]

        glyph.interpolate(factor, g1, g2)

        return glyph

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if font is None:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('interpolating glyphs:\n')
            print(f'\tmaster 1: {self.masterName1} > {self.masterLayer1}')
            print(f'\tmaster 2: {self.masterName2} > {self.masterLayer2}')
            print(f'\ttarget layer: {self.targetLayer}')
            print(f'\tfactor x: {self.factorX}')
            print(f'\tfactor y: {self.factorY}')
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName].getLayer(self.targetLayer)
            g.prepareUndo('interpolate')
            self.makeGlyph(g)
            g.performUndo()
            g.changed()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    InterpolateGlyphsDialog()
