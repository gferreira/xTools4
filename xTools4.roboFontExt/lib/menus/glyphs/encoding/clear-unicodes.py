# menuTitle : clear unicodes

from xTools4.modules.messages import noFontOpen, noGlyphSelected, showMessage
from xTools4.dialogs.old import getLayerNames

# TODO: read global settings
messageMode = 1
verbose = True

def clearUnicodes(font):

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
                g.unicodes = []
            if verbose:
                print()

        else:
            glyph.unicodes = []


if __name__ == '__main__':

    clearUnicodes(CurrentFont())
