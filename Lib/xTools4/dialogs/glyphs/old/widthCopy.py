from vanilla import TextBox, PopUpButton, Button, List
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from xTools4.dialogs.old import hDialog

KEY = 'com.xTools4.widthCopy'
class CopyWidthDialog(hDialog, BaseWindowController):

    '''
    A dialog to copy the width from selected glyphs in one font to the same glyphs in another font or layer.

    ::

        from xTools4.dialogs.glyphs.old.widthCopy import CopyWidthDialog
        CopyWidthDialog()

    '''

    title = 'width'
    key   = f'{hDialog.key}.glyphs.widthCopy'
    allFonts = {}

    def __init__(self):
        self.height  = self.textHeight * 9
        self.height += self.padding * 5 + 4
        self.w = self.window(
            (self.width, self.height), self.title,
            maxSize=(self.width * 1.5, self.height * 1.5),
            minSize=(self.width, self.height))
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        y -= 2
        self.w.sourceLabel = TextBox(
                (x, y, -p, self.textHeight),
                "source",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateSourceLayerCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.targetLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.targetFont = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateTargetFontCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        listHeight = -(self.textHeight + p) -p
        self.w.targetLayers = List(
                (x, y, -p, listHeight),
                [])

        y = -(self.textHeight + p) - 3
        self.w.apply = Button(
                (x, y, -p, self.buttonHeight),
                "copy",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.updateSourceLayer()
        self.updateTargetFonts()
        self.updateTargetLayers()
        self.setUpBaseWindowBehavior()
        addObserver(self, 'updateListsObserver', 'currentGlyphChanged')
        addObserver(self, 'updateListsObserver', 'newFontDidOpen')
        addObserver(self, 'updateListsObserver', 'fontDidOpen')
        addObserver(self, 'updateListsObserver', 'fontDidClose')
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceFont(self):
        return self.getCurrentFont()

    @property
    def sourceLayer(self):
        i = self.w.sourceLayer.get()
        items = self.w.sourceLayer.getItems()
        if not items:
            return
        return items[i]

    @property
    def targetFont(self):
        i = self.w.targetFont.get()
        items = self.w.targetFont.getItems()
        if not items:
            return
        fontName = items[i]
        return self.allFonts.get(fontName)

    @property
    def targetLayers(self):
        selection = self.w.targetLayers.getSelection()
        layers    = self.w.targetLayers.get()
        return [L for i, L in enumerate(layers) if i in selection]

    # ---------
    # observers
    # ---------

    def updateListsObserver(self, sender):
        self.updateSourceLayer()
        self.updateTargetFonts()
        self.updateTargetLayers()

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
        self.updateTargetLayers()

    def updateTargetFontCallback(self, sender):
        self.updateTargetLayers()

    def applyCallback(self, sender):
        self.apply()

    # -------
    # methods
    # -------

    def updateSourceLayer(self):

        if not self.sourceFont:
            self.w.sourceLayer.setItems([])
            return

        self.w.sourceLayer.setItems(self.sourceFont.layerOrder)

    def updateTargetFonts(self):

        if not self.sourceFont:
            self.w.targetFont.setItems([])
            return

        self.allFonts = { f'{f.info.familyName} {f.info.styleName}' : f for f in AllFonts() }

        if not self.allFonts:
            self.w.targetFont.setItems([])
            return

        self.w.targetFont.setItems(self.allFonts.keys())

    def updateTargetLayers(self):

        sourceFont = self.getCurrentFont()
        targetFont = self.targetFont

        if not targetFont:
            self.w.targetLayers.set([])
            return

        targetLayers = targetFont.layerOrder

        if sourceFont == targetFont:
            targetLayers.remove(self.sourceLayer)

        self.w.targetLayers.set(targetLayers)

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        sourceFont = self.sourceFont
        if not sourceFont:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        targetFont = self.targetFont

        # ----------
        # print info
        # ----------

        if self.verbose:
            sourceFontName = f'{sourceFont.info.familyName} {sourceFont.info.styleName}'
            targetFontName = f'{targetFont.info.familyName} {targetFont.info.styleName}'
            print('copying glyph widths:\n')
            print(f'\tsource layer: {sourceFontName} > {self.sourceLayer}')
            print('\ttarget layers:')
            for targetLayer in self.targetLayers:
                print(f"\t- {targetLayer}")
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # -----------
        # copy widths
        # -----------

        for glyphName in glyphNames:
            sourceGlyph = sourceFont[glyphName].getLayer(self.sourceLayer)
            for targetLayer in self.targetLayers:
                targetGlyph = targetFont[glyphName].getLayer(targetLayer)
                targetGlyph.prepareUndo('copy width')
                targetGlyph.width = sourceGlyph.width
                targetGlyph.changed()
                targetGlyph.performUndo()

        # done
        targetFont.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    CopyWidthDialog()
