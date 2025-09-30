from importlib import reload
import xTools4.modules.linkPoints2
reload(xTools4.modules.linkPoints2)

import os, csv
from fontTools.agl import UV2AGL
from fontParts.world import RFont
from xTools4.modules.linkPoints2 import *


tempEditModeKey = 'com.xTools4.tempEdit.mode'


def permille(value, unitsPerEm):
    '''Converts a value in font units to a permille value (thousands of em).'''
    return round(value * 1000 / unitsPerEm)


class FontMeasurements:
    '''
    M = FontMeasurements()
    M.read(jsonPath)
    M.measure(f)

    # print all measurements
    M.print()

    print(M.definitions)
    print(M.values)

    '''

    def __init__(self, definitions=[]):
        self.definitions = definitions
        self.values = {}

    def read(self, jsonPath):
        M = readMeasurements(jsonPath)
        self.definitions = []
        for name, attrs in M['font'].items():
            try:
                pt1 = int(attrs['point 1'])
            except:
                pt1 = attrs['point 1']
            try:
                pt2 = int(attrs['point 2'])
            except:
                pt2 = attrs['point 2']
            self.definitions.append((name, attrs['direction'], attrs['glyph 1'], pt1, attrs['glyph 2'], pt2, attrs.get('parent'), attrs.get('description')))

    def measure(self, font, roundToInt=True, absolute=False):
        for d in self.definitions:
            M = Measurement(*d)
            self.values[M.name] = M.measure(font, roundToInt=roundToInt, absolute=absolute)

    def print(self):
        for k, v in self.values.items():
            print(k, v)


class GlyphMeasurements:
    '''
    M = GlyphMeasurements(font, glyphName)
    M.read(jsonPath)
    M.measure(g)

    print(M.definitions)
    print(M.values)

    '''

    def __init__(self, font, glyphName, definitions=[]):
        self.font        = font
        self.glyphName   = glyphName
        self.definitions = definitions
        self.values      = []

    def read(self, jsonPath):
        M = readMeasurements(jsonPath)

        measurements = M['glyphs'].get(self.glyphName)
        if not measurements:
            print('no measurements for glyph!')
            return

        self.definitions = []
        for key, attrs in measurements.items():
            parts = key.split()
            if len(parts) == 2:
                pt1, pt2 = parts
            else:
                continue

            try:
                pt1 = int(pt1)
            except:
                pass
            try:
                pt2 = int(pt2)
            except:
                pass

            self.definitions.append((attrs['name'], attrs['direction'], self.glyphName, pt1, self.glyphName, pt2))

    def measure(self, glyph=None, roundToInt=True, absolute=False):

        for d in self.definitions:
            if glyph is not None:
                d = list(d)
                d[2] = d[4] = glyph.name

            M = Measurement(*d)
            self.values.append(M.measure(self.font, roundToInt=roundToInt, absolute=absolute))


class Measurement:

    '''
    M = Measurement('XTRA', 'x', 'H', 10, 'H', 9)
    print(M.measure(font))

    '''

    font = None

    def __init__(self, name, direction, glyphName1, pointIndex1, glyphName2, pointIndex2, parent=None, description=None):
        self.name        = name
        self.direction   = direction
        self.glyphName1  = glyphName1
        self.pointIndex1 = pointIndex1
        self.glyphName2  = glyphName2
        self.pointIndex2 = pointIndex2
        self.parent      = parent

    @property
    def fontIsDefcon(self):
        return hasattr(self.font, 'representationFactories')

    @property
    def glyph1(self):
        if self.font:
            if self.glyphName1 and self.glyphName1 in self.font:
                return self.font[self.glyphName1]

    @property
    def glyph2(self):
        if self.font:
            if self.glyphName2 and self.glyphName2 in self.font:
                return self.font[self.glyphName2]

    @property
    def point1(self):
        if self.glyph1 is not None:
            try:
                return getPointAtIndex(self.glyph1, int(self.pointIndex1), isDefcon=self.fontIsDefcon)
            except:
                return getAnchorPoint(self.font, self.pointIndex1)

    @property
    def point2(self):
        if self.glyph2 is not None:
            try:
                return getPointAtIndex(self.glyph2, int(self.pointIndex2), isDefcon=self.fontIsDefcon)
            except:
                return getAnchorPoint(self.font, self.pointIndex2)

    def measure(self, font, roundToInt=True, absolute=False, verbose=False, italicCorrection=True):

        self.font = font

        if verbose:
            print(f'measuring {self.font}...')
            print(f'\tglyph 1   : {self.glyphName1} {self.glyph1}')
            print(f'\tpoint 1   : {self.pointIndex1} {self.point1}')
            print(f'\tglyph 2   : {self.glyphName2}  {self.glyph2}')
            print(f'\tpoint 2   : {self.pointIndex2} {self.point2}')
            print(f'\tdirection : {self.direction}')

        if self.font is None:
            return

        if self.point1 is None or self.point2 is None:
            return

        x1, y1 = self.point1.x, self.point1.y
        x2, y2 = self.point2.x, self.point2.y

        if italicCorrection:
            angle  = font.info.italicAngle
            offset = font.lib.get('com.typemytype.robofont.italicSlantOffset') or 0
            if angle or offset:
                x1, y1 = offsetAngledPoint((x1, y1), angle, offset)
                x2, y2 = offsetAngledPoint((x2, y2), angle, offset)

        if self.direction == 'x':
            d = x2 - x1

        elif self.direction == 'y':
            d = y2 - y1

        else:
            d = sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if absolute:
            d = abs(d)

        if roundToInt:
            d = round(d)

        if verbose:
            print(f'\tdistance : {d}')
            print('...done.\n')

        return d





