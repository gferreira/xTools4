# menuTitle : decompose

from xTools4.dialogs.old import getLayerNames
from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.messages import noFontOpen, noGlyphSelected, showMessage

# TODO: read global settings
messageMode = 1
verbose     = True

def decomposeSelectedGlyphs(font):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    glyphNames = getGlyphs2(font, template=False)

    if not len(glyphNames):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    layerNames = getLayerNames()
    if not layerNames:
        layerNames = [font.defaultLayer.name]

    for glyphName in glyphNames:
        for layerName in layerNames:
            g = font[glyphName].getLayer(layerName)
            if not g.components:
                continue
            g.prepareUndo('clear anchors')
            for component in g.components:
                component.decompose()
            g.changed()
            g.performUndo()


if __name__ == '__main__':

    decomposeSelectedGlyphs(CurrentFont())
