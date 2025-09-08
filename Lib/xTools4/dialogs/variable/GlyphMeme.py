from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os
import ezui
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, NewFont, OpenFont, CurrentFont
from mojo.smartSet import readSmartSets
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import GlyphSet
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.measurements import FontMeasurements, GlyphMeasurements
from xTools4.dialogs.variable.old.TempEdit import setupNewFont, splitall


glyphSetPathKey        = 'com.xTools4.tempEdit.glyphSetPath'
tempEditModeKey        = 'com.xTools4.tempEdit.mode'
fontMeasurementsKey    = 'com.xTools4.measurements.font'
defaultMeasurementsKey = 'com.xTools4.measurements.default'


class GlyphMemeController(ezui.WindowController):

    title   = 'parameters'
    margins = 10
    verbose = True

    designspacePath  = None
    measurementsPath = None
    smartsetsPath    = None

    defaultFont = None
    glyphGroups = {}

    content = """
    (groups ...)  @groupSelector
    (glyphs ...)  @glyphSelector

    | | @glyphMeme

    ( open )  @openButton
    ( save )  @saveButton

    ---

    ( designspace…  )  @getDesignspaceButton
    ( measurements… )  @getMeasurementsButton
    ( smart sets…   )  @getSmartSetsButton

    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        groupSelector=dict(
            width='fill',
        ),
        glyphSelector=dict(
            width='fill',
        ),
        openButton=dict(
            width='fill',
        ),
        saveButton=dict(
            width='fill',
        ),
        getSmartSetsButton=dict(
            width='fill',
        ),
        getDesignspaceButton=dict(
            width='fill',
        ),
        getMeasurementsButton=dict(
            width='fill',
        ),
    )

    def build(self):
        self.w = ezui.EZPanel(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            margins=self.margins,
            size=(123, 400),
            minSize=(123, 300),
            maxSize=(123, 960),
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem("glyphMeme").getNSTableView().setRowHeight_(17)
        self.w.open()

    # def started(self):
    #     pass

    @property
    def familyName(self):
        if self.defaultFont is None:
            return
        return self.defaultFont.info.familyName

    def getDesignspaceButtonCallback(self, sender):
        self.designspacePath = GetFile(message='Select designspace file:')
        if self.designspacePath is None:
            return

        if self.verbose:
            print(f'loading designspace from {os.path.split(self.designspacePath)[-1]}... ', end='')

        self.designspace = DesignSpaceDocument()
        self.designspace.read(self.designspacePath)
        self.defaultFont = OpenFont(self.designspace.default.path, showInterface=False)

        if self.verbose:
            print('done.\n')

    def getMeasurementsButtonCallback(self, sender):
        self.measurementsPath = GetFile(message='Select measurements file:')
        if self.measurementsPath is None:
            return

        if self.verbose:
            print(f'loading measurements from {os.path.split(self.measurementsPath)[-1]}... ', end='')

        measurements = readMeasurements(self.measurementsPath)
        self.measurements = measurements['glyphs']

        if self.verbose:
            print('done.\n')

    def getSmartSetsButtonCallback(self, sender):
        self.smartsetsPath = GetFile(message='Select SmartSets file:')
        if self.smartsetsPath is None:
            return

        if self.verbose:
            print(f'loading glyph groups from {os.path.split(self.smartsetsPath)[-1]}... ', end='')

        smartSets = readSmartSets(self.smartsetsPath, useAsDefault=False, font=None)

        self.glyphGroups = {}
        for smartGroup in smartSets:
            if not smartGroup.groups:
                continue
            for smartSet in smartGroup.groups:
                # remove component glyphs from glyph lists
                glyphNames = []
                for glyphName in smartSet.glyphNames:
                    if glyphName not in self.defaultFont:
                        continue
                    g = self.defaultFont[glyphName]
                    if not len(g.components):
                        glyphNames.append(glyphName)
                if len(glyphNames):
                    self.glyphGroups[smartSet.name] = glyphNames

        groupSelector = self.w.getItem("groupSelector")
        groupSelector.setItems(self.glyphGroups.keys())
        self.groupSelectorCallback(None)

        if self.verbose:
            print('done.\n')

    def groupSelectorCallback(self, sender):
        groupSelector = self.w.getItem("groupSelector")
        glyphSelector = self.w.getItem("glyphSelector")
        selectedGroup = groupSelector.getItem()
        glyphSelector.setItems(self.glyphGroups[selectedGroup])
        self.glyphSelectorCallback(None)

    def glyphSelectorCallback(self, sender):
        glyphName = self.w.getItem("glyphSelector").getItem()
        measurementsDict = self.measurements.get(glyphName, {})
        measurements = sorted(list(set([m['name'] for m in measurementsDict.values()])))
        memesTable = self.w.getItem("glyphMeme")
        memesTable.set(measurements)
        memesTable.setSelectedIndexes(range(len(measurements)))

    def openButtonCallback(self, sender):

        glyphName = self.w.getItem("glyphSelector").getItem()
        selectedMeasurements = self.w.getItem("glyphMeme").getSelectedItems()

        # create temp font
        tmpFont = NewFont(familyName='tempEdit')
        setupNewFont(tmpFont)
        tmpFont.info.familyName = f'{self.familyName}'
        tmpFont.info.styleName  = glyphName

        # get parametric sources for current glyph
        sources = {}
        for src in self.designspace.sources:
            for measurementName in selectedMeasurements:
                if measurementName in src.styleName:
                    sources[src.filename] = src.path

        print('opening glyphs...\n')

        for i, sourceFile in enumerate(sources.keys()):
            # ufoPath = os.path.join(sourcesFolder, sourceFile)
            ufoPath = sources[sourceFile]
            srcFont = OpenFont(ufoPath, showInterface=False)

            # copy vertical metrics from 1st source
            if i == 0:
                for attr in ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender']:
                    value = getattr(srcFont.info, attr)
                    setattr(tmpFont.info, attr, value)

            # make temp glyph name
            glyphsFolder = os.path.join(ufoPath, 'glyphs')
            ufoName = splitall(glyphsFolder)[-2]
            glyphNameExtension = os.path.splitext(sourceFile)[0].split('_')[-1]
            tmpGlyphName = f'{glyphName}.{glyphNameExtension}'

            # import source glyph into temp font
            print(f'\timporting {glyphName} from {ufoName}...')
            srcGlyph = srcFont[glyphName]
            tmpFont.newGlyph(tmpGlyphName)
            tmpFont[tmpGlyphName].appendGlyph(srcGlyph)
            tmpFont[tmpGlyphName].width = srcGlyph.width
            tmpFont[tmpGlyphName].unicodes = srcGlyph.unicodes
            tmpFont.changed()

            # store the import mode in the font lib
            tmpFont.lib[tempEditModeKey] = 'glyphs'

            # get default font measurements
            FM = FontMeasurements()
            FM.read(self.measurementsPath)
            FM.measure(self.defaultFont)

            # get default glyph measurements
            GM = GlyphMeasurements(self.defaultFont, glyphName)
            GM.read(self.measurementsPath)
            GM.measure()

            # store default measurements in the font lib
            tmpFont.lib[defaultMeasurementsKey] = {
                'font'  : FM.values,
                'glyph' : GM.values,
            }

            # store path to glyphset in the glyph lib
            tmpFont[tmpGlyphName].lib[glyphSetPathKey] = glyphsFolder

            # store current font measurements in glyph lib
            FM.measure(srcFont)
            tmpFont[tmpGlyphName].lib[fontMeasurementsKey] = FM.values

        print('\n...done!\n')

    def saveButtonCallback(self, sender):

        f = CurrentFont()

        if f is None:
            return

        print('saving selected glyphs...\n')

        for glyphName in f.selectedGlyphNames:

            glyph = f[glyphName].getLayer('foreground')

            if glyphSetPathKey not in glyph.lib:
                continue

            glyphsFolder = glyph.lib[glyphSetPathKey]
            srcGlyphName = glyphName[:glyphName.rfind('.')]
            ufoName = splitall(glyphsFolder)[-2]

            print(f'\texporting {srcGlyphName} to {ufoName}...')
            glyphSet = GlyphSet(glyphsFolder, validateWrite=True)
            glyphSet.writeGlyph(srcGlyphName, glyph.naked(), glyph.drawPoints)
            glyphSet.writeContents()

        print('\n...done!\n')



if __name__ == '__main__':

    OpenWindow(GlyphMemeController)

