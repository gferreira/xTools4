# menuTitle: invert selection

from xTools4.modules.messages import noFontOpen, showMessage
from xTools4.dialogs.old import getLayerNames

# TODO: read global settings
messageMode = 1
verbose = True


def invertSelection(font):

    if font is None:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    allGlyphs = set(font.glyphOrder)
    selection = set(font.selectedGlyphNames)
    inverseSelection = allGlyphs.difference(selection)

    font.selectedGlyphNames = inverseSelection


if __name__ == '__main__':

    invertSelection(CurrentFont())
