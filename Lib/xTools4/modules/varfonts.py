import os, glob
import shutil
from fontParts.world import RFont, OpenFont
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, RuleDescriptor
from xTools4.modules.unicode import autoUnicode
from xTools4.modules.encoding import cropGlyphset

try:
    import ufoProcessor
except ModuleNotFoundError:
    print('ufoProcessor is not available in this environment')
    pass

'''Tools to create variable fonts. These are very specific to my workflow, probably not useful for anyone else.'''


def buildVariableFontMasters2(srcFolder, dstFolder, glyphOrder, fontInfoDict, kerning=True, groups=True, features=None, verbose=True, decomposeGlyphs=[], customUnicodes={}):
    '''
    Export UFO masters for generating variable fonts from multilayer complete design masters.

    - Layers in design masters are exported as separated UFOs for variable fonts.
    - To avoid errors during development, the glyph set is reduced based on the given glyph order.

    '''

    # remove existing var masters
    varUFOs = [os.path.join(dstFolder, f) for f in os.listdir(dstFolder) if os.path.splitext(f)[-1] == '.ufo']
    if varUFOs:
        for ufo in varUFOs:
            shutil.rmtree(ufo)

    # make var masters
    ufos = [f for f in os.listdir(srcFolder) if os.path.splitext(f)[-1] == '.ufo']

    for ufo in ufos:
        ufoSrcPath = os.path.join(srcFolder, ufo)
        ufoVarPath = os.path.join(dstFolder, ufo)
        shutil.copytree(ufoSrcPath, ufoVarPath)

        f = OpenFont(ufoVarPath, showInterface=False)

        # clear font data
        f.clearGuidelines()
        if not kerning:
            f.kerning.clear()
        if not groups:
            f.groups.clear()

        # clear layers
        for layerName in f.layerOrder:
            if layerName != f.defaultLayer.name:
                f.removeLayer(layerName)

        # set glyph order
        cropGlyphset(f, glyphOrder)
        f.glyphOrder = glyphOrder

        for glyphName in f.glyphOrder:
            if glyphName not in f:
                continue
 
            glyph = f[glyphName]
            glyph.clearGuidelines()
            glyph.clearAnchors()
            autoUnicode(glyph, customUnicodes=customUnicodes)

            if glyphName in decomposeGlyphs:
                glyph.decompose()

        # set features
        if features and os.path.exists(features):
            with open(features, 'r') as feaFile:
                feaText = feaFile.read()
                f.features.text = feaText
        else:
            f.features.text = ''

        f.save()
        f.close()

def getNeutral(designSpacePath):
    designSpace = DesignSpaceDocument()
    designSpace.read(designSpacePath)
    
    default = designSpace.findDefault()
    return default.filename

def setVariableFontInfo(designSpacePath, fontInfoDict, kerning=True, groups=True, features=False):
    '''
    Font info data specific to the variable font is set in the neutral master.

    '''
    designSpace = DesignSpaceDocument()
    designSpace.read(designSpacePath)
    varFolder = os.path.dirname(designSpacePath)

    # get neutral
    neutralPath = os.path.join(varFolder, designSpace.default.filename)

    # set attributes in neutral
    neutral = OpenFont(neutralPath, showInterface=False)
    for attr, value in fontInfoDict.items():
        setattr(neutral.info, attr, value)

    # set features in neutral
    if features and os.path.exists(features):
        with open(features, 'r') as feaFile:
            feaText = feaFile.read()
            neutral.features.text = feaText

    neutral.save()

    if kerning or groups:
        for source in designSpace.sources:
            if neutralPath == source.path:
                continue
            f = OpenFont(source.path, showInterface=False)

            # copy kerning
            if kerning:
                for pair, value in neutral.kerning.items():
                    f.kerning[pair] = value

            if groups:
                for group in neutral.groups:
                    f.groups[group] = neutral.groups[group]

            # set features in neutral
            # if features:
            #     f.features.text = feaText

            f.save()
            f.close()

    neutral.close()

def makeDesignSpace(familyName, axes, sources, instances=None, rules=None, sourcesFolder=None, ext='ufo'):

    '''
    Create a .designspace file with the given data.

    '''

    doc = DesignSpaceDocument()

    # add axes
    for axisName, axis in axes.items():
        a = AxisDescriptor()
        a.name    = axisName
        a.tag     = axis['tag']
        a.maximum = axis['maximum']
        a.minimum = axis['minimum']
        a.default = axis['default']
        if 'map' in axis:
            a.map = axis['map']
        if 'hidden' in axis:
            a.hidden = axis['hidden']
        doc.addAxis(a)

    # add sources
    for styleName, location in sources.items():
        srcPath = f'{styleName}.{ext}'
        src = SourceDescriptor()
        src.path       = srcPath if sourcesFolder is None else os.path.join(sourcesFolder, srcPath)
        src.familyName = familyName
        src.name       = styleName
        src.styleName  = styleName
        src.location   = location
        # neutral
        if not any(location.values()):
            src.copyInfo     = True
            src.copyLib      = True
            src.copyGroups   = True
            src.copyFeatures = True
            # doc.default      = src.name # doesn't work?
            # src.isDefault    = True

        doc.addSource(src)

    # add rules
    if rules is not None:
        for ruleName in rules.keys():
            rule = RuleDescriptor(name=ruleName)
            rule.conditionSets = rules[ruleName]['conditionSets']
            rule.subs          = rules[ruleName]['subs']
            doc.addRule(rule)

    # add instances
    if instances is not None:
        for instanceName in instances.keys():
            instance = InstanceDescriptor()
            instance.familyName = familyName
            instance.styleName  = instanceName
            instance.location   = instances[instanceName]
            doc.addInstance(instance)

    return doc

def fillSparseMasters(folder, prefix):
    ### THIS IS PROBABLY NOT NECESSARY!!!
    ### LOOK INTO source.mutedGlyphNames <<<---
    ufos = glob.glob(f'{folder}/*.ufo')
    ufosPrefix = [f for f in ufos if os.path.basename(f).startswith(prefix)]
    for dstPath in ufosPrefix:
        dstFont = OpenFont(dstPath, showInterface=False)
        srcPath = dstPath.replace(prefix, '')
        srcFont = OpenFont(srcPath, showInterface=False)
        print(f'filling glyphs in {dstFont.info.styleName} with {srcFont.info.styleName}...')
        for glyph in srcFont:
            # don't overwrite existing glyphs!
            if glyph.name in dstFont: # and len(dstFont[glyph.name]):
                continue
            # print(f'\tinserting {glyph.name}...')
            dstFont.insertGlyph(glyph, name=glyph.name)
            dstFont[glyph.name].markColor = 1, 0, 0, 0.35
        dstFont.save()
        srcFont.close()

def makeInstances(designSpacePath, dstFolder, roundGeometry=True, verbose=True):
    '''Build UFO instances in designspace into a given folder.'''
    instances = glob.glob(f'{dstFolder}/*.ufo')
    for ufoPath in instances:
        shutil.rmtree(ufoPath)
    # generate instances
    if verbose:
        print(f'generating instances in designspace {designSpacePath}...')
    ufoProcessor.build(designSpacePath, roundGeometry=roundGeometry)
