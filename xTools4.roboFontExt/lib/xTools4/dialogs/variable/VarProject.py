import os
import AppKit
from vanilla import *
from mojo.UI import AccordionView
from xTools4.modules.designspacePlus import DesignSpacePlus
from xTools4.modules.measurements import FontMeasurements
from xTools4.modules.validation import applyValidationColors


def setNamesFromMeasurements(font, familyName, measurementsPath, ignoreTags=['wght', 'wdth', 'opsz', 'GRAD', 'BARS']):

    # maybe it's better to have it the other way around? that is:
    # define which tags to measure instead of which ones to ignore.

    if font.info.familyName != familyName:
        print(f'family name: {font.info.familyName} --> {familyName}' )
        if not preflight:
            font.info.familyName = familyName

    if tag in ignoreTags:
        print(f'getting {tag} value from file name: {os.path.split(ufo)[-1]}...')
        newValue = newValue1000 = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
        print(f'\t{newValue}')

    else:
        print(f'measuring {tag} in {os.path.split(ufo)[-1]}...')
        m = FontMeasurements()
        m.read(measurementsPath)
        m.measure(f)
        newValue = m.values[tag]
        newValue1000 = round(newValue * 1000 / font.info.unitsPerEm)
        print(f'\tunits  = {newValue}')
        print(f'\tpermil = {newValue1000}')

    # set style name
    newStyleName = f'{tag}{newValue1000}'
    allNames.append(newStyleName)
    if newStyleName != font.info.styleName:
        print(f'style name: {font.info.styleName} --> {newStyleName}' )
        if not preflight:
            font.info.styleName = newStyleName

    # rename UFO file
    newFileName = f'{familyName}_{newStyleName}.ufo'
    newFilePath = os.path.join(os.path.split(font.path)[0], newFileName)
    if not preflight:
        font.save()
    font.close()

    if ufo != newFilePath:
        print(f'\tfile name: {os.path.split(ufo)[-1]} --> {newFileName}' )
        if not preflight:
            shutil.move(ufo, newFilePath)

    print()

def applyValidationColors(font):
    # this function probably already exists in the validation module
    pass

def copyGlyphOrder(font, sourceFont):

    glyphOrder = sourceFont.templateGlyphOrder

    print(f'setting glyph order in {os.path.split(font.path)[-1]}…')
    font.templateGlyphOrder = glyphOrder

    # mark glyphs which are not in the default font
    diffGlyphs = set(font.keys()).difference(set(glyphOrder))
    for glyphName in diffGlyphs:
        font[glyphName].markColor = 1, 0, 0, 0.35

def copyFeatures(font, sourceFont):

    print(f'copying features to {os.path.split(font.path)[-1]}...')

    font.features.text = sourceFont.features.text

def copyUnicodes(font, sourceFont):

    print(f'copying unicodes to {os.path.split(font.path)[-1]}...')
    for glyphName in font.glyphOrder:
        if glyphName not in sourceFont:
            continue
        font[glyphName].unicodes = sourceFont[glyphName].unicodes

def buildGlyphs(font, glyphNames, glyphConstructionPath, verbose=True):

    # load glyph constructions from file
    with open(glyphConstructionPath, 'r') as f:
        glyphConstructions = f.read()

    print(f'building glyphs in {os.path.split(font.path)[-1]}...')
    buildAccentedGlyphs(font, glyphNames, glyphConstructions, clear=True, verbose=verbose, autoUnicodes=False, indentLevel=1)

def copyGlyphs(font, sourceFont, glyphNames):

    print(f'copying glyphs to {os.path.split(font.path)[-1]}...')
    for glyphName in glyphNames:
        if glyphName not in sourceFont:
            print(f'\tERROR: {glyphName} not in source font')
            continue
        print(f'\tcopying {glyphName}...')
        if not preflight:
            font.insertGlyph(sourceFont[glyphName], name=glyphName)

def cleanupBeforeCommit(font):
    # clear background layer
    # remove mark colors
    # clear glyph libs
    pass


