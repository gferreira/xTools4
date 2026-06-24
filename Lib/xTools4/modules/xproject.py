from importlib import reload
import xTools4.modules.glyphMemeProofer
reload(xTools4.modules.glyphMemeProofer)
import xTools4.modules.tuningPreview
reload(xTools4.modules.tuningPreview)
import xTools4.modules.measurements
reload(xTools4.modules.measurements)
import xTools4.modules.xprojectLib
reload(xTools4.modules.xprojectLib)

import os, glob, json, shutil, time, datetime
import subprocess
from functools import cached_property
from xml.etree.ElementTree import parse
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from defcon import Font
from mojo.roboFont import OpenFont, RGlyph
from mojo.smartSet import readSmartSets
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.measurements import *
from xTools4.modules.normalization import cleanupSources, normalizeSources
from xTools4.modules.validation import validateDesignspace, validateFonts
from xTools4.modules.ttx import ttf2ttx, ttx2ttf
from xTools4.modules.xprojectLib import *
from xTools4.modules.glyphMemeProofer import GlyphMemeProofer
from xTools4.modules.glyphSetProofer import GlyphSetProofer
from xTools4.modules.blendsPreview import BlendsPreview, getEffectiveLocation, instantiateGlyph
from xTools4.modules.tuningPreview import TuningPreview


