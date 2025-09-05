from vanilla import PopUpButton, Button, CheckBox, TextBox
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from xTools4.dialogs.old import hDialog
from xTools4.modules.anchors import copyAnchors

# TODO: add observers for layerset changes
# update UI when adding/deleting/renaming layers

class MaskDialog(hDialog, BaseWindowController):

    '''
    A dialog to transfer glyphs between main layer and mask layer.

    ::

        from hTools3.dialogs.glyphs.layersMask import MaskDialog
        MaskDialog()

    '''

    title = 'mask'
    key   = f'{hDialog.key}.glyphs.layers.mask'
    settings = {
        'copyWidth'   : True,
        'copyAnchors' : True,
    }

    def __init__(self):
        self.height  = self.textHeight * 9
        self.height += self.padding * 6 -5
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = "LayerMask"

        x = p = self.padding
        y = p - 3
        self.w.sourceLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                'main layer',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateSourceLayerCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p # - 5
        self.w.maskLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                'mask layer',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.maskLayers = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p # + 5
        self.w.copyButton = Button(
                (x, y, -p, self.textHeight),
                "copy",
                sizeStyle=self.sizeStyle,
                callback=self.copyCallback)

        y += self.textHeight + p/2
        self.w.switchButton = Button(
                (x, y, -p, self.textHeight),
                "flip",
                sizeStyle=self.sizeStyle,
                callback=self.flipLayersCallback)

        y += self.textHeight + p/2
        self.w.clearButton = Button(
                (x, y, -p, self.textHeight),
                "clear",
                sizeStyle=self.sizeStyle,
                callback=self.clearMaskCallback)

        y += self.textHeight + p
        self.w.lockLayerWidths = CheckBox(
                (x, y, -p, self.textHeight),
                'copy width',
                value=self.settings['copyWidth'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.copyAnchors = CheckBox(
                (x, y, -p, self.textHeight),
                'copy anchors',
                value=self.settings['copyAnchors'],
                sizeStyle=self.sizeStyle)

        self.updateSourceLayer()
        self.updateMaskLayersList()
        self.setUpBaseWindowBehavior()
        addObserver(self, 'updateLayersObserver', 'currentGlyphChanged')
        addObserver(self, 'updateLayersObserver', 'newFontDidOpen')
        addObserver(self, 'updateLayersObserver', 'fontDidOpen')
        addObserver(self, 'updateLayersObserver', 'fontDidClose')
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceLayer(self):
        i = self.w.sourceLayer.get()
        return self.w.sourceLayer.getItems()[i]

    @property
    def maskLayer(self):
        i = self.w.maskLayers.get()
        return self.w.maskLayers.getItems()[i]

    @property
    def lockLayerWidths(self):
        return self.w.lockLayerWidths.get()

    @property
    def copyAnchors(self):
        return self.w.copyAnchors.get()

    # ---------
    # observers
    # ---------

    def updateLayersObserver(self, sender):
        self.updateSourceLayer()
        self.updateMaskLayersList()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, 'currentGlyphChanged')
        removeObserver(self, 'newFontDidOpen')
        removeObserver(self, 'fontDidOpen')
        removeObserver(self, 'fontDidClose')

    def updateSourceLayerCallback(self, sender):
        font = self.getCurrentFont()
        if not font:
            return
        self.updateMaskLayersList()

    def flipLayersCallback(self, sender):
        '''
        Flip contents between source layer and mask layer.

        '''
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        for glyphName in glyphNames:
            g = font[glyphName]
            g.flipLayers(self.sourceLayer, self.maskLayer)

            if self.lockLayerWidths:
                sourceGlyph = font[glyphName].getLayer(self.sourceLayer)
                maskGlyph   = font[glyphName].getLayer(self.maskLayer)
                maskGlyph.width = sourceGlyph.width

    def clearMaskCallback(self, sender):
        '''
        Clear mask layer in selected glyphs.

        '''
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        for glyphName in glyphNames:
            g = font[glyphName].getLayer(self.maskLayer)
            g.prepareUndo('clear mask layer')
            g.clear()
            g.performUndo()

    def copyCallback(self, sender):
        '''
        Copy foreground layer to mask layer.

        '''
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        for glyphName in glyphNames:
            g = font[glyphName].getLayer(self.sourceLayer)
            g.copyToLayer(self.maskLayer, clear=False)

            if self.lockLayerWidths:
                sourceGlyph = font[glyphName].getLayer(self.sourceLayer)
                maskGlyph   = font[glyphName].getLayer(self.maskLayer)
                maskGlyph.width = sourceGlyph.width

            if self.copyAnchors:
                sourceGlyph = font[glyphName].getLayer(self.sourceLayer)
                maskGlyph   = font[glyphName].getLayer(self.maskLayer)
                copyAnchors(sourceGlyph, maskGlyph, clear=False, proportional=False)

    # -------
    # methods
    # -------

    def updateSourceLayer(self):
        '''
        Update source layer pop-up list based on the current font.

        '''
        font = self.getCurrentFont()
        if not font:
            self.w.sourceLayer.setItems([])
        else:
            self.w.sourceLayer.setItems(font.layerOrder)

    def updateMaskLayersList(self):
        '''
        Update mask layer pop-up list based on the current font.

        '''
        font = self.getCurrentFont()
        if not font:
            self.w.maskLayers.setItems([])
        else:
            maskLayers = list(font.layerOrder)
            maskLayers.remove(self.sourceLayer)
            self.w.maskLayers.setItems(maskLayers)

# -------
# testing
# -------

if __name__ == "__main__":

    MaskDialog()