class VarProjectController:

    title      = 'VarProject'
    width      = 123*2
    height     = 640
    padding    = 10
    lineHeight = 22
    verbose    = True

    _designspaces = {}
    _sources      = {}

    _fontActions  = {
        'set names from measurements' : False,
        'set validation mark colors'  : False,
        'copy default glyph order'    : False,
        'copy default features'       : False,
        'copy default unicodes'       : False,
        'cleanup before commit'       : False,
    }

    glyphConstructionPath = None

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
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropDesignspaceCallback),
                )

        self.sources = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.sources.list = List((x, y, -p, -self.lineHeight-p*2), [])
        
        y = -self.lineHeight - p
        self.sources.validate = Button(
                (x, y, -p, self.lineHeight),
                'validate locations',
                sizeStyle='small',
                callback=self.validateLocationsCallback)
        
        y += p

        # font actions

        self.fontActions = Group((0, 0, -0, -0))

        x = y = p = self.padding

        self.fontActions.list = List(
                (x, y, -p, -self.lineHeight-p*2),
                self._fontActions)

        y = -self.lineHeight - p
        self.fontActions.apply = Button(
                (x, y, -p, self.lineHeight),
                'apply actions to sources',
                sizeStyle='small',
                callback=self.applyFontActionsCallback)

        # glyph actions

        self.glyphsCopy = Group((0, 0, -0, -0))

        x = y = p = self.padding
        textBoxHeight = -(self.lineHeight * 1) - (p * 2)
        self.glyphsCopy.names = EditText(
                (x, y, -p, textBoxHeight),
                'a b c A B C one two three')

        y = -(p + self.lineHeight)
        self.glyphsCopy.apply = Button(
                (x, y, -p, self.lineHeight),
                'copy default glyphs to sources',
                sizeStyle='small',
                callback=self.copyGlyphsCallback)

        self.glyphsBuild = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.glyphsBuild.glyphConstruction = Button(
                (x, y, -p, self.lineHeight),
                'get glyph constructions…',
                sizeStyle='small',
                callback=self.getGlyphConstructionsCallback)

        y += self.lineHeight + p
        textBoxHeight = -(self.lineHeight * 1) - (p * 2)
        self.glyphsBuild.names = EditText(
                (x, y, -p, textBoxHeight),
                'a b c A B C one two three')

        y = -(p + self.lineHeight)
        self.glyphsBuild.apply = Button(
                (x, y, -p, self.lineHeight),
                'build glyphs in sources',
                sizeStyle='small',
                callback=self.buildGlyphsCallback)

        self.glyphsRemove = Group((0, 0, -0, -0))

        x = y = p = self.padding
        textBoxHeight = -(self.lineHeight * 1) - (p * 2)
        self.glyphsRemove.names = EditText(
                (x, y, -p, textBoxHeight),
                'a b c A B C one two three')

        y = -(p + self.lineHeight)
        self.glyphsRemove.apply = Button(
                (x, y, -p, self.lineHeight),
                'remove glyphs from sources',
                sizeStyle='small',
                callback=self.deleteGlyphsCallback)
            
        # build accordion

        descriptions = [
           dict(label="designspaces",
                view=self.designspaces,
                size=self.lineHeight*5,
                minSize=self.lineHeight*3,
                collapsed=False,
                canResize=True),
           dict(label="sources",
                view=self.sources,
                size=self.lineHeight*8,
                minSize=self.lineHeight*6,
                collapsed=False,
                canResize=True),
           dict(label="font actions",
                view=self.fontActions,
                size=self.lineHeight*8,
                minSize=self.lineHeight*12,
                collapsed=True,
                canResize=False),
           dict(label="copy glyphs",
                view=self.glyphsCopy,
                size=self.lineHeight*6,
                minSize=self.lineHeight*4,
                collapsed=True,
                canResize=True),
           dict(label="build glyphs",
                view=self.glyphsBuild,
                size=self.lineHeight*7,
                minSize=self.lineHeight*6,
                collapsed=True,
                canResize=True),
           dict(label="remove glyphs",
                view=self.glyphsRemove,
                size=self.lineHeight*6,
                minSize=self.lineHeight*4,
                collapsed=True,
                canResize=True),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    # dynamic attributes

    @property
    def selectedDesignspace(self):
        designspacesList = self.designspaces.list
        selection = designspacesList.getSelection()
        designspaces = designspacesList.get()
        selectedDesignspaces = [designspace for i, designspace in enumerate(designspaces) if i in selection]
        if not len(selectedDesignspaces):
            return
        return selectedDesignspaces[0]

    @property
    def selectedDesignspacePath(self):
        if not self.selectedDesignspace:
            return
        return self._designspaces[self.selectedDesignspace]

    @property
    def selectedDesignspacePlus(self):
        if not self.selectedDesignspacePath:
            return
        return DesignSpacePlus(self.selectedDesignspacePath)

    @property
    def selectedFontActions(self):
        pass

    @property
    def defaultFont(self):
        pass

    @property
    def selectedSources(self):
        pass

    @property
    def familyName(self):
        pass

    @property
    def measurementsPath(self):
        # let's assume that there is a measurements.json file next to the default for now
        pass

    # callbacks

    def dropDesignspaceCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.designspace']

        if not paths:
            return False

        if not isProposal:
            designspacesList = self.designspaces.list
            for path in paths:
                label = os.path.split(path)[-1]
                self._designspaces[label] = path
                designspacesList.append(label)
                designspacesList.setSelection([0])

        return True

    def selectDesignspaceCallback(self, sender):

        if not self.selectedDesignspace:
            self.sources.list.set([])
            return

        self._sources = {}
        for source in self.selectedDesignspacePlus.document.sources:
            if source.path == self.selectedDesignspacePlus.default.path:
                continue
            sourceFileName = os.path.splitext(os.path.split(source.path)[-1])[0]
            self._sources[sourceFileName] = source.path

        self.sources.list.set(self._sources.keys())

    def validateLocationsCallback(self, sender):

        designspace = self.selectedDesignspacePlus
        if designspace is None:
            return

        doc = designspace.document

        # validate source locations
        locations = []
        for src in doc.sources:
            if src not in locations:
                locations.append(src.location)
            else:
                print(src.name, src.location)

        # validate instance locations
        # axes = { axis.tag: axis for axis in doc.axes }
        # for instance in doc.instances:
        #     print(instance.name)
        #     for axisName, value in instance.designLocation.items():
        #         axis = axes[axisName]
        #         if not axis.minimum <= value <= axis.maximum:
        #             print(f"!! {axisName} {value} ({axis.minimum} {axis.maximum}) {'-' if value < axis.minimum else '+' if value > axis.maximum else ''} ")
        #     print()

    def applyFontActionsCallback(self, sender):

        actions   = self.selectedFontActions
        preflight = self.fontActionsPreflight

        defaultFont = self.defaultFont

        for source in self.selectedSources:
            for action in actions:
                if 'set names from measurements':
                    self.setNamesFromMeasurements(source, defaultFont)
                if 'set validation mark colors':
                    applyValidationColors(source, defaultFont)
                if 'copy default glyph order':
                    self.copyGlyphOrder(source, defaultFont)
                if 'copy default features':
                    self.copyFeatures(source, defaultFont)
                if 'copy default unicodes':
                    self.copyUnicodes(source, defaultFont)
                if 'cleanup before commit':
                    self.cleanupBeforeCommit(source)

            if not preflight:
                source.save()

    def copyGlyphsCallback(self, sender):

        glyphNames = self.glyphsCopy.names.get().split()
        if not glyphNames:
            return

        for source in self.selectedSources:
            copyGlyphs(source, self.defaultFont, glyphNames)


    def getGlyphConstructionsCallback(self, sender):
        pass


    def buildGlyphsCallback(self, sender):

        glyphNames = self.glyphsBuild.names.get().split()
        if not glyphNames:
            return

        for source in self.selectedSources:

            buildGlyphs(source, glyphNames, self.glyphConstructionPath)


    def deleteGlyphsCallback(self, sender):
        pass

    # methods > font


if __name__ == '__main__':

    VarProjectController()