class xProject:
    '''
    A base object to control the source files of a parametric avar2 variable font.

    '''

    verbose = True
    '''Enable/disable console output.'''

    def __init__(self, folder, familyName):
        self.baseFolder = folder
        self.familyName = familyName

    #----------
    # SETTINGS
    #----------

    settingsFile = 'xproject.json'
    '''The name of the project settings file.'''

    @property
    def settingsPath(self):
        '''Returns the full path of the settings file.'''
        return os.path.join(self.baseFolder, self.settingsFile)

    # designspace

    @property
    def designspaceFile(self):
        '''Returns the name of the designspace file.'''
        return f'{self.familyName.replace(' ', '') }.designspace'

    @property
    def designspacePath(self):
        '''Returns the full path of the designspace file.'''
        return os.path.join(self.sourcesFolder, self.designspaceFile)

    designspace = None
    '''Returns a fontTools designspace object (after building).'''

    # parametric sources

    parametricAxes = []
    '''A list of parametric axes as 4-letter tags.'''

    parametricAxesHidden = True
    '''A switch to make parametric axes hidden (or not).'''

    sourcesFolderName = 'Sources'
    '''The name of the sources folder.'''

    @property
    def sourcesFolder(self):
        '''Returns the full path of the sources folder.'''
        folder = os.path.join(self.baseFolder, self.sourcesFolderName)
        return folder

    @cached_property
    def sourcesPaths(self):
        '''Returns a list with the full paths of all parametric UFO sources.'''
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def sources(self):
        '''Returns a dict of tuning locations (keys) and their UFO sources (values).'''
        return { os.path.splitext(os.path.split(ufo)[-1])[0] : ufo for ufo in self.sourcesPaths }

    # default

    defaultName = 'wght400'
    '''The name of the default source.'''

    @property
    def defaultSourcePath(self):
        '''Returns the full path of the default source.'''
        return os.path.join(self.sourcesFolder, f"{self.familyName.replace(' ', '')}_{self.defaultName}.ufo")

    @property
    def defaultLocation(self):
        '''Returns the parametric location of the default source.'''
        if not self.measurementsDefault:
            return

        # get parametric measurements
        L = {}
        for name in self.parametricAxes:
            if name in self.measurementsDefault.values:
                L[name] = permille(self.measurementsDefault.values[name], self.defaultFont.info.unitsPerEm)

        # add tuning axes
        if self.tuning:
            for styleName, axis in self.tuningAxes.items():
                L[axis.tag] = axis.default

        return L

    @cached_property
    def defaultFont(self):
        '''Returns an RFont object of the default font (cached).'''
        return OpenFont(self.defaultSourcePath, showInterface=False)

    # measurements

    measurementsFile = 'measurements.json'
    '''The name of the measurements file.'''

    @property
    def measurementsPath(self):
        '''Returns the full path of the measurements file.'''
        return os.path.join(self.sourcesFolder, self.measurementsFile)

    @cached_property
    def measurements(self):
        '''Returns the imported measurements as a dictionary.'''
        if self.measurementsPath is None or not os.path.exists(self.measurementsPath):
            return {}
        else:
            return readMeasurements(self.measurementsPath)

    @cached_property
    def measurementsDefault(self):
        '''Returns a dictionary with measurements of the default source.'''
        if not os.path.exists(self.measurementsPath):
            return
        measurements = FontMeasurements()
        measurements.read(self.measurementsPath)
        measurements.measure(self.defaultFont)
        return measurements

    # smart sets

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
        '''Returns the imported smart sets as a two-level dictionary (cases > groups).'''
        smartSetsRaw = readSmartSets(self.smartSetsPath, useAsDefault=False, font=None)

        smartSets = {}
        for smartGroup in smartSetsRaw:
            # skip empty folders
            if not smartGroup.groups:
                continue
            smartSets[smartGroup.name] = {}
            for smartSet in smartGroup.groups:
                smartSets[smartGroup.name][smartSet.name] = smartSet.glyphNames

        return smartSets

    # glyph construction

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

    # blending

    blendsFile = 'blends.json'
    '''The name of the blends file.'''

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

    # tuning

    tuning = False
    '''Enable/disable tuning (optional, disabled by default).'''

    tuningLevels = [1, 2, 3] # 1: duovars / 2: trivars / 3: quadvars
    '''The level(s) of tuning to include in the designspace.'''

    tuningSourcesFolderName = 'tuning'
    '''The name of the tuning folder.'''

    tuningAxesHidden = True
    '''A switch to make tuning axes hidden (or not).'''

    @property
    def tuningSourcesFolder(self):
        '''Returns the full path of the tuning sources subfolder.'''
        return os.path.join(self.sourcesFolder, self.tuningSourcesFolderName)

    @property
    def tuningSourcesPaths(self):
        '''Returns a list with the full paths of all tuning UFO sources.'''
        return glob.glob(f'{self.tuningSourcesFolder}/*.ufo')

    @property
    def tuningSources(self):
        '''Returns a dict of tuning locations (keys) and their UFO sources (values).'''
        return { os.path.splitext(os.path.split(ufo)[-1])[0] : ufo for ufo in self.tuningSourcesPaths }

    @property
    def tuningAxes(self):
        '''A dict of blended location names (keys) and tuning axes (values).'''

        tuningAxes = {}

        for i, styleName in enumerate(sorted(self.tuningSources)):
            ufo = self.tuningSources[styleName]

            styleNameParts = styleName.split('_')
            if len(styleNameParts) not in self.tuningLevels:
                continue

            axisTag = f'TN{i:02}'

            a = AxisDescriptor()
            a.name    = axisTag # styleName
            a.tag     = axisTag
            a.minimum = 0
            a.maximum = 100
            a.default = 0
            a.hidden  = self.tuningAxesHidden
            tuningAxes[styleName] = a

        return tuningAxes

    # reference

    referenceSourcesFolderName = 'reference'
    '''The name of the reference folder.'''

    @property
    def referenceSourcesFolder(self):
        '''Returns the full path of the reference sources subfolder.'''
        return os.path.join(self.sourcesFolder, self.referenceSourcesFolderName)

    @property
    def referenceSourcesPaths(self):
        '''Returns a list with the full paths of all reference UFO sources.'''
        return { os.path.splitext(os.path.split(f)[-1])[0]: f for f in glob.glob(f'{self.referenceSourcesFolder}/*.ufo')}

    @property
    def referenceBlendsPath(self):
        '''Returns the full path of the blends file for reference sources.'''
        return os.path.join(self.referenceSourcesFolder, self.blendsFile)

    @property
    def referenceFontName(self):
        '''The name of the reference font file.'''
        return os.path.split(self.varFontFile)[-1]

    @property
    def referenceFontPath(self):
        '''Returns the full path of the reference variable font file.'''
        return os.path.join(self.referenceSourcesFolder, self.referenceFontName)

    # instances

    instancesFolderName = 'instances'
    '''The name of the instances folder.'''

    @property
    def instancesFolder(self):
        '''Returns the full path of the UFO instances folder.'''
        return os.path.join(self.sourcesFolder, self.instancesFolderName)

    # variable fonts

    fontsFolderName = 'Fonts'
    '''The name of the fonts folder.'''

    @property
    def fontsFolder(self):
        '''Returns the full path of the binary fonts folder.'''
        return os.path.join(self.baseFolder, self.fontsFolderName)

    @property
    def varFontFile(self):
        '''Returns the name of the variable font file.'''
        return self.designspaceFile.replace('.designspace', '.ttf')

    @property
    def varFontPath(self):
        '''Returns the full path of the variable font file.'''
        return os.path.join(self.fontsFolder, self.varFontFile)

    # proofs

    proofsFolderName = 'Proofs'
    '''The name of the proofs folder.'''

    @property
    def proofsFolder(self):
        '''Returns the full path of the proofs folder.'''
        return os.path.join(self.baseFolder, self.proofsFolderName)

    #---------
    # METHODS
    #---------

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
        if self.verbose:
            print(f'creating parametric sources...')

        for parameter in parameters:
            if minSource:
                minSourcePath = self.defaultSourcePath.replace(self.defaultName, f'{parameter}min')
                if self.verbose:
                    print(f'\tcreating {os.path.split(minSourcePath)[-1]}...')
                if os.path.exists(minSourcePath):
                    if self.verbose:
                        print(f'\t{os.path.split(minSourcePath)[-1]} already exists, skipping...')
                else:
                    shutil.copytree(self.defaultSourcePath, minSourcePath)
            if maxSource:
                maxSourcePath = self.defaultSourcePath.replace(self.defaultName, f'{parameter}max')
                if self.verbose:
                    print(f'\tcreating {os.path.split(maxSourcePath)[-1]}...')
                if os.path.exists(maxSourcePath):
                    if self.verbose:
                        print(f'\t{os.path.split(minSourcePath)[-1]} already exists, skipping...')
                else:
                    shutil.copytree(self.defaultSourcePath, maxSourcePath)

        if self.verbose:
            print(f'...done.\n')

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
            # add boilerplate smart sets
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

    def updateGlyphsFromDefault(self, glyphNames, oldDefaultPath, preflight=True, parametricSources=True, tuningSources=False):
        '''Update default glyphs in all sources.'''
        ufoPaths = []
        if parametricSources:
            ufoPaths += self.sourcesPaths
        if tuningSources:
            ufoPaths += self.tuningSourcesPaths
        batchUpdateGlyphsFromDefault(glyphNames, ufoPaths, self.defaultSourcePath, oldDefaultPath, preflight=preflight)

    def copyGlyphsFromDefault(self, glyphNames, sourceNames=None):
        '''Copy glyphs from the default source to other sources.'''
        pass

    def copyGroupsFromDefault(self):
        '''Copy groups from the default source to other sources.'''

        srcFont = OpenFont(self.defaultSourcePath, showInterface=False)

        print(f'copying groups from the default to all other sources...')

        for dstPath in self.sourcesPaths:
            if dstPath == self.defaultSourcePath:
                continue

            print(f'\tcopying groups to {os.path.split(dstPath)[-1]}...')
            dstFont = OpenFont(dstPath, showInterface=False)
            dstFont.groups.clear()
            dstFont.groups.update(srcFont.groups)
            dstFont.save()

        print('...done!\n')

    def copyKerningFromDefault(self):
        '''Copy glyphs from the default source to other sources.'''

        srcFont = OpenFont(self.defaultSourcePath, showInterface=False)

        print(f'copying kerning from the default to all other sources...')

        for dstPath in self.sourcesPaths:
            if dstPath == self.defaultSourcePath:
                continue

            print(f'\tcopying kerning to {os.path.split(dstPath)[-1]}...')
            dstFont = OpenFont(dstPath, showInterface=False)
            dstFont.kerning.clear()
            dstFont.kerning.update(srcFont.kerning)
            dstFont.save()

        print('...done!\n')

    def copyUnicodesFromDefault(self, preflight=False):
        '''Copy unicodes from the default source to all other sources.'''

        srcFont = OpenFont(self.defaultSourcePath, showInterface=False)

        print(f'copying all unicodes from the default to all other sources...')
        for dstPath in self.sourcesPaths:
            if dstPath == self.defaultSourcePath:
                continue

            dstFont = OpenFont(dstPath, showInterface=False)

            print(f'\tcopying unicodes to {os.path.split(dstPath)[-1]}...')
            for glyphName in srcFont.glyphOrder:
                if glyphName not in srcFont or glyphName not in dstFont:
                    continue
                if dstFont[glyphName].unicodes != srcFont[glyphName].unicodes:
                    print(f'\t\tcopying unicodes in {glyphName}...')
                    if not preflight:
                        dstFont[glyphName].unicodes = srcFont[glyphName].unicodes

            if not preflight:
                print(f'\tsaving font...')
                dstFont.save()

        print('...done!\n')

    def copyGlyphOrderFromDefault(self):
        '''Copy glyph order from the default source to all other sources.'''

        srcFont = OpenFont(self.defaultSourcePath, showInterface=False)
        glyphOrder = srcFont.templateGlyphOrder # srcFont.glyphOrder

        print(f'copying glyph order from the default to all other sources...')
        for dstPath in self.sourcesPaths:
            if dstPath == self.defaultSourcePath:
                continue
            dstFont = OpenFont(dstPath, showInterface=False)
            print(f'\tcopying default glyph order to {os.path.split(dstPath)[-1]}...')
            dstFont.templateGlyphOrder = glyphOrder
            dstFont.save()

        print('...done!\n')

    def buildCompositeGlyphs(self, glyphNames):
        '''Build composite glyphs from glyph constructions.'''
        pass

    def splitSources(self, srcName, dstName, glyphNames):
        '''Split new parametric sources from existing sources.'''
        for srcPath in self.sourcesPaths:
            srcFileName = os.path.split(srcPath)[-1]
            if srcName in srcFileName:
                dstFileName = srcFileName.replace(srcName, dstName)
                print(srcFileName, dstFileName)
                # 1. duplicate default as dstName
                # 2. copy glyphNames from srcName to dstName
                # 3. copy glyphNames from default to srcName
        pass

    def createTuningSources(self, sparse=False):
        '''Initialize tuning sources for all blended locations.'''
        if self.verbose:
            print('creating tuning sources...')

        for styleName in self.blendedSources.keys():

            if 'opsz' not in styleName and 'wght' not in styleName and 'wght' not in styleName:
                continue

            ufoPath = os.path.join(self.tuningSourcesFolder, f'{styleName}.ufo')
            if os.path.exists(ufoPath):
                continue

            if self.verbose:
                print(f'\tcreating {styleName}...')

            # duplicate default
            shutil.copytree(self.defaultSourcePath, ufoPath)

            f = OpenFont(ufoPath, showInterface=False)

            if sparse:
                for glyphName in f.glyphOrder:
                    f.removeGlyph(glyphName)

            f.info.styleName = styleName
            f.kerning.clear()
            f.features.text = ''

            f.close(save=True)

        if self.verbose:
            print('...done!\n')

    def calculateTuningSources(self, glyphNames, referenceSource, levels=[1, 2, 3]):
        '''Calculate tuning sources for glyphs based on reference default source.'''

        referenceFont = OpenFont(referenceSource, showInterface=False)

        operator = UFOOperator()
        operator.read(self.designspacePath)
        operator.loadFonts()

        referenceSources = {'_'.join(k.split('_')[1:]): OpenFont(v, showInterface=False) for k, v in self.referenceSources.items()}

        for glyphName in glyphNames:

            glyphDefault = self.defaultFont[glyphName]

            # SKIP COMPOSITE GLYPHS!
            # collect base glyphs for tuning?
            if glyphDefault.components:
                continue

            glyphReference = referenceFont[glyphName]
            matchingPoints = getMatchingPoints(glyphDefault, glyphReference)

            if self.verbose:
                print(f'calculating tuning sources for /{glyphName}...\n')

            for styleName, ufoPath in self.tuningSources.items():
                styleNameParts = styleName.split('_')
                if len(styleNameParts) not in levels:
                    continue

                if self.verbose:
                    print(f'\ttuning {styleName}...')

                # get blended glyph (parametric)
                blendedLocation = { part[:4]: int(part[4:]) for part in styleNameParts }
                parametricLocation = getEffectiveLocation(self.designspacePath, blendedLocation)
                blendedGlyph = RGlyph(instantiateGlyph(operator, glyphName, parametricLocation))

                # get reference glyph
                blendedReference = referenceSources[styleName][glyphName]

                # make tuning glyph
                tuningGlyph = makeTuningGlyph(blendedGlyph, blendedReference, glyphDefault, matchingPoints)

                # save glyph to tuning source
                tuningSource = OpenFont(ufoPath, showInterface=False)
                tuningSource.insertGlyph(tuningGlyph, name=glyphName)
                tuningSource.save()

            if self.verbose:
                print()

        if self.verbose:
            print('...done!\n')

    def resetTuningSources(self):
        '''Clear all glyphs from all tuning sources.'''

        if self.verbose:
            print('resetting tuning sources...\n')

        for styleName, ufoPath in self.tuningSources.items():
            f = OpenFont(ufoPath, showInterface=False)
            if self.verbose:
                print(f'\tresetting all glyphs from {styleName}...')
            for glyphName in self.defaultFont.glyphOrder:
                f.insertGlyph(self.defaultFont[glyphName], name=glyphName)
            f.glyphOrder = self.defaultFont.glyphOrder
            f.close(save=True)

        if self.verbose:
            print('\n...done!\n')

    # designspace

    def addParametricAxes(self, customAxes={}):
        '''Add parametric axes to the designspace.'''

        if self.verbose:
            print('\tadding parametric axes...')

        for name in self.parametricAxes:
            # get default value
            if name in self.measurementsDefault.values:
                defaultValue = permille(self.measurementsDefault.values[name], self.defaultFont.info.unitsPerEm)
            elif name in customAxes:
                defaultValue = customAxes[name]

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

    def addParametricSources(self, familyName=None):
        '''Add parametric sources to the designspace.'''
        if self.verbose:
            print('\tadding parametric sources...')

        for name in self.parametricAxes:
            for ufoPath in self.sourcesPaths:
                if name in ufoPath:
                    # if self.verbose:
                    #     print(f'\t\tadding {ufoPath}...')
                    src = SourceDescriptor()
                    src.path = ufoPath
                    src.familyName = self.familyName if not familyName else familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufoPath)[-1])[0].split('_')[-1][4:])
                    src.styleName = src.name = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addDefaultSource(self, familyName=None):
        '''Add the default source to the designspace.'''

        if not self.designspace:
            return

        src = SourceDescriptor()
        src.path       = self.defaultSourcePath
        src.familyName = self.familyName if not familyName else familyName
        src.styleName  = src.name = self.defaultName
        src.location   = self.defaultLocation

        self.designspace.addSource(src)

    def addTuningAxes(self):
        '''Add tuning axes to the designspace.'''

        if self.verbose:
            print('\tadding tuning axes...')

        for styleName, axis in self.tuningAxes.items():
            # print(f'\t\tadding tuning axis: {styleName} {axis.tag}...')
            self.designspace.addAxis(axis)

    def addTuningSources(self, familyName=None):
        '''Add tuning sources to the designspace.'''

        if self.verbose:
            print('\tadding tuning sources...')

        for styleName, axis in self.tuningAxes.items():
            tuningSourcePath = self.tuningSources[styleName]
            # print(f'\t\tadding tuning source: {styleName} {axis.tag}...')
            src = SourceDescriptor()
            src.path = tuningSourcePath
            src.familyName = self.familyName if not familyName else familyName
            src.styleName = src.name = styleName
            L = self.defaultLocation.copy()

            # for styleNamePart in styleName.split('_'):
            #     tag, value = styleNamePart[:4], styleNamePart[4:]
            #     L[tag] = value

            L[axis.tag] = axis.maximum
            src.location = L
            self.designspace.addSource(src)

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

            # set value for corner tuning axes
            if self.tuning:
                for tuningStyleName, tuningAxis in self.tuningAxes.items():
                    if styleName == tuningStyleName:
                        outputLocation[tuningAxis.tag] = tuningAxis.maximum
                    else:
                        outputLocation[tuningAxis.tag] = tuningAxis.default

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation
            m.description    = styleName

            self.designspace.addAxisMapping(m)

    # building

    def buildDesignspace(self, instances=False):
        '''Build designspace file from source data.'''

        if self.verbose:
            print(f'building {os.path.split(self.designspacePath)[-1]}...')

        self.designspace = DesignSpaceDocument()

        self.addBlendedAxes()
        self.addParametricAxes()

        if self.tuning:
            self.addTuningAxes()

        self.addBlendedSources()
        self.addDefaultSource()
        self.addParametricSources()

        if self.tuning:
            self.addTuningSources()

        if instances:
            self.addInstances()

        self.addCustomKeysToLib()

        self.save()

    def buildInstances(self, clear=True):
        '''Build UFO instances for blended sources.'''
        pass

    def buildVariableFont(self, debug=False, featureWriter=True, noGDEF=False):
        '''Build avar2 variable font from designspace.'''

        print(f'generating variable font for {self.designspaceFile}...')

        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        print(f'\tloading sources...')
        for src in D.sources:
            if debug:
                print(f'\t\tloading {src.familyName} {src.styleName}...')
            src.font = Font(src.path)

        # generate variable font with fontmake

        if 'PYTHONHOME' in os.environ:
           del os.environ['PYTHONHOME']

        print(f"\tbuilding avar2 font... ", end='')

        cmd  = ['/Library/Frameworks/Python.framework/Versions/3.11/bin/fontmake']
        cmd += ['-m', self.designspacePath]
        cmd += ['-o', 'variable']
        cmd += ['--output-path', self.varFontPath]
        if not featureWriter:
            cmd += ['--feature-writer', 'None']
        if noGDEF:
            cmd += ['--no-generate-GDEF']
        cmd += ['--keep-direction']
        cmd += ['--verbose WARNING']
        cmd  = ' '.join(cmd)

        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
            for line in p.stdout.readlines():
                print(line,)
            retval = p.wait()

        print(f'{os.path.exists(self.varFontPath)}')

        print('...done.\n')

    # saving

    def cleanupSources(self, parametric=True, tuning=True, clearFontLibs=True, clearGlyphLibs=True, clearFontGuides=True, clearGlyphGuides=True, clearMarks=True, clearLayers=True, preflight=False, ignoreLayers=[]):
        '''Remove unnecessary data from UFO sources.'''

        # delete all font libs except these:
        ignoreFontLibs = [
            'com.typemytype.robofont.italicSlantOffset',
            'com.typemytype.robofont.segmentType',
        ]

        # delete all layers except these:
        ignoreLayers += ['foreground']

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
        '''Save paths to data files in the designspace lib.'''

        if self.verbose:
            print('\tadding custom keys to lib...')

        if os.path.exists(self.smartSetsPath):
            self.designspace.lib[smartSetsPathKey] = os.path.relpath(self.smartSetsPath, self.sourcesFolder)

        if os.path.exists(self.measurementsPath):
            self.designspace.lib[measurementsPathKey] = os.path.relpath(self.measurementsPath, self.sourcesFolder)

        if os.path.exists(self.glyphConstructionsPath):
            self.designspace.lib[glyphConstructionsPathKey] = os.path.relpath(self.glyphConstructionsPath, self.sourcesFolder)

        if os.path.exists(self.referenceFontPath):
            self.designspace.lib[referenceFontPathKey] = os.path.relpath(self.referenceFontPath, self.sourcesFolder)

    def save(self):
        '''Save current designspace to file.'''

        if not self.designspace:
            return

        if self.verbose:
            print(f'\tsaving designspace...', end=' ')

        self.designspace.write(self.designspacePath)
        if self.verbose:
            print(os.path.exists(self.designspacePath))
            print()

    # project info

    def printAxes(self):
        '''Print a list of all variation axes in this project.'''

        measurements = {}
        for d in self.measurementsDefault.definitions:
            name, description = d[0], d[7]
            measurements[name] = description

        print('\n### Parametric axes\n')
        for n, axis in enumerate(self.parametricAxes):
            print(f'{n+1}. `{axis}` {measurements.get(axis)}')

        print('\n### Tuning axes\n')
        for styleName, tuningAxis in self.tuningAxes.items():
            print(f"- `{tuningAxis.tag}` {styleName.replace('_', ' ')}")

        print()

    def printSettings(self):
        '''Print an overview of this project’s settings.'''

        txt  = f'base folder: {self.baseFolder}\n'
        txt += f'family name: {self.familyName}\n\n'
        # txt += f'settings file: {self.settingsFile}\n'
        # txt += f'settings path: {self.settingsPath} ({os.path.exists(self.settingsPath)})\n\n'

        txt += f'designspace file: {self.designspaceFile}\n'
        txt += f'designspace path: {self.designspacePath} ({os.path.exists(self.designspacePath)})\n\n'

        txt += f'sources folder name: {self.sourcesFolderName}\n'
        txt += f'sources folder path: {self.sourcesFolder} ({os.path.exists(self.sourcesFolder)})\n'
        txt += f'sources paths: {self.sourcesPaths}\n\n'

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
        txt += f'blended axes: {list(self.blendedAxes.keys())}\n'
        txt += f'blended sources: {list(self.blendedSources.keys())}\n\n'

        txt += f'tuning folder name: {self.tuningSourcesFolderName}\n'
        txt += f'tuning folder path: {self.tuningSourcesFolder} ({os.path.exists(self.tuningSourcesFolder)})\n'
        txt += f'tuning sources paths: {self.tuningSourcesPaths}\n\n'

        txt += f'reference folder name: {self.referenceSourcesFolderName}\n'
        txt += f'reference folder path: {self.referenceSourcesFolder} ({os.path.exists(self.referenceSourcesFolder)})\n'
        txt += f'reference sources paths: {self.referenceSourcesPaths}\n'
        txt += f'reference blends path: {self.referenceBlendsPath} ({os.path.exists(self.referenceBlendsPath)})\n'
        txt += f'reference font path: {self.referenceFontPath} ({os.path.exists(self.referenceFontPath)})\n\n'

        txt += f'instances folder name: {self.instancesFolderName}\n'
        txt += f'instances folder path: {self.instancesFolder} ({os.path.exists(self.instancesFolder)})\n\n'

        txt += f'fonts folder name: {self.fontsFolderName}\n'
        txt += f'fonts folder: {self.fontsFolder} ({os.path.exists(self.fontsFolder)})\n\n'
        txt += f'variable font file: {self.varFontFile}\n'
        txt += f'variable font path: {self.varFontPath} ({os.path.exists(self.varFontPath)})\n\n'

        print(txt)

    # validation

    def validateDesignspace(self, locations=True, mappings=True, instances=True):
        '''Validate range of designspace locations.'''
        validateDesignspace(self.designspacePath, locations=locations, mappings=mappings, instances=instances)

    def validateSources(self, width=False, left=False, right=False, points=True, components=True, anchors=True, unicodes=True, targetSources=[]):
        '''Validate glyph attributes in all sources against the default.'''

        options = {
            'width'      : width,
            'left'       : left,
            'right'      : right,
            'points'     : points,
            'components' : components,
            'anchors'    : anchors,
            'unicodes'   : unicodes,
        }

        txt = 'validating sources...\n\n'
        for check in options:
            if options[check]:
                txt += f'\t- {check}\n'
        txt += '\n'

        # get default font
        txt += f'\tdefault font: {self.defaultFont.info.familyName} {self.defaultFont.info.styleName}\n\n'

        # get target sources
        if not targetSources:
            targetPaths = self.sourcesPaths
        else:
            targetPaths = [os.path.join(self.sourcesFolder, f'{srcName}.ufo') for srcName in targetSources]

        if self.defaultSourcePath in targetPaths:
            targetPaths.remove(self.defaultSourcePath)
        targetFonts = [OpenFont(f, showInterface=False) for f in targetPaths]

        txt += validateFonts(targetFonts, self.defaultFont, options)
        txt += '...done!\n\n'

        print(txt)

    # proofing

    def proofGlyphMemes(self, glyphNames, anchors=True):
        '''Build glyph meme PDF proofs.'''
        for glyphName in glyphNames:
            P = GlyphMemeProofer(glyphName, self.designspacePath)
            P.anchorsDraw = anchors
            P.draw()

            pdfFileName = os.path.splitext(os.path.split(self.designspacePath)[-1])[0]
            glyphMemesFolder = os.path.join(self.proofsFolder, 'PDF', 'glyph-memes')
            P.save(glyphMemesFolder, pdfFileName)

    def proofSourcesGlyphSet(self, familyName=None, showCompatible=True, validateComposites=True):
        '''Build glyph set PDF proofs.'''
        if not familyName:
            familyName = self.familyName

        sourcePaths = sorted(glob.glob(f'{self.sourcesFolder}/*.ufo'))
        glyphsetProofsFolder = os.path.join(self.proofsFolder, 'PDF', 'glyphset')

        P = GlyphSetProofer(f'{familyName}', self.defaultSourcePath, sourcePaths, self.glyphConstructionsPath)
        P.checksShowCompatible = showCompatible
        P.validateComposites = validateComposites
        P.build(savePDF=True, folder=glyphsetProofsFolder)

    def proofBlends(self, glyphNames, familyName=None, margins=True, labels=True, levels=False, levelsShow=[1, 2, 3, 4], header=True, footer=True, points=False):
        '''Build PDF proof of blends.'''

        B = BlendsPreview(self.designspacePath)

        if self.referenceFontPath:
            B.compareFontPath = self.referenceFontPath
            B.compare = True
        else:
            B.compare = False

        designspace = DesignSpaceDocument()
        designspace.read(self.designspacePath)

        blendedAxes = ['opsz', 'wght', 'wdth']

        axesList = []
        for axis in designspace.axes:
            if axis.tag in blendedAxes:
                axesList.append((axis.tag, [int(axis.minimum), int(axis.default), int(axis.maximum)]))

        B.axesList   = axesList
        B.margins    = margins
        B.labels     = labels
        B.levels     = levels
        B.levelsShow = levelsShow
        B.header     = header
        B.footer     = footer
        B.points     = points

        for glyphName in glyphNames:
            if not glyphName:
                continue
            B.draw(glyphName)

        if not familyName:
            familyName = self.familyName

        pdfPath = os.path.join(self.proofsFolder, 'PDF', 'blending', f'blending-preview_{familyName}.pdf')
        print(f'saving {pdfPath}...', end=' ')
        B.save(pdfPath)
        print(f'done!\n')

    def proofTuning(self, glyphNames, referenceSource, level=1):
        '''Build PDF proofs of tuning sources.'''

        T = TuningPreview(self, referenceSource)

        for glyphName in glyphNames:
            # skip composite glyphs
            defaultGlyph = self.defaultFont[glyphName]
            if defaultGlyph.components:
                continue

            T.draw(glyphName, level=level)

            pdfFileName = os.path.splitext(os.path.split(self.designspacePath)[-1])[0]
            tuningProofsFolder = os.path.join(self.proofsFolder, 'PDF', 'tuning')
            T.save(tuningProofsFolder, pdfFileName)








