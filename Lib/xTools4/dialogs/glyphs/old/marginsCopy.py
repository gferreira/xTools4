from vanilla import TextBox, PopUpButton, Button, CheckBox
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from xTools4.dialogs.old import hDialog

KEY = 'com.xTools4.marginsCopy'
class CopyMarginsDialog(hDialog, BaseWindowController):

    '''
    A dialog to copy left/margin margins from selected glyphs in one font to the same glyphs in another font or layer.

    ::

        from xTools4.dialogs.glyphs.old.marginsCopy import CopyMarginsDialog
        CopyMarginsDialog()

    '''

    title = 'margins'
    key   = f'{hDialog.key}.glyphs.marginsCopy'
    allFonts = {}

    def __init__(self):
        self.height  = self.textHeight * 8
        self.height += self.padding * 3.5
        self.w = self.window((self.width, self.height), self.title)
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

        y += self.textHeight + p * 0.5
        self.w.targetLayer = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.left = CheckBox(
                (x, y, -p, self.textHeight),
                "left",
                value=True,
                sizeStyle=self.sizeStyle)

        x += self.width * 0.5 - 8
        self.w.right = CheckBox(
                (x, y, -p, self.textHeight),
                "right",
                value=True,
                sizeStyle=self.sizeStyle)

        x = p
        y += self.textHeight + p
        self.w.apply = Button(
                (x, y, -p, self.textHeight),
                "copy",
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

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
        return self.w.sourceLayer.getItems()[i]

    @property
    def targetFont(self):
        i = self.w.targetFont.get()
        targetFonts = self.w.targetFont.getItems()
        if not len(targetFonts):
            return
        fontName = self.w.targetFont.getItems()[i]
        return self.allFonts.get(fontName)

    @property
    def targetLayer(self):
        i = self.w.targetLayer.get()
        return self.w.targetLayer.getItems()[i]

    @property
    def left(self):
        return bool(self.w.left.get())

    @property
    def right(self):
        return bool(self.w.right.get())

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
        self.w.targetFont.setItems(self.allFonts.keys())

    def updateTargetLayers(self):

        sourceFont = self.getCurrentFont()
        targetFont = self.targetFont

        if not targetFont:
            self.w.targetLayer.setItems([])
            return

        targetLayers = targetFont.layerOrder

        if sourceFont == targetFont:
            targetLayers.remove(self.sourceLayer)

        self.w.targetLayer.setItems(targetLayers)

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

        targetFont  = self.targetFont

        left, right = self.left, self.right
        if not (left or right):
            print('select at least one side (left/right)')
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            sourceFontName = f'{sourceFont.info.familyName} {sourceFont.info.styleName}'
            targetFontName = f'{targetFont.info.familyName} {targetFont.info.styleName}'
            print('copying glyph margins:\n')
            print(f'\tsource: {sourceFontName} > {self.sourceLayer}')
            print(f'\ttarget: {targetFontName} > {self.targetLayer}')
            print(f'\tleft: {left}')
            print(f'\tright: {right}')
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # -----------
        # copy widths
        # -----------

        for glyphName in glyphNames:
            sourceGlyph = sourceFont[glyphName].getLayer(self.sourceLayer)
            targetGlyph = targetFont[glyphName].getLayer(self.targetLayer)
            targetGlyph.prepareUndo('copy margins')
            if left:
                targetGlyph.leftMargin = sourceGlyph.leftMargin
            if right:
                targetGlyph.rightMargin = sourceGlyph.rightMargin
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

    CopyMarginsDialog()
