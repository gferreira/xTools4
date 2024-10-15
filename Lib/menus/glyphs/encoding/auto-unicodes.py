# menuTitle : auto unicodes

from xTools4.modules.messages import noFontOpen, noGlyphSelected, showMessage
from xTools4.modules.unicode import autoUnicode, unicodesExtra
from xTools4.dialogs.old import getLayerNames

# TODO: read global settings
messageMode = 1
verbose = True

def autoUnicodes(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = font.selectedGlyphs

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    layers = getLayerNames()

    for glyph in selectedGlyphs:
        if layers:
            for layerName in layers:
                g = glyph.getLayer(layerName)
                autoUnicode(g, customUnicodes=unicodesExtra, verbose=verbose)
            if verbose:
                print()
        else:
            autoUnicode(glyph, customUnicodes=unicodesExtra, verbose=verbose)


if __name__ == '__main__':

    autoUnicodes(CurrentFont())
