import os, sys
from colorsys import hsv_to_rgb
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from vanilla import FloatingWindow, List, Button, TextBox, EditText, RadioGroup, ProgressBar, Group
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import GlyphSet
from mojo.UI import AccordionView
from mojo.roboFont import OpenFont, NewFont, CurrentFont


KEY = 'com.xTools4.dialogs.variable.old.tempEdit'


def splitall(path):
    # copied from http://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def setupNewFont(font, showPoints=True):
    # create background layer
    if 'background' not in font.layerOrder:
        font.newLayer('background')
        font.changed()
    # set layer display options
    displayOptions = {
        'Fill'        : False,
        'Stroke'      : True,
        'Points'      : showPoints,
        'Coordinates' : False,
    }
    for i, layer in enumerate(font.layers):
        hue = i * 1.0 / (len(font.layers) - 1)
        layerColor = hsv_to_rgb(hue, 1, 1) + (1,)
        layer.color = layerColor
        layer.setDisplayOption(displayOptions)


class TempEdit:

    title      = 'TempEdit'
    key        = KEY
    width      = 123*3
    height     = 640
    padding    = 10
    lineHeight = 22
    verbose    = True

    _designspaces = {}
    _sources = {}

    def __init__(self):
        self.w = FloatingWindow(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width*0.9, self.width*0.5))

        self.designspaces = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.designspaces.list = List(
                (x, y, -p, -p),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                # editCallback=self.selectDesignspaceCallback,
                selectionCallback=self.selectDesignspaceCallback,
                enableDelete=True,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropCallback),
                )

        self.sources = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.sources.list = List(
                (x, y, -p, -p),
                [],
                allowsMultipleSelection=True,
                enableDelete=False,
            )

        self.glyphs = Group((0, 0, -0, -0))

        x = y = p = self.padding
        textBoxHeight = -(self.lineHeight * 5) - (p * 3)
        self.glyphs.names = EditText(
                (x, y, -p, textBoxHeight),
                'a b c A B C one two three')

        y = -(p + self.lineHeight) * 4
        self.glyphs.importButton = Button(
                (x, y, -p, self.lineHeight),
                'import glyphs',
                callback=self.importButtonCallback)

        y = -(p + self.lineHeight) * 3
        self.glyphs.importMode = RadioGroup(
                (x, y, -p, self.lineHeight),
                ['fonts → fonts', 'fonts → glyphs', 'fonts → layers'],
                sizeStyle='small',
                isVertical=False)
        self.glyphs.importMode.set(2)

        y = -(p + self.lineHeight) * 2
        self.glyphs.exportButton = Button(
                (x, y, -p, self.lineHeight),
                'export selected glyphs',
                callback=self.exportButtonCallback)

        y = -(p + self.lineHeight)
        self.glyphs.progress = ProgressBar((x, y, -p, self.lineHeight))

        descriptions = [
           dict(label="designspaces",
                view=self.designspaces,
                size=self.lineHeight*5,
                minSize=self.lineHeight*3,
                collapsed=False,
                canResize=True
            ),
           dict(label="sources",
                view=self.sources,
                size=self.lineHeight*8,
                minSize=self.lineHeight*6,
                collapsed=False,
                canResize=True,
            ),
            dict(label="glyphs",
                view=self.glyphs,
                size=self.lineHeight*10,
                minSize=self.lineHeight*8,
                collapsed=False,
                canResize=True
            ),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def glyphNames(self):
        return self.glyphs.names.get().split()

    @property
    def selectedDesignspace(self):
        selection = self.designspaces.list.getSelection()
        designspaces = self.designspaces.list.get()
        return [designspace for i, designspace in enumerate(designspaces)] \
            if len(designspaces) else None

    @property
    def selectedMasters(self):
        selection = self.sources.list.getSelection()
        masters   = self.sources.list.get()
        return [master for i, master in enumerate(masters) if i in selection]

    @property
    def glyphSetPathKey(self):
        return f'{self.key}.glyphSetPath'

    @property
    def importMode(self):
        return self.glyphs.importMode.get()

    # ---------
    # callbacks
    # ---------

    def selectDesignspaceCallback(self, sender):

        selection = sender.getSelection()
        designSpaces = self.designspaces.list.get()

        # delete current list
        # posSize = self.sources.list.getPosSize()
        # del self.sources.list

        # list of sources is empty
        if not selection or not len(designSpaces):
            items = []
            self.sources.list.set([])
            return

        # get sources from selected designspace
        designSpaceLabel = [D for i, D in enumerate(designSpaces) if i in selection][0]
        designSpacePath = self._designspaces[designSpaceLabel]
        designSpace = DesignSpaceDocument()
        designSpace.read(designSpacePath)

        # get column descriptions
        descriptions  = [{"title": 'name', "width": 210, "minWidth": 180 }]
        descriptions += [{"title": axis.name, "width": 40} for axis in designSpace.axes]

        # make list items
        self._sources = {}
        # items = []
        for source in designSpace.sources:
            sourceName = os.path.splitext(os.path.split(source.path)[-1])[0]
            self._sources[sourceName] = source.path
        #     item = { 'name' : sourceName }
        #     for axis in designSpace.axes:
        #         item[axis.name] = source.location[axis.name]
        #     items.append(item)

        # create list UI with items
        self.sources.list.set(self._sources.keys()) # = List(
        #     posSize, items,
        #     columnDescriptions=descriptions,
        #     allowsMultipleSelection=True,
        #     enableDelete=False)

    def dropCallback(self, sender, dropInfo):

        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.designspace']

        if not paths:
            return False

        if not isProposal:
            for path in paths:
                label = os.path.splitext(os.path.split(path)[-1])[0]
                self._designspaces[label] = path
                self.designspaces.list.append(label)
                self.designspaces.list.setSelection([0])

        return True

    def importButtonCallback(self, sender):

        if not len(self.selectedMasters):
            return

        if self.verbose:
            print('importing glyphs from selected sources...\n')

        # mode 0 : fonts → fonts

        if self.importMode == 0:

            for i, master in enumerate(self.selectedMasters):
                srcPath = self._sources[master]
                srcFont = OpenFont(srcPath, showInterface=False)
                tmpFont = NewFont(familyName=srcFont.info.familyName, styleName=srcFont.info.styleName, showInterface=False)

                # copy vertical metrics from source font
                for attr in ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender']:
                    value = getattr(srcFont.info, attr)
                    setattr(tmpFont.info, attr, value)

                setupNewFont(tmpFont)

                glyphsFolder = os.path.join(srcPath, 'glyphs')
                ufoName = splitall(glyphsFolder)[-2]

                if self.verbose:
                    print(f'\t{ufoName}:')

                for glyphName in self.glyphNames:
                    if glyphName not in srcFont:
                        if self.verbose:
                            print(f'\t\t{glyphName} not in font.')
                        continue

                    srcGlyph = srcFont[glyphName]
                    if srcGlyph.components:
                        for component in srcGlyph.components:
                            if not component.baseGlyph in tmpFont:
                                if self.verbose:
                                    print(f'\t\timporting {component.baseGlyph} ({glyphName})...')
                                tmpFont[component.baseGlyph] = srcFont[component.baseGlyph]
                                tmpFont[component.baseGlyph].lib[self.glyphSetPathKey] = glyphsFolder

                    if self.verbose:
                        print(f'\t\timporting {glyphName}...')
                    tmpFont[glyphName] = srcGlyph
                    tmpFont[glyphName].lib[self.glyphSetPathKey] = glyphsFolder

                srcFont.close()
                tmpFont.openInterface()

                if self.verbose:
                    print()

        # mode 1 : fonts → glyphs

        elif self.importMode == 1:
            tmpFont = CurrentFont()
            tmpFontIsNew = False
            if tmpFont is None:
                tmpFontIsNew = True
                tmpFont = NewFont(familyName='tempEdit')
                # tmpFont.changed()
                setupNewFont(tmpFont)

            for i, master in enumerate(self.selectedMasters):
                ufoPath = self._sources[master]
                if not os.path.exists(ufoPath):
                    if self.verbose:
                        print(f'source file does not exist: {ufoPath}')
                    continue

                srcFont = OpenFont(ufoPath, showInterface=False)

                # copy vertical metrics from 1st source font
                if tmpFontIsNew and i == 0:
                    for attr in ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender']:
                        value = getattr(srcFont.info, attr)
                        setattr(tmpFont.info, attr, value)

                glyphsFolder = os.path.join(ufoPath, 'glyphs')
                ufoName = splitall(glyphsFolder)[-2]
                glyphNameExtension = os.path.splitext(ufoName)[0]

                for glyphName in self.glyphNames:

                    tmpGlyphName = f'{glyphName}.{glyphNameExtension}'

                    if glyphName not in srcFont:
                        if self.verbose:
                            print(f'\t\tcreating {glyphName}...')
                            tmpFont.newGlyph(tmpGlyphName)

                    else:
                        srcGlyph = srcFont[glyphName]
                        for component in srcGlyph.components:
                            if component.baseGlyph not in tmpFont:
                                if component.baseGlyph not in srcFont:
                                    continue
                                if self.verbose:
                                    print(f'\t\timporting {component.baseGlyph} ({glyphName})...')
                                tmpBaseGlyph = f'{component.baseGlyph}.{glyphNameExtension}'
                                tmpFont[tmpBaseGlyph] = srcFont[component.baseGlyph]
                                tmpFont[tmpBaseGlyph].lib[self.glyphSetPathKey] = glyphsFolder

                        if self.verbose:
                            print(f'\t\timporting {glyphName}...')

                        tmpFont.newGlyph(tmpGlyphName)
                        tmpFont[tmpGlyphName].appendGlyph(srcGlyph)
                        tmpFont[tmpGlyphName].width = srcGlyph.width
                        tmpFont.changed()

                    tmpFont[tmpGlyphName].lib[self.glyphSetPathKey] = glyphsFolder

                if self.verbose:
                    print()

        # mode 2 : fonts → layers

        else:

            tmpFont = CurrentFont()
            tmpFontIsNew = False
            if tmpFont is None:
                tmpFont = NewFont(familyName='tempEdit')
                tmpFontIsNew = True

            for i, master in enumerate(self.selectedMasters):
                ufoPath = self._sources[master]
                if not os.path.exists(ufoPath):
                    if self.verbose:
                        print(f'source file does not exist: {ufoPath}')
                    continue

                srcFont = OpenFont(ufoPath, showInterface=False)

                # copy vertical metrics from 1st source font
                if tmpFontIsNew and i == 0:
                    for attr in ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender']:
                        value = getattr(srcFont.info, attr)
                        setattr(tmpFont.info, attr, value)

                glyphsFolder = os.path.join(ufoPath, 'glyphs')
                ufoName = splitall(glyphsFolder)[-2]
                layerName = os.path.splitext(ufoName)[0]
                tmpLayer = tmpFont.newLayer(layerName)

                if self.verbose:
                    print(f'\t{ufoName}:')

                if i == 0:
                    tmpFont.defaultLayer = tmpLayer
                    if 'foreground' in tmpFont.layerOrder:
                        tmpFont.removeLayer('foreground')

                for glyphName in self.glyphNames:

                    if glyphName not in srcFont:
                        if self.verbose:
                            print(f'\t\tcreating {glyphName}...')
                            tmpLayer.newGlyph(glyphName)

                    else:
                        srcGlyph = srcFont[glyphName]
                        for component in srcGlyph.components:
                            if component.baseGlyph not in tmpLayer:
                                if component.baseGlyph not in srcFont:
                                    continue
                                if self.verbose:
                                    print(f'\t\timporting {component.baseGlyph} ({glyphName})...')
                                tmpLayer[component.baseGlyph] = srcFont[component.baseGlyph]
                                tmpLayer[component.baseGlyph].lib[self.glyphSetPathKey] = glyphsFolder

                        if self.verbose:
                            print(f'\t\timporting {glyphName}...')
                        tmpLayer[glyphName] = srcGlyph
                        tmpLayer[glyphName].width = srcGlyph.width

                    tmpLayer[glyphName].lib[self.glyphSetPathKey] = glyphsFolder

                if self.verbose:
                    print()

            if tmpFontIsNew:
                setupNewFont(tmpFont, showPoints=False)

        if self.verbose:
            print('...done.\n')

    def exportButtonCallback(self, sender):

        f = CurrentFont()

        if f is None:
            return

        if self.verbose:
            print('exporting selected glyphs back to their sources...\n')

        for glyphName in f.selectedGlyphNames:

            if self.importMode == 1:

                glyph = f[glyphName].getLayer('foreground')

                if self.glyphSetPathKey not in glyph.lib:
                    continue

                glyphsFolder = glyph.lib[self.glyphSetPathKey]
                ufoName = splitall(glyphsFolder)[-2]
                glyphNameExtension = os.path.splitext(ufoName)[0]
                glyphNameParts = glyphName.split('.')

                if not (len(glyphNameParts) > 1 and glyphNameParts[-1] == os.path.splitext(ufoName)[0]):
                    print(f'{glyphName} does not have the expected glyph name extension, skipping...')
                    continue

                if self.verbose:
                    print(f'\twriting {glyphName} to {ufoName}...')

                outputGlyphName = '.'.join(glyphNameParts[:-1])
                glyphSet = GlyphSet(glyphsFolder, validateWrite=True)
                glyphSet.writeGlyph(outputGlyphName, glyph.naked(), glyph.drawPoints)
                glyphSet.writeContents()

            else:

                for layerName in f.layerOrder:
                    glyph = f[glyphName].getLayer(layerName)

                    if self.glyphSetPathKey not in glyph.lib:
                        continue

                    glyphsFolder = glyph.lib[self.glyphSetPathKey]

                    # mode 0
                    if not '.ufoz' in glyphsFolder:
                        glyphSet = GlyphSet(glyphsFolder, validateWrite=True)
                        ufoName = splitall(glyphsFolder)[-2]
                        if self.verbose:
                            print(f'\twriting {glyphName} to {ufoName}...')
                        glyphSet.writeGlyph(glyphName, glyph.naked(), glyph.drawPoints)
                        glyphSet.writeContents()

                    # mode 2
                    else:
                        ufoPath = os.path.dirname(glyphsFolder)
                        ufoName = splitall(ufoPath)[-1]
                        dstFont = OpenFont(ufoPath, showInterface=False)
                        if self.verbose:
                            print(f'\twriting {glyphName} to {ufoName}...')
                        dstFont.insertGlyph(glyph, name=glyph.name)
                        dstFont.save()
                        dstFont.close()

        if self.verbose:
            print()
            print('...done.\n')

