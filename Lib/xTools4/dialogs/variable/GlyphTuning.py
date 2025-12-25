import os, glob
import ezui
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, NewFont, OpenFont, CurrentFont
from mojo.smartSet import readSmartSets
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import GlyphSet
from xTools4.modules.xproject import measurementsPathKey, smartSetsPathKey
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

    | | @glyphTuning

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
            size=(123, 400),
            minSize=(123, 300),
            maxSize=(123*3, 960),
        )
        self.w.workspaceWindowIdentifier = "GlyphTuning"
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem("glyphTuning").getNSTableView().setRowHeight_(17)
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

        self._loadTuningSources()
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

    def _loadTuningSources(self):
        if self.verbose:
            print(f'loading tuning sources... ', end='')

        sources = glob.glob(f'{self.tuningSourcesFolder}/*.ufo')
        for srcPath in sources:
            styleName = os.path.splitext(os.path.split(srcPath)[-1])[0]
            self.tuningSources[styleName] = OpenFont(srcPath, showInterface=False)

    def getDesignspaceButtonCallback(self, sender):
        self.designspacePath = GetFile(message='Select designspace file:', title=self.title)
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
        selectedTuningSources = self.w.getItem("glyphTuning").getSelectedItems()
        print(selectedTuningSources)

        # create temp font
        tmpFont = NewFont(familyName='tempEdit')
        setupNewFont(tmpFont)
        tmpFont.info.familyName  = f'{self.familyName}'
        tmpFont.info.styleName   = glyphName

        print('opening glyphs...\n')

        for i, styleName in enumerate(selectedTuningSources):
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
            print(f'\timporting {glyphName} from {ufoName}...')
            srcGlyph = srcFont[glyphName]
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

            glyphsFolder = glyph.lib[glyphSetPathKey]
            srcGlyphName = glyphName[:glyphName.rfind('.')]
            ufoName = splitall(glyphsFolder)[-2]

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
        glyphName = self.w.getItem("glyphSelector").getItem()
        duovars   = self.w.getItem("duovars").get()
        trivars   = self.w.getItem("trivars").get()
        quadvars  = self.w.getItem("quadvars").get()

        tuningSources = []
        for styleName, src in self.tuningSources.items():
            styleNameParts = styleName.split('_')
            if len(styleNameParts) == 1 and not duovars:
                continue
            elif len(styleNameParts) == 2 and not trivars:
                continue
            elif len(styleNameParts) == 3 and not quadvars:
                continue

            if glyphName in src:
                tuningSources.append(styleName)

        glyphTuningTable = self.w.getItem("glyphTuning")
        glyphTuningTable.set(sorted(tuningSources))
        glyphTuningTable.setSelectedIndexes(range(len(tuningSources)))


if __name__ == '__main__':

    OpenWindow(GlyphTuningController)

