# menuTitle: new glyphs from templates

from xTools4.modules.messages import noFontOpen, noGlyphSelected, showMessage
from xTools4.dialogs.old import getLayerNames

# TODO: read global settings
messageMode = 1
verbose = True


def createSelectedTemplates(font):

    if font is None:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    selectedGlyphs = font.templateSelectedGlyphNames

    if not len(selectedGlyphs):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    layers = getLayerNames()

    if layers:
        for layerName in layers:
            layer = font.getLayer(layerName)
            for glyphName in selectedGlyphs:
                layer.newGlyph(glyphName)
                # layer[glyphName].changed()
            if verbose:
                print()
    else:
        for glyphName in selectedGlyphs:
            font.newGlyph(glyphName)
            # font[glyphName].changed()


if __name__ == '__main__':

    createSelectedTemplates(CurrentFont())
