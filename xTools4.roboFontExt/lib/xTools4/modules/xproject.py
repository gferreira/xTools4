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

    def __init__(self, folder, familyName):
        self.baseFolder = folder
        self.familyName = familyName

    # sources

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Sources')

    @property
    def sources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultSource(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}_{self.defaultName}.ufo')

    # designspace

    @property
    def designspaceFileName(self):
        return f'{self.familyName}.designspace'

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceFileName)

    @property
    def defaultLocation(self):
        # L = { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }
        # L['GRAD'] = 0
        return L

    # measurements

    @property
    def measurementsFileName(self):
        return 'measurements.json'

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, self.measurementsFileName)

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

    # setSourceNamesFromMeasurements
    # cleanupNormalizeSources



