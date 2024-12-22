# menuTitle : center glyph

from xTools4.modules.messages import noFontOpen, noGlyphSelected, showMessage
from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.glyphutils import centerGlyph
from xTools4.dialogs.old import getLayerNames

# TODO: read global settings
messageMode = 1
verbose = True

def centerSelectedGlyphs(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    # selectedGlyphs = font.selectedGlyphs
    glyphNames = getGlyphs2(font, template=False)

    if not len(glyphNames):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
            return

    layers = getLayerNames()

    for glyphName in glyphNames:
        if layers:
            for layerName in layers:
                g = font[glyphName].getLayer(layerName)
                centerGlyph(g, verbose=verbose)
            if verbose:
                print()
        else:
            centerGlyph(font[glyphName])


if __name__ == '__main__':

    centerSelectedGlyphs(CurrentFont())
