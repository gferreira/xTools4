import os
from mojo.roboFont import OpenFont
from vanilla import Button, TextBox, PopUpButton, RadioGroup, EditText, CheckBox
from vanilla.dialogs import getFile
from xTools4.modules.anchors import copyAnchors
from xTools4.modules.pens import DecomposePointPen
from xTools4.dialogs.old import hDialog


KEY = f'{hDialog.key}.glyphs.layersImport'


tempEditModeKey = 'com.xTools4.tempEdit.mode'


class ImportGlyphsIntoLayerDialog(hDialog):

    '''
    A dialog to import glyphs from a font file into a layer of the selected glyphs.

    ::

        from xTools4.dialogs.glyphs.old.layersImport import ImportGlyphsIntoLayerDialog
        ImportGlyphsIntoLayerDialog()

    '''

    title = 'layers'
    key = KEY
    sourceFont = None

    settings = {
        'layerName' : 'background',
    }

    def __init__(self):
        self.height  = self.textHeight * 8
        self.height += self.padding * 9
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.getFile = Button(
                (x, y, -p, self.textHeight),
                "get ufo...",
                callback=self.getFontCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.sourceLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                "source layer",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.sourceLayers = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.targetLayerLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target layer",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.targetLayer = RadioGroup(
                (x, y, -p, self.textHeight * 2),
                ["font name", "custom"],
                isVertical=True,
                sizeStyle=self.sizeStyle)
        self.w.targetLayer.set(1)

        y += self.textHeight * 2 + p
        self.w.targetLayerName = EditText(
                (x, y, -p, self.textHeight),
                self.settings['layerName'],
                # placeholder='layer name',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.decompose = CheckBox(
                (x, y, -p, self.textHeight),
                "decompose",
                value=False,
                sizeStyle='small')

        y += self.textHeight + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "import",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.w.workspaceWindowIdentifier = KEY

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceLayer(self):
        i = self.w.sourceLayers.get()
        return self.w.sourceLayers.getItems()[i]

    @property
    def targetLayer(self):
        if self.w.targetLayer.get() == 0:
            return '%s %s %s' % (self.sourceFont.info.familyName, self.sourceFont.info.styleName, self.sourceLayer)
        else:
            layerName = self.w.targetLayerName.get()
            if len(layerName):
                return layerName
            else:
                return 'untitled'

    # ---------
    # callbacks
    # ---------

    def getFontCallback(self, sender):
        selectedFiles = getFile()
        if not selectedFiles:
            # rewrite with xTools4.modules.messages.showMessage
            print('no file selected, aborting.\n')
            return

        ufoPath = selectedFiles[0]
        self.sourceFont = OpenFont(ufoPath, showInterface=False)
        self.w.sourceLayers.setItems(self.sourceFont.layerOrder)

    def applyCallback(self, sender):
        self.apply()

    # -------
    # methods
    # -------

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        if not self.sourceFont:
            print('no source font selected.\n')
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        decompose = self.w.decompose.get()

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('importing glyphs into layer...\n')
            print('\tsource font: %s %s' % (self.sourceFont.info.familyName, self.sourceFont.info.styleName))
            print('\tsource layer: %s' % self.sourceLayer)
            print('\ttarget layer: %s' % self.targetLayer)
            print('\tdecompose: %s' % decompose)
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # -----------
        # copy glyphs
        # -----------

        for glyphName in glyphNames:

            # get default glyph from temp glyph
            if font.lib.get(tempEditModeKey) == 'glyphs':
                defaultGlyphName = glyphName[:glyphName.rfind('.')]
            else:
                defaultGlyphName = glyphName

            if not defaultGlyphName in self.sourceFont:
                continue

            sourceGlyph = self.sourceFont[defaultGlyphName].getLayer(self.sourceLayer)

            targetGlyph = font[glyphName].getLayer(self.targetLayer)
            pen = targetGlyph.getPointPen()
            if decompose and len(sourceGlyph.components):
                decomposePen = DecomposePointPen(sourceGlyph.font, pen)
                sourceGlyph.drawPoints(decomposePen)
            else:
                sourceGlyph.drawPoints(pen)
            
            targetGlyph.width = sourceGlyph.width
            copyAnchors(sourceGlyph, targetGlyph, clear=True, proportional=False)
            targetGlyph.changed()

            # try:
            #     targetLayer = self.sourceFont.getLayer(self.targetLayer)
            # except:
            #     targetLayer = self.sourceFont.newLayer(self.targetLayer)

            # targetLayer.insertGlyph(sourceGlyph, name=glyphName)
            # targetLayer[glyphName].changed()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    ImportGlyphsIntoLayerDialog()