#-------------------
# measurement tools
#-------------------

def extractMeasurements(ufos, measurementsPath, parametricAxes):
    sources = {}
    print('extracting measurements from UFOs...')
    for ufoPath in sorted(ufos):
        fontName = os.path.splitext(os.path.split(ufoPath)[-1])[0]
        styleName = '_'.join(fontName.split('_')[1:])
        f = OpenFont(ufoPath, showInterface=False)
        print(f'\tmeasuring {fontName}…')
        M = FontMeasurements()
        M.read(measurementsPath)
        M.measure(f)
        sources[styleName] = { k: permille(v, f.info.unitsPerEm) for k, v in M.values.items() if k in parametricAxes }
    print('...done!\n')
    return sources

def renameGlyphMeasurements(measurementsPath, glyphNames, renameDict):

    measurements = readMeasurements(measurementsPath)

    print(f"renaming glyph measurements...\n")

    for glyphName in glyphNames:
        print(f"\trenaming measurements in /{glyphName}...")
        if glyphName not in measurements['glyphs']:
            continue

        glyphMeasurements = {}
        for ID, m in measurements['glyphs'][glyphName].items():
            if m['name'] in renameDict:
                newName = renameDict[m['name']]
                print(f"\t\trenaming {m['name']} to {newName}...")
                glyphMeasurements[ID] = {
                    'name'      : newName,
                    'direction' : m['direction'],
                }
            else:
                glyphMeasurements[ID] = m

        measurements['glyphs'][glyphName] = glyphMeasurements
        print()

    print('\tsaving measurements...')
    with open(measurementsPath, 'w', encoding='utf-8') as f:
        json.dump(measurements, f, indent=2)

    print('...done.')


def setSourceNamesFromMeasurements(sourcesFolder, familyName, measurementsPath, preflight=True, ignoreTags=[]):

    ### expects semi-correct source names -- ex: FamilyName_AXISmin.ufo

    allSources = glob.glob(f'{sourcesFolder}/*.ufo')

    allSourceNames = []
    for sourcePath in sorted(allSources):
        tag = os.path.splitext(os.path.split(sourcePath)[-1])[0].split('_')[-1][:4]

        # set family name
        f = OpenFont(sourcePath, showInterface=False)
        if f.info.familyName != familyName:
            print(f'family name: {f.info.familyName} --> {familyName}' )
            if not preflight:
                f.info.familyName = familyName

        # measure source
        if tag not in ignoreTags:
            m = FontMeasurements()
            m.read(measurementsPath)
            m.measure(f)
            newValue = m.values[tag]
            newValue1000 = round(newValue * 1000 / f.info.unitsPerEm)

        # exception: get tag value from file name
        else:
            newValue = newValue1000 = int(os.path.splitext(os.path.split(sourcePath)[-1])[0].split('_')[-1][4:])

        # set style name
        newStyleName = f'{tag}{newValue1000}'
        allSourceNames.append(newStyleName)
        if newStyleName != f.info.styleName:
            print(f'updating style name:\n\t{f.info.styleName} --> {newStyleName}\n' )
            if not preflight:
                f.info.styleName = newStyleName

        # rename UFO file
        newSourceName = f'{familyName.replace(' ', '-')}_{newStyleName}.ufo'
        newSourcePath = os.path.join(sourcesFolder, newSourceName)
        if not preflight:
            f.save()
        f.close()

        if sourcePath != newSourcePath:
            print(f'updating file name:\n\t{os.path.split(sourcePath)[-1]} --> {newSourceName}\n' )
            if not preflight:
                shutil.move(ufo, newSourcePath)

    # find duplicate styles
    duplicates = [k for k, v in Counter(allSourceNames).items() if v > 1]
    print('duplicate style names:')
    print(duplicates)
