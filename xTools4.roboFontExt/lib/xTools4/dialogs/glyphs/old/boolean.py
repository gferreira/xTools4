from vanilla import *
from mojo import drawingTools as ctx
from mojo.UI import getDefault
from mojo.events import removeObserver
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


def booleanGlyphFactory(glyph, glyph1, glyph2, operation):

    if operation == 'subtract':
        result = glyph1 % glyph2

    elif operation == 'add':
        result = glyph1 | glyph2

    elif operation == 'intersect':
        result = glyph1 & glyph2

    else:
        result = glyph1 ^ glyph2

    return result


class BooleanOperationsDialog(GlyphsDialogBase):

    '''
    A dialog to apply boolean glyph operations between layers of the selected glyphs.

    ::

        from xTools4.dialogs.glyphs.old.boolean import BooleanOperationsDialog
        BooleanOperationsDialog()

    '''

    title = 'boolean'
    key   = f'{GlyphsDialogBase.key}.boolean'
    settings = {}

    operations = [
        'add',
        'subtract',
        'intersect',
        'exclude'
    ]

    def __init__(self):
        self.height  = self.textHeight * 9
        self.height += self.textHeight * len(self.operations)
        self.height += self.padding * 6 + 7
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 3
        self.w.glyph1Label = TextBox(
                (x, y, -p, self.textHeight),
                "shape 1",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.glyph1Layer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p - 3
        self.w.glyph2Label = TextBox(
                (x, y, -p, self.textHeight),
                "shape 2",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.glyph2Layer = PopUpButton(
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

        y += self.textHeight + p
        listHeight = self.textHeight * len(self.operations)
        self.w.operation = RadioGroup(
                (x, y, -p, listHeight),
                self.operations,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                isVertical=True)
        self.w.operation.set(0)

        y += listHeight + p - 5
        self.w.clear = CheckBox(
                (x, y, -p, self.textHeight),
                "clear layer",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.buttonApply = Button(
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

        self.initGlyphsWindowBehaviour()

        registerRepresentationFactory(Glyph, "%s.preview" % self.key, booleanGlyphFactory)

        # TODO: add observer to update layers when the current font changes
        self.updateLayers()

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def glyph1Layer(self):
        selection = self.w.glyph1Layer.get()
        return self.w.glyph1Layer.getItems()[selection]

    @property
    def glyph2Layer(self):
        selection = self.w.glyph2Layer.get()
        return self.w.glyph2Layer.getItems()[selection]

    @property
    def targetLayer(self):
        selection = self.w.targetLayer.get()
        items = self.w.targetLayer.getItems()
        return items[selection] if items else None

    @property
    def boolOperation(self):
        selection = self.w.operation.get()
        return self.operations[selection]

    @property
    def clearGlyph(self):
        return bool(self.w.clear.get())

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

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        '''
        Removes observers and representation factories after the window is closed.

        '''
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        unregisterRepresentationFactory(Glyph, "%s.preview" % self.key)

    # -------
    # methods
    # -------

    def makeGlyph(self, glyph, preview=False):

        g1 = glyph.getLayer(self.glyph1Layer)
        g2 = glyph.getLayer(self.glyph2Layer)

        if preview:
            glyph = glyph.copy()

        result = glyph.getRepresentation("%s.preview" % self.key, glyph1=g1, glyph2=g2, operation=self.boolOperation) # clear=self.clearGlyph
        glyph.appendGlyph(result)

        return glyph

    def updateLayers(self):
        font = self.getCurrentFont()
        if font is None:
            return
        self.w.glyph1Layer.setItems(font.layerOrder)
        self.w.glyph2Layer.setItems(font.layerOrder)
        self.w.targetLayer.setItems(font.layerOrder)

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
            print('boolean glyph:\n')
            print('\tlayer 1: %s' % self.glyph1Layer)
            print('\tlayer 2: %s' % self.glyph2Layer)
            print(f'\ttarget layer: {self.targetLayer}')
            print('\toperation: %s' % self.boolOperation)
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            g = font[glyphName].getLayer(self.targetLayer)
            g.prepareUndo('boolean operation')
            if self.clearGlyph:
                g.clear()
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

if __name__ == '__main__':

    BooleanOperationsDialog()
