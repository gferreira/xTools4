from vanilla import TextBox, PopUpButton, Button, List
from mojo.events import addObserver, removeObserver
from xTools4.modules.anchors import copyAnchors
from xTools4.dialogs.glyphs.old.base import GlyphsCopyDataDialogBase


KEY = f'{GlyphsDialogBase.key}.anchorsCopy'


class CopyAnchorsDialog(GlyphsCopyDataDialogBase):

    '''
    A dialog to copy all anchors in the selected glyphs in one font to the same glyphs in another font or layer.

    ::

        from xTools4.dialogs.glyphs.old.anchorsCopy import CopyAnchorsDialog
        CopyAnchorsDialog()

    '''

    title = "anchors"
    key   = KEY
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
            sourceFontName = f'{sourceFont.info.familyName} {sourceFont.info.styleName}'
            targetFontName = f'{targetFont.info.familyName} {targetFont.info.styleName}'
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


