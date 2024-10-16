# menuTitle : create guides

from xTools4.dialogs.old import getLayerNames
from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.messages import noFontOpen, noGlyphSelected, noPointSelected, showMessage

# TODO: read global settings
messageMode = 1
verbose = True

def newGuidesFromSelection(font, mode=0):

    if not font:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    modes = ['vertical', 'horizontal']

    if font.info.italicAngle is None:
        italicAngle = 0
    else:
        italicAngle = font.info.italicAngle

    angle = 90 + italicAngle if not mode else 0

    glyphNames = getGlyphs2(font, template=False)

    if not len(glyphNames):
        if verbose:
            showMessage(noGlyphSelected, messageMode)
        return

    layerNames = getLayerNames()
    if not layerNames:
        layerNames = [font.defaultLayer.name]

    if verbose:
        print(f'creating {modes[mode]}  guides at selected points...\n')

    for glyphName in glyphNames:
        for layerName in layerNames:
            g = font[glyphName].getLayer(layerName)
            # no points selected
            if not len(g.selectedBPoints):
                print(f"\tskipping {g.name} ({g.layer.name}), no point(s) selected.")
                # print(noPointSelected)
                continue
            # create guides
            if verbose:
                print(f"\tcreating guides in '{g.name}' ({g.layer.name})...")
            g.prepareUndo('new guides from selection')
            for pt in g.selectedPoints:    
                g.appendGuideline((pt.x, pt.y), angle)
            g.changed()
            g.performUndo()

    if verbose:
        print('\n...done.\n')


if __name__ == '__main__':

    newGuidesFromSelection(CurrentFont(), mode=0)
