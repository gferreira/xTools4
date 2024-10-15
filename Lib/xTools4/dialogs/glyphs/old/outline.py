from vanilla import TextBox, RadioGroup, Button, CheckBox, PopUpButton
from mojo import drawingTools as ctx
from mojo.roboFont import RGlyph
from mojo.events import addObserver, removeObserver
from mojo.UI import getDefault, UpdateCurrentGlyphView
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.modules.outline import expandGlyph
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase
from xTools4.dialogs.old.misc.numberEditText01 import NumberEditText_01


def outlineGlyphFactory(glyph, layerName, distance, join, cap, inner, outer):

    glyph = RGlyph(glyph).getLayer(layerName)
    srcGlyph = glyph.copy()
    srcGlyph.clearComponents()
    srcGlyph.correctDirection()

    dstGlyph = RGlyph()
    expandGlyph(srcGlyph, dstGlyph, distance, join=join, cap=cap, inner=outer, outer=inner)

    return dstGlyph


class OutlineGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to visualize and apply an outline to glyph contours.

    ::

        from hTools3.dialogs.glyphs.outline import OutlineGlyphsDialog
        OutlineGlyphsDialog()

    '''

    title = 'outline'
    key   = f'{GlyphsDialogBase.key}.outline'
    settings = {
        'strokeWidth' : 20,
        'joinstyle'   : 1,
        'capstyle'    : 1,
    }
    strokeParameters = ['Square', 'Round', 'Butt']

    def __init__(self):
        self.height  = self.textHeight * 13
        self.height += self.padding * 9
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        y -= 3
        self.w.sourceLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                'source layer',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateSourceLayerCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.targetLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                'target layer',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.targetLayer = PopUpButton(
            (x, y, -p, self.textHeight),
            [],
            sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 5
        self.w.strokeWidthLabel = TextBox(
                (x, y, col, self.textHeight),
                'stroke',
                sizeStyle=self.sizeStyle)
        self.w.strokeWidthValue = NumberEditText_01(
                (x+col, y, -p, self.textHeight),
                text=self.settings['strokeWidth'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                continuous=False)

        y += self.textHeight + p
        self.w.joinLabel = TextBox(
                (x, y, -p, self.textHeight),
                "join style",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.join = RadioGroup(
                (x, y, -p, self.textHeight),
                ['S', 'R', 'B'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                isVertical=False)
        self.w.join.set(self.settings['joinstyle'])

        y += self.textHeight + p
        self.w.capLabel = TextBox(
                (x, y, -p, self.textHeight),
                "cap style",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.cap = RadioGroup(
                (x, y, -p, self.textHeight),
                ['S', 'R', 'B'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                isVertical=False)
        self.w.cap.set(self.settings['capstyle'])

        y += self.textHeight + p
        self.w.edgeLabel = TextBox(
                (x, y, -p, self.textHeight),
                "edges",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        w = (self.width - p * 2) * 0.5
        self.w.edgeInner = CheckBox(
                (x, y, w, self.textHeight),
                "inner",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)
        self.w.edgeOuter = CheckBox(
                (x + w, y, w, self.textHeight),
                "outer",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.buttonApply = Button(
                (x, y, -p, self.textHeight),
                "apply",
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
        addObserver(self, 'updateLayersObserver', 'currentGlyphChanged')
        addObserver(self, 'updateLayersObserver', 'newFontDidOpen')
        addObserver(self, 'updateLayersObserver', 'fontDidOpen')
        addObserver(self, 'updateLayersObserver', 'fontDidClose')
        registerRepresentationFactory(Glyph, f"{self.key}.preview", outlineGlyphFactory)
        self.updateSourceLayer()
        self.updateTargetLayer()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceLayer(self):
        i = self.w.sourceLayer.get()
        return self.w.sourceLayer.getItems()[i]

    @property
    def targetLayer(self):
        i = self.w.targetLayer.get()
        return self.w.targetLayer.getItems()[i]

    @property
    def distance(self):
        return self.w.strokeWidthValue.get()

    @property
    def join(self):
        return self.w.join.get()

    @property
    def cap(self):
        return self.w.cap.get()

    @property
    def inner(self):
        return self.w.edgeInner.get()

    @property
    def outer(self):
        return self.w.edgeOuter.get()

    # ---------
    # callbacks
    # ---------

    def updateSourceLayerCallback(self, sender):

        font = self.getCurrentFont()
        if not font:
            return

        self.updateTargetLayer()

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        removeObserver(self, 'currentGlyphChanged')
        removeObserver(self, 'newFontDidOpen')
        removeObserver(self, 'fontDidOpen')
        removeObserver(self, 'fontDidClose')
        unregisterRepresentationFactory(Glyph, f"{self.key}.preview")

    # ---------
    # observers
    # ---------

    def updateLayersObserver(self, sender):
        self.updateSourceLayer()
        self.updateTargetLayer()

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
        previewGlyph = g.getRepresentation(
            f"{self.key}.preview",
            layerName=self.sourceLayer,
            distance=self.distance,
            join=self.join,
            cap=self.cap,
            inner=self.inner,
            outer=self.outer
        )

        if previewGlyph is None:
            return

        if not previewGlyph.bounds:
            return

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def updateSourceLayer(self):
        font = self.getCurrentFont()
        if not font:
            self.w.sourceLayer.setItems([])
        else:
            self.w.sourceLayer.setItems(font.layerOrder)

    def updateTargetLayer(self):
        font = self.getCurrentFont()
        if not font:
            self.w.targetLayer.setItems([])
        else:
            targetLayers = list(font.layerOrder)
            targetLayers.remove(self.sourceLayer)
            self.w.targetLayer.setItems(targetLayers)

    def drawPreview(self, glyph, previewScale, plain=False):

        ctx.save()

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = 10000 # getDefault("glyphViewDefaultWidth")
            h = 10000 # getDefault("glyphViewDefaultHeight")
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        ctx.restore()

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
            print('outlining contours...\n')
            print(f'\tdistance: {self.distance}')
            print(f'\tjoin: {self.strokeParameters[self.join]}')
            print(f'\tcap: {self.strokeParameters[self.cap]}')
            print(f'\tinner: {bool(self.inner)}')
            print(f'\touter: {bool(self.outer)}')
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:

            g = font[glyphName]
            result = g.getRepresentation(
                f"{self.key}.preview",
                layerName=self.sourceLayer,
                distance=self.distance,
                join=self.join,
                cap=self.cap,
                inner=self.inner,
                outer=self.outer
            )

            dstGlyph = g.getLayer(self.targetLayer)
            dstGlyph.prepareUndo('outline glyphs')
            dstGlyph.clearContours()
            dstGlyph.appendGlyph(result)
            dstGlyph.changed()
            dstGlyph.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    OutlineGlyphsDialog()
