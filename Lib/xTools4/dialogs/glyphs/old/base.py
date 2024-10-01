from importlib import reload
import hTools3.dialogs
reload(hTools3.dialogs)

from vanilla import TextBox, PopUpButton, Button, List
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.roboFont import AllFonts
from mojo.UI import UpdateCurrentGlyphView
from mojo.events import addObserver, removeObserver
from hTools3.dialogs import hDialog


class GlyphsDialogBase(hDialog, BaseWindowController):

    '''
    A Base object for tools which do something to selected glyphs in the current font.

    '''

    title = None
    key   = f'{hDialog.key}.glyphs'
    windowType = 0

    def initGlyphsWindowBehaviour(self):
        '''
        Initialize basic window behaviour.

        '''
        self.setUpBaseWindowBehavior()
        addObserver(self, "backgroundPreview", "drawBackground")
        addObserver(self, "backgroundPreview", "drawPreview")
        UpdateCurrentGlyphView()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        '''
        Removes observers from the dialog after the window is closed.

        '''
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")

    def updatePreviewCallback(self, sender):
        UpdateCurrentGlyphView()

    def applyCallback(self, sender):
        self.apply()

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):
        '''
        Draw a preview of the current settings in the background of the Glyph View.

        '''
        pass

    def backgroundPreviewPlain(self, notification):
        pass

    # -------
    # methods
    # -------

    def makeGlyph(self, glyph, *args):
        '''
        Transform an input glyph to make a new glyph.

        Args:
            glyph (RGlyph): An input glyph.

        Returns:
            An output glyph (RGlyph).

        '''
        pass

    def apply(self):
        '''
        Apply actions to selected glyphs.

        '''
        pass


class GlyphsCopyDataDialogBase(hDialog, BaseWindowController):

    title = None
    key = '%s.glyphs' % hDialog.key
    windowType = 0
    allFonts = {}

    def __init__(self):
        self.height  = self.textHeight * 9
        self.height += self.padding * 5 + 4
        self.w = self.window(
            (self.width, self.height), self.title,
            maxSize=(self.width * 1.5, self.height * 1.5),
            minSize=(self.width, self.height))

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

        self.allFonts = {'%s %s' % (f.info.familyName, f.info.styleName) : f for f in AllFonts()}

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
            sourceFontName = '%s %s' % (sourceFont.info.familyName, sourceFont.info.styleName)
            targetFontName = '%s %s' % (targetFont.info.familyName, targetFont.info.styleName)

            print('copying glyph data:\n')
            print(f'\tsource layer: {sourceFontName} > {self.sourceLayer}')
            print('\ttarget layers:')
            for targetLayer in self.targetLayers:
                print(f"\t- {targetFontName} > {targetLayer}")
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ---------
        # copy data
        # ---------

        for glyphName in glyphNames:
            sourceGlyph = sourceFont[glyphName].getLayer(self.sourceLayer)
            for targetLayer in self.targetLayers:
                targetGlyph = targetFont[glyphName].getLayer(targetLayer)
                targetGlyph.prepareUndo('copy glyph data')
                ############################
                ### copy glyph data here ###
                ############################
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
