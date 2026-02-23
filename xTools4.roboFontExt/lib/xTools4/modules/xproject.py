import os, glob

# WARNING: THIS IS A WORK-IN-PROGRESS DRAFT, NOT USABLE YET!

measurementsPathKey       = 'com.xTools4.xProject.measurementsPath'
smartSetsPathKey          = 'com.xTools4.xProject.smartSetsPath'
glyphConstructionsPathKey = 'com.xTools4.xProject.glyphConstructionsPath'

class xProject:
    '''
    This object represents the source files of a parametric avar2 variable font.

    - smart sets
    - glyph constructions
    - features
    - measurements
    - blends
    - fences?

    Example:

    p = xProject(folder, 'AmstelvarA2')
    p.buildBlends()
    p.buildDesignspace()
    p.buildVariableFont()
    p.buildInstancesUFO()
    p.buildInstancesTTF()

    '''

    defaultName    = 'wght400'
    parametricAxes = []

    def __init__(self, folder, familyName, subFamilyName=None):
        self.baseFolder = folder
        self.familyName = familyName
        self.subFamilyName = subFamilyName

    # designspace

    @property
    def designspaceFileName(self):
        fileName = self.familyName.replace(' ', '') 
        if self.subFamilyName:
            fileName += f'-{self.subFamilyName.replace(' ', '') }'
        return f'{fileName}.designspace'

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceFileName)

    @property
    def defaultLocation(self):
        # L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        # L['GRAD'] = 0
        # return L
        pass

    # parametric sources

    @property
    def sourcesFolder(self):
        folder = os.path.join(self.baseFolder, 'Sources')
        if self.subFamilyName:
            folder = os.path.join(folder, self.subFamilyName.replace(' ', ''))
        return folder

    @property
    def sources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultSource(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}_{self.defaultName}.ufo')

    # measurements

    @property
    def measurementsFileName(self):
        return 'measurements.json'

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, self.measurementsFileName)

    # data files

    @property
    def smartSetsPath(self):
        pass

    @property
    def glyphConstructionsPath(self):
        pass

    # blending

    @property
    def blendsFileName(self):
        return 'blends.json'

    @property
    def blendsPath(self):
        return os.path.join(self.sourcesFolder, self.blendsFileName)

    @property
    def blendedAxes(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['axes']

    @property
    def blendedSources(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['sources']

    # tuning

    @property
    def tuningSourcesFolder(self):
        pass

    @property
    def tuningSources(self):
        pass

    # instances

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    # variable font

    @property
    def fontsFolder(self):
        return os.path.join(self.baseFolder, 'Fonts')

    @property
    def varFontPath(self):
        return os.path.join(self.fontsFolder, f'{self.familyName}.ttf')

    # -------
    # methods
    # -------

    def addParametricAxes(self):
        pass

    def addParametricSources(self):
        pass

    def addDefaultSource(self):
        pass

    def addTuningAxes(self, duovars=True, trivars=True, quadvars=True):
        pass

    def addTuningSources(self):
        pass

    def addInstances(self):
        pass

    def addBlendedAxes(self):
        pass

    def buildBlendsFile(self):
        pass

    def patchBlendsFile(self):
        pass

    def addMappings(self):
        pass

    def save(self):
        pass

    def setSourceNamesFromMeasurements(self):
        pass

    def cleanupNormalizeSources(self):
        pass

    def buildInstances(self, clear=True):
        pass

    def buildVariableFont(self, subset=None, setVersionInfo=True, debug=False, fixGDEF=False, removeMarkFeature=False):
        pass

    def buildInstancesVariableFont(self, clear=True, ufo=False):
        pass

    def printAxes(self):
        pass

    def build(self, patchBlends=False, tuneDuovars=False, tuneTrivars=False, tuneQuadvars=False):

        self.buildBlendsFile()
        if patchBlends:
            self.patchBlendsFile()

        self.designspace = DesignSpaceDocument()

        self.addBlendedAxes()
        self.addParametricAxes()
        self.addCornerTuningAxes(duovars=tuneDuovars, trivars=tuneTrivars, quadvars=tuneQuadvars)
        self.addMappings()
        self.addDefaultSource()
        self.addParametricSources()
        self.addCornerTuningSources()
        # self.addInstances()

        self.save()

