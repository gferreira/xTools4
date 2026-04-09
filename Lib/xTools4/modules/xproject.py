from importlib import reload
import xTools4.modules.measurements
reload(xTools4.modules.measurements)
import xTools4.modules.normalization
reload(xTools4.modules.normalization)

import os, glob, json, shutil
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from fontParts.world import OpenFont
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.measurements import FontMeasurements, permille, setSourceNamesFromMeasurements
from xTools4.modules.normalization import cleanupSources, normalizeSources


measurementsPathKey       = 'com.xTools4.xProject.measurementsPath'
smartSetsPathKey          = 'com.xTools4.xProject.smartSetsPath'
glyphConstructionsPathKey = 'com.xTools4.xProject.glyphConstructionsPath'
referenceFontPathKey      = 'com.xTools4.xProject.referenceFontPath'


class xProject:
    '''
    A base object to control the source files of a parametric avar2 variable font.

    '''

    verbose = True

    #: A list of parametric axes (4-letter names).
    parametricAxes = []

    #: A switch to make parametric axes hidden (or not).
    parametricAxesHidden = True

    def __init__(self, folder, familyName):
        self.baseFolder = folder
        self.familyName = familyName

    #==========
    # SETTINGS
    #==========

    #: The name of the project settings file.
    settingsFile = 'xproject.json'

    @property
    def settingsPath(self):
        '''Returns the full path of the settings file.'''
        return os.path.join(self.baseFolder, self.settingsFile)

    # -----------
    # designspace
    # -----------

    @property
    def designspaceFile(self):
        '''Returns the name of the designspace file.'''
        return f'{self.familyName.replace(' ', '') }.designspace'

    @property
    def designspacePath(self):
        '''Returns the full path of the designspace file.'''
        return os.path.join(self.sourcesFolder, self.designspaceFile)

    # ------------------
    # parametric sources
    # ------------------

    #: The name of the sources folder.
    sourcesFolderName = 'Sources'

    @property
    def sourcesFolder(self):
        '''Returns the full path of the sources folder.'''
        folder = os.path.join(self.baseFolder, self.sourcesFolderName)
        return folder

    @property
    def sourcesPaths(self):
        '''Returns a list with the full paths of all (parametric) UFO sources.'''
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    # -------
    # default
    # -------

    #: The name of the default source.
    defaultName = 'wght400'

    @property
    def defaultSourcePath(self):
        '''Returns the full path of the default source.'''
        return os.path.join(self.sourcesFolder, f"{self.familyName.replace(' ', '')}_{self.defaultName}.ufo")

    @property
    def defaultLocation(self):
        '''Returns the (parametric) location of the default source.'''
        if not self.measurementsDefault:
            return
        return { name: permille(self.measurementsDefault.values[name], self.defaultFont.info.unitsPerEm) for name in self.parametricAxes }

    @property
    def defaultFont(self):
        return OpenFont(self.defaultSourcePath, showInterface=False)

    # ------------
    # measurements
    # ------------

    #: The name of the measurements file.
    measurementsFile = 'measurements.json'

    @property
    def measurementsPath(self):
        '''Returns the full path of the measurements file.'''
        return os.path.join(self.sourcesFolder, self.measurementsFile)

    @property
    def measurements(self):
        '''Returns the imported measurements as a dictionary.'''
        if self.measurementsPath is None or not os.path.exists(self.measurementsPath):
            return {}
        else:
            return readMeasurements(self.measurementsPath)

    @property
    def measurementsDefault(self):
        if not os.path.exists(self.measurementsPath):
            return
        measurements = FontMeasurements()
        measurements.read(self.measurementsPath)
        measurements.measure(self.defaultFont)
        return measurements

    # ----------
    # smart sets
    # ----------

    @property
    def smartSetsFile(self):
        '''Returns the name of the smart sets file.'''
        return self.designspaceFile.replace('.designspace', '.roboFontSets')

    @property
    def smartSetsPath(self):
        '''Returns the full path of the smart sets file.'''
        return os.path.join(self.sourcesFolder, self.smartSetsFile)

    @property
    def smartSets(self):
        '''Returns the imported smart sets as a dictionary.'''
        return {}

    # ------------------
    # glyph construction
    # ------------------

    @property
    def glyphConstructionsFile(self):
        '''Returns the name of the glyph construction file.'''
        return self.designspaceFile.replace('.designspace', '.glyphConstruction')

    @property
    def glyphConstructionsPath(self):
        '''Returns the full path of the glyph construction file.'''
        return os.path.join(self.sourcesFolder, self.glyphConstructionsFile)

    @property
    def glyphConstructions(self):
        '''Returns the imported glyph constructions as a dictionary.'''
        pass

    # --------
    # blending
    # --------

    #: The name of the blends file.
    blendsFile = 'blends.json'

    @property
    def blendsPath(self):
        '''Returns the full path of the blends file.'''
        return os.path.join(self.sourcesFolder, self.blendsFile)

    @property
    def blendedAxes(self):
        '''Returns the imported blended axes as a dictionary.'''
        if not os.path.exists(self.blendsPath):
            return {}
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['axes']

    @property
    def blendedSources(self):
        '''Returns the imported blended sources as a dictionary.'''
        if not os.path.exists(self.blendsPath):
            return {}
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['sources']

    # ------
    # tuning
    # ------

    #: The name of the tuning folder.
    tuningSourcerFolderName = 'corners'

    @property
    def tuningSourcesFolder(self):
        '''Returns the full path of the tuning sources (sub)folder.'''
        return os.path.join(self.sourcesFolder, self.tuningSourcerFolderName)

    @property
    def tuningSourcesPaths(self):
        '''Returns a list with the full paths of all tuning UFO sources.'''
        return glob.glob(f'{self.tuningSourcesFolder}/*.ufo')

    # ---------
    # instances
    # ---------

    #: The name of the instances folder.
    instancesFolderName = 'instances'

    @property
    def instancesFolder(self):
        '''Returns the full path of the UFO instances folder.'''
        return os.path.join(self.sourcesFolder, self.instancesFolderName)

    # --------------
    # variable fonts
    # --------------

    #: The name of the fonts folder.
    fontsFolderName = 'Fonts'

    @property
    def fontsFolder(self):
        '''Returns the full path of the (binary) fonts folder.'''
        return os.path.join(self.baseFolder, self.fontsFolderName)

    @property
    def varFontFile(self):
        '''Returns the name of the variable font file.'''
        return self.designspaceFile.replace('.designspace', '.ttf')

    @property
    def varFontPath(self):
        '''Returns the full path of the variable font file.'''
        return os.path.join(self.fontsFolder, self.varFontFile)

    #=========
    # METHODS
    #=========

    def setSourceNamesFromMeasurements(self, preflight=True, ignoreTags=['wght']):
        '''Set source names from the actual measurement value in each source.'''
        setSourceNamesFromMeasurements(
                self.sourcesFolder,
                self.familyName,
                self.measurementsPath,
                preflight=preflight,
                ignoreTags=ignoreTags,
        )

    def createParametricSources(self, parameters, minSource=True, maxSource=True):
        '''Create fresh min/max sources for parametric axes from default.'''
        for parameter in parameters:
            if minSource:
                minSourcePath = self.defaultSourcePath.replace(self.defaultName, f'{parameter}min')
                if os.path.exists(minSourcePath):
                    if self.verbose:
                        print(f'{os.path.split(minSourcePath)[-1]} already exists, skipping…')
                else:
                    shutil.copytree(self.defaultSourcePath, minSourcePath)
            if maxSource:
                maxSourcePath = self.defaultSourcePath.replace(self.defaultName, f'{parameter}max')
                if os.path.exists(maxSourcePath):
                    if self.verbose:
                        print(f'{os.path.split(minSourcePath)[-1]} already exists, skipping…')
                else:
                    shutil.copytree(self.defaultSourcePath, maxSourcePath)

    def createMeasurementsFile(self):
        '''Create a fresh measurements file.'''
        if self.verbose:
            print('creating measurements file...')
        measurements = {
            'font'   : {},
            'glyphs' : {},
        }
        if os.path.exists(self.measurementsPath):
            print(f'{self.measurementsPath} already exists.\n')
            return
        with open(self.measurementsPath, 'w', encoding='utf-8') as f:
            json.dump(measurements, f, indent=2)

    def createSmartSetsFile(self):
        '''Create a fresh smart sets file.'''
        if self.verbose:
            print('creating smart sets file...')
        if os.path.exists(self.smartSetsPath):
            print(f'{self.smartSetsPath} already exists.\n')
            return
        with open(self.smartSetsPath, 'w') as f:
            pass

    def createGlyphConstructionFile(self):
        '''Create a fresh glyph construction file.'''
        if self.verbose:
            print('creating glyph construction file...')
        if os.path.exists(self.glyphConstructionsPath):
            print(f'{self.glyphConstructionsPath} already exists.\n')
            return
        with open(self.glyphConstructionsPath, 'w') as f:
            pass

    # designspace

    def addParametricAxes(self):
        '''Add parametric axes to the designspace.'''

        if self.verbose:
            print('\tadding parametric axes...')

        for name in self.parametricAxes:

            # get default value
            defaultValue = permille(self.measurementsDefault.values[name], self.defaultFont.info.unitsPerEm)

            # get min/max values from file names
            values = []
            for ufo in self.sourcesPaths:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            if len(values) == 2:
                values.sort()
                minValue, maxValue = values
            elif len(values) == 1:
                values.append(defaultValue)
                values.sort()
                minValue, maxValue = values
            else:
                print(f'ERROR: {name}: {values}')
                continue

            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = minValue
            a.maximum = maxValue
            a.default = defaultValue
            a.hidden  = self.parametricAxesHidden

            self.designspace.addAxis(a)

    def addParametricSources(self):
        '''Add parametric sources to the designspace.'''
        if self.verbose:
            print('\tadding parametric sources...')

        for name in self.parametricAxes:
            for ufoPath in self.sourcesPaths:
                if name in ufoPath:
                    src = SourceDescriptor()
                    src.path = ufoPath
                    src.familyName = self.familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addDefaultSource(self):
        '''Add the default source to the designspace.'''

        if not self.designspace:
            return

        src = SourceDescriptor()
        src.path       = self.defaultSourcePath
        src.familyName = self.familyName
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation

        self.designspace.addSource(src)

    def addTuningAxes(self):
        '''Add tuning axes to the designspace.'''
        pass

    def addTuningSources(self):
        '''Add tuning sources to the designspace.'''
        pass

    def addInstances(self):
        '''Add instances to the designspace.'''
        pass

    def addBlendedAxes(self):
        '''Add blended axes to the designspace.'''
        if self.verbose:
            print('\tadding blended axes...')

        for tag in self.blendedAxes.keys():
            a = AxisDescriptor()
            a.name    = self.blendedAxes[tag]['name']
            a.tag     = tag
            a.minimum = self.blendedAxes[tag]['minimum']
            a.maximum = self.blendedAxes[tag]['maximum']
            a.default = self.blendedAxes[tag]['default']
            # if tag == 'opsz':
            #     a.map = self.opszMapping
            self.designspace.addAxis(a)

    def addBlendedSources(self):
        '''Add blended sources (mappings) to the designspace.'''

        blendedAxes    = self.blendedAxes
        blendedSources = self.blendedSources

        if self.verbose:
            print('\tadding blend mappings...')

        for styleName in blendedSources.keys():
            m = AxisMappingDescriptor()

            # get input value from style name
            inputLocation = {}
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                axisName  = blendedAxes[tag]['name']
                inputLocation[axisName] = value

            # get output value from blends.json file
            outputLocation = {}
            for axisName in blendedSources[styleName]:
                outputLocation[axisName] = int(blendedSources[styleName][axisName])

            # # set value for corner tuning axes
            # if styleName in self.cornerTuningAxes:
            #     axisTag = self.cornerTuningAxes[styleName]
            #     outputLocation[axisTag] = 100

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation
            m.description    = styleName

            self.designspace.addAxisMapping(m)

    # building

    def buildBlendsFile(self):
        pass

    def buildDesignspace(self, tuning=False, instances=False):

        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.designspace = DesignSpaceDocument()

        self.addBlendedAxes()
        self.addParametricAxes()

        if tuning:
            self.addTuningAxes()

        self.addBlendedSources()
        self.addDefaultSource()
        self.addParametricSources()

        if tuning:
            self.addTuningSources()

        if instances:
            self.addInstances()

        self.addCustomKeysToLib()

        self.save()

    def buildInstances(self, clear=True):
        pass

    def buildVariableFont(self, subset=None, setVersionInfo=True, debug=False):
        pass

    def buildInstancesVariableFont(self, clear=True, ufo=False):
        pass

    # saving

    def cleanupSources(self, parametric=True, tuning=True, clearFontLibs=True, clearGlyphLibs=True, clearFontGuides=True, clearGlyphGuides=True, clearMarks=True, clearLayers=True, preflight=False):
        '''Remove unnecessary data from UFO sources.'''

        # delete all font libs except these:
        ignoreFontLibs = [
            'com.typemytype.robofont.italicSlantOffset',
            'com.typemytype.robofont.segmentType',
        ]

        # delete all layers except these:
        ignoreLayers = [
            'foreground',
            'background',
        ]

        if parametric:
            cleanupSources(self.sourcesFolder,
                    clearFontLibs=clearFontLibs,
                    clearGlyphLibs=clearGlyphLibs,
                    clearFontGuides=clearFontGuides,
                    clearGlyphGuides=clearGlyphGuides,
                    clearMarks=clearMarks,
                    clearLayers=clearLayers,
                    preflight=preflight,
                    ignoreFontLibs=ignoreFontLibs,
                    ignoreLayers=ignoreLayers,
                    # verbose=self.verbose
                )

        if tuning:
            cleanupSources(self.tuningSourcesFolder,
                    clearFontLibs=clearFontLibs,
                    clearGlyphLibs=clearGlyphLibs,
                    clearFontGuides=clearFontGuides,
                    clearGlyphGuides=clearGlyphGuides,
                    clearMarks=clearMarks,
                    clearLayers=clearLayers,
                    preflight=preflight,
                    ignoreFontLibs=ignoreFontLibs,
                    ignoreLayers=ignoreLayers,
                    # verbose=self.verbose
                )

    def normalizeSources(self, parametric=True, tuning=True):
        '''Normalize UFO sources.'''

        if parametric:
            normalizeSources(self.sourcesFolder, onlyModified=False, writeModTimes=False, verbose=self.verbose)

        if tuning:
            normalizeSources(self.tuningSourcesFolder, onlyModified=False, writeModTimes=False, verbose=self.verbose)

    def addCustomKeysToLib(self):

        if os.path.exists(self.smartSetsPath):
            self.designspace.lib[smartSetsPathKey] = os.path.split(self.smartSetsPath)[-1]

        if os.path.exists(self.measurementsPath):
            self.designspace.lib[measurementsPathKey] = os.path.split(self.measurementsPath)[-1]

        if os.path.exists(self.glyphConstructionsPath):
            self.designspace.lib[glyphConstructionsPathKey] = os.path.split(self.glyphConstructionsPath)[-1]

    def save(self):
        if not self.designspace:
            return

        if self.verbose:
            print(f'saving designspace...', end=' ')

        self.designspace.write(self.designspacePath)
        if self.verbose:
            print(os.path.exists(self.designspacePath))
            print()

    # project info

    def printAxes(self):
        pass

    def printSettings(self):
        txt  = f'base folder: {self.baseFolder}\n'
        txt += f'family name: {self.familyName}\n\n'
        # txt += f'settings file: {self.settingsFile}\n'
        # txt += f'settings path: {self.settingsPath} ({os.path.exists(self.settingsPath)})\n\n'

        txt += f'designspace file: {self.designspaceFile}\n'
        txt += f'designspace path: {self.designspacePath} ({os.path.exists(self.designspacePath)})\n\n'

        txt += f'sources folder name: {self.sourcesFolderName}\n'
        txt += f'sources folder path: {self.sourcesFolder} ({os.path.exists(self.sourcesFolder)})\n\n'
        # txt += f'sources paths: {self.sourcesPaths}\n\n'

        txt += f'default name: {self.defaultName}\n'
        txt += f'default path: {self.defaultSourcePath} ({os.path.exists(self.defaultSourcePath)})\n'
        txt += f'default location: {self.defaultLocation}\n\n'

        txt += f'measurements file: {self.measurementsFile}\n'
        txt += f'measurements path: {self.measurementsPath} ({os.path.exists(self.measurementsPath)})\n\n'
        # txt += f'measurements data: {self.measurements}\n\n'

        txt += f'smart sets file: {self.smartSetsFile}\n'
        txt += f'smart sets path: {self.smartSetsPath} ({os.path.exists(self.smartSetsPath)})\n\n'
        # txt += f'smart sets data: {self.smartSets}\n\n'

        txt += f'blends file: {self.blendsFile}\n'
        txt += f'blends path: {self.blendsPath} ({os.path.exists(self.blendsPath)})\n'
        txt += f'blended axes: {self.blendedAxes.keys()}\n'
        txt += f'blended sources: {self.blendedSources.keys()}\n\n'

        txt += f'tuning folder name: {self.tuningSourcerFolderName}\n'
        txt += f'tuning folder path: {self.tuningSourcesFolder} ({os.path.exists(self.tuningSourcesFolder)})\n\n'
        # txt += f'tuning sources paths: {self.tuningSourcesPaths}\n\n'

        txt += f'instances folder name: {self.instancesFolderName}\n'
        txt += f'instances folder path: {self.instancesFolder} ({os.path.exists(self.instancesFolder)})\n\n'

        txt += f'fonts folder name: {self.fontsFolderName}\n'
        txt += f'fonts folder: {self.fontsFolder} ({os.path.exists(self.fontsFolder)})\n\n'
        txt += f'variable font file: {self.varFontFile}\n'
        txt += f'variable font path: {self.varFontPath} ({os.path.exists(self.varFontPath)})\n\n'

        print(txt)










