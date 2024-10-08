from importlib import reload
import hTools3.dialogs.glyphs.base
reload(hTools3.dialogs.glyphs.base)

from vanilla import TextBox, PopUpButton, Button, List
# from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
# from defconAppKit.windows.baseWindow import BaseWindowController
# from hTools3.dialogs import hDialog
from hTools3.modules.anchors import copyAnchors
from hTools3.dialogs.glyphs.base import GlyphsCopyDataDialogBase


class CopyAnchorsDialog(GlyphsCopyDataDialogBase):

    '''
    A dialog to copy all anchors in the selected glyphs in one font to the same glyphs in another font or layer.

    ::

        from hTools3.dialogs.glyphs.anchorsCopy import CopyAnchorsDialog
        CopyAnchorsDialog()

    '''

    title = "anchors"
    key   = f'{GlyphsCopyDataDialogBase.key}.anchorsCopy'
    settings = {}

    # -------
    # methods
    # -------

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
            print('copying anchors:\n')
            print(f'\tsource layer: {sourceFontName} > {self.sourceLayer}')
            print('\ttarget layers:')
            for targetLayer in self.targetLayers:
                print(f"\t- {targetFontName} > {targetLayer}")
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
                targetGlyph.prepareUndo('copy anchors')
                copyAnchors(sourceGlyph, targetGlyph, clear=True, proportional=False)
                targetGlyph.changed()
                targetGlyph.performUndo()

        # done
        targetFont.changed()
        if self.verbose:
            print('\n...done.\n')
