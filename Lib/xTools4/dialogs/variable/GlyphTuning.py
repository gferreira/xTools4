import os, glob
import ezui
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, NewFont, OpenFont, CurrentFont
from mojo.smartSet import readSmartSets
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import GlyphSet
from xTools4.modules.xproject import measurementsPathKey, smartSetsPathKey
from xTools4.modules.validation import assignValidationGroup
from xTools4.dialogs.variable.old.TempEdit import setupNewFont, splitall


glyphSetPathKey = 'com.xTools4.tempEdit.glyphSetPath'
tempEditModeKey = 'com.xTools4.tempEdit.mode'
italicOffsetKey = 'com.typemytype.robofont.italicSlantOffset'


class GlyphTuningController(ezui.WindowController):

    title   = 'GlyphTuning'
    margins = 10
    verbose = True

    designspacePath  = None
    smartSetsPath    = None

    defaultFont   = None
    glyphGroups   = {}
    tuningSources = {}

    content = """
    (groups ...)  @groupSelector
    (glyphs ...)  @glyphSelector

    [X] duovars   @duovars 
    [X] trivars   @trivars
    [X] quadvars  @quadvars

    ( open )  @openButton
    ( save )  @saveButton

    ---

    ( designspace…  )  @getDesignspaceButton
    ( reload ↺ )       @reloadButton

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
        getDesignspaceButton=dict(
            width='fill',
        ),
        reloadButton=dict(
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
            size=(123, 'auto'),
        )
        self.w.workspaceWindowIdentifier = "GlyphTuning"
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        # self.w.getItem("axesList").getNSTableView().setRowHeight_(17)
        self.w.open()

    @property
    def familyName(self):
        if self.defaultFont is None:
            return
        return self.defaultFont.info.familyName

    @property
    def sourcesFolder(self):
        return os.path.dirname(self.designspacePath)

    @property
    def tuningSourcesFolder(self):
        return os.path.join(self.sourcesFolder, 'corners')

    @property
    def tuningSources(self):
        return {
            os.path.splitext(os.path.split(srcPath)[-1])[0] : OpenFont(srcPath, showInterface=False)
            for srcPath in glob.glob(f'{self.tuningSourcesFolder}/*.ufo')
        }

    @property
    def parametricAxes(self):
        return self.designspace.default.location.keys()

    @property
    def blendedAxes(self):
        return {
            tag : [axis for axis in self.designspace.axes if axis.tag == tag][0] 
            for tag in ['opsz', 'wght', 'wdth']
        }

    @property
    def smartSetsPath(self):
        fileName = self.designspace.lib.get(smartSetsPathKey)
        if fileName:
            return os.path.join(self.sourcesFolder, fileName)

    def _loadDesignspace(self):

        if self.verbose:
            print(f'loading designspace from {os.path.split(self.designspacePath)[-1]}... ', end='')

        self.designspace = DesignSpaceDocument()
        self.designspace.read(self.designspacePath)
        self.defaultFont = OpenFont(self.designspace.default.path, showInterface=False)

        if self.verbose:
            print('done.\n')

        # self._loadTuningSources()
        # self._loadAxes()
        self._loadSmartSets()

    def _loadSmartSets(self):

        if self.verbose:
            print(f'loading glyph groups from {os.path.split(self.smartSetsPath)[-1]}... ', end='')

        smartSets = readSmartSets(self.smartSetsPath, useAsDefault=False, font=None)

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

    # def _loadAxes(self):
    #     if self.verbose:
    #         print(f'loading blended axes... ', end='')

    #     axesItems = []
    #     for axis in self.designspace.axes:
    #         for axisName in self.blendedAxes:
    #             if axisName in self.ignoreAxes or axisName.startswith('TN'):
    #                 continue
    #             if axisName == axis.name:
    #                 axesItems.append({
    #                     'axis' : axis.tag,
    #                     'values': f'{int(axis.minimum)} {int(axis.default)} {int(axis.maximum)}',
    #                 })

    #     self.w.getItem('axesList').set(axesItems)

    def getDesignspaceButtonCallback(self, sender):
        self.designspacePath = GetFile(
            message='Select designspace file:',
            title=self.title, 
            allowsMultipleSelection=False,
            fileTypes=["designspace"]
        )
        if self.designspacePath is None:
            return

        self._loadDesignspace()

    def groupSelectorCallback(self, sender):
        groupSelector = self.w.getItem("groupSelector")
        glyphSelector = self.w.getItem("glyphSelector")
        selectedGroup = groupSelector.getItem()
        glyphSelector.setItems(self.glyphGroups[selectedGroup])
        self.glyphSelectorCallback(None)

    def glyphSelectorCallback(self, sender):
        self._updateTuningSources()

    def openButtonCallback(self, sender):

        glyphName = self.w.getItem("glyphSelector").getItem()
        duovars   = self.w.getItem("duovars").get()
        trivars   = self.w.getItem("trivars").get()
        quadvars  = self.w.getItem("quadvars").get()

        axesList = []
        for axisTag, axis in self.blendedAxes.items():
            axisValues = [ int(v) for v in set([axis.minimum, axis.default, axis.maximum]) ]
            axisValues.sort()
            axesList.append((axisTag, axisValues))

        axis1Tag, axis1Values = axesList[0]
        axis2Tag, axis2Values = axesList[1]
        axis3Tag, axis3Values = axesList[2]

        for axis in self.designspace.axes:
            if axis1Tag == axis.tag:
                axis1Default = axis.default
            elif axis2Tag == axis.tag:
                axis2Default = axis.default
            elif axis3Tag == axis.tag:
                axis3Default = axis.default

        # create temp font
        tmpFont = NewFont(familyName='tempEdit')
        setupNewFont(tmpFont)
        tmpFont.info.familyName  = f'{self.familyName}'
        tmpFont.info.styleName   = glyphName

        print('opening glyphs...\n')

        for i, axisValue1 in enumerate(sorted(axis1Values)):
            for j, axisValue2 in enumerate(reversed(sorted(axis2Values))):
                for k, axisValue3 in enumerate(sorted(axis3Values)):

                    styleName = []
                    if axisValue1 != axis1Default:
                        styleName.append(f'{axis1Tag}{axisValue1}')
                    if axisValue2 != axis2Default:
                        styleName.append(f'{axis2Tag}{axisValue2}')
                    if axisValue3 != axis3Default:
                        styleName.append(f'{axis3Tag}{axisValue3}')

                    if len(styleName) == 0:
                        continue
                    elif len(styleName) == 1 and not duovars:
                        continue
                    elif len(styleName) == 2 and not trivars:
                        continue
                    elif len(styleName) == 3 and not quadvars:
                        continue

                    styleName = '_'.join(styleName)
                    if styleName not in self.tuningSources:
                        continue

                    srcFont = self.tuningSources[styleName]

                    # copy vertical metrics etc. from 1st source
                    if i == 0:
                        for attr in ['unitsPerEm', 'xHeight', 'capHeight', 'descender', 'ascender', 'italicAngle']:
                            value = getattr(srcFont.info, attr)
                            setattr(tmpFont.info, attr, value)
                        italicOffset = srcFont.lib.get(italicOffsetKey)
                        if italicOffset:
                            tmpFont.lib[italicOffsetKey] = italicOffset

                    # make temp glyph name
                    glyphsFolder = os.path.join(srcFont.path, 'glyphs')
                    ufoName = splitall(glyphsFolder)[-2]
                    sourceFile = os.path.split(srcFont.path)[-1]
                    glyphNameExtension = os.path.splitext(sourceFile)[0]
                    tmpGlyphName = f'{glyphName}.{glyphNameExtension}'

                    # import source glyph into temp font
                    if glyphName in srcFont:
                        print(f'\timporting {glyphName} from {ufoName}...')
                        srcGlyph = srcFont[glyphName]
                    else:
                        print(f'\tcreating {glyphName} for {ufoName}...')
                        srcGlyph = self.defaultFont[glyphName]

                    tmpFont.newGlyph(tmpGlyphName)
                    tmpFont[tmpGlyphName].appendGlyph(srcGlyph)
                    tmpFont[tmpGlyphName].width = srcGlyph.width
                    tmpFont[tmpGlyphName].unicodes = srcGlyph.unicodes
                    tmpFont.changed()

                    # store the import mode in the font lib
                    tmpFont.lib[tempEditModeKey] = 'glyphs'

                    # store path to glyphset in the glyph lib
                    tmpFont[tmpGlyphName].lib[glyphSetPathKey] = glyphsFolder
                    # also in the background layer (in case we switch layers)
                    tmpFont[tmpGlyphName].getLayer('background').lib[glyphSetPathKey] = glyphsFolder

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

            srcGlyphName = glyphName[:glyphName.rfind('.')]
            glyphsFolder = glyph.lib[glyphSetPathKey]
            ufoName = splitall(glyphsFolder)[-2]

            defaultGlyph = self.defaultFont[srcGlyphName]
            validationGroup = assignValidationGroup(glyph, defaultGlyph)
            if validationGroup == 'contoursEqual':
                print(f'\tskipping {srcGlyphName} in {ufoName} (same as default)...')
                continue

            print(f'\texporting {srcGlyphName} to {ufoName}...')
            glyphSet = GlyphSet(glyphsFolder, validateWrite=True)
            glyphSet.writeGlyph(srcGlyphName, glyph.naked(), glyph.drawPoints)
            glyphSet.writeContents()

        print('\n...done!\n')

    def reloadButtonCallback(self, sender):
        self._loadDesignspace()

    def duovarsCallback(self, sender):
        self._updateTuningSources()

    def trivarsCallback(self, sender):
        self._updateTuningSources()

    def quadvarsCallback(self, sender):
        self._updateTuningSources()

    def _updateTuningSources(self):
        pass
        # glyphName = self.w.getItem("glyphSelector").getItem()
        # duovars   = self.w.getItem("duovars").get()
        # trivars   = self.w.getItem("trivars").get()
        # quadvars  = self.w.getItem("quadvars").get()

        # tuningSources = []
        # for styleName, src in self.tuningSources.items():
        #     styleNameParts = styleName.split('_')
        #     if len(styleNameParts) == 1 and not duovars:
        #         continue
        #     elif len(styleNameParts) == 2 and not trivars:
        #         continue
        #     elif len(styleNameParts) == 3 and not quadvars:
        #         continue

        #     if glyphName in src:
        #         tuningSources.append(styleName)

        # glyphTuningTable = self.w.getItem("axesList")
        # glyphTuningTable.set(sorted(tuningSources))
        # glyphTuningTable.setSelectedIndexes(range(len(tuningSources)))


if __name__ == '__main__':

    OpenWindow(GlyphTuningController)

