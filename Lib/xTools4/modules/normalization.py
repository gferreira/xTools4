import os, glob, shutil
from ufonormalizer import normalizeUFO
from fontParts.world import OpenFont


def cleanupSources(sourcesFolder, clearFontLibs=True, clearGlyphLibs=True, clearFontGuides=True, clearGlyphGuides=True, clearMarks=True, clearLayers=True, preflight=True, verbose=False, ignoreFontLibs=[], ignoreLayers=[]):

    ufoPaths  = glob.glob(f'{sourcesFolder}/*.ufo')

    fontLibKeys  = []
    glyphLibKeys = []
    layerNames   = []

    print(f'cleaning up sources...\n')

    for ufoPath in ufoPaths:
        fileName = os.path.split(ufoPath)[-1]
        name = os.path.splitext(fileName)[0].split('_')[-1]

        print(f'\tcleaning up {fileName}...')
        f = OpenFont(ufoPath, showInterface=False)

        if clearLayers:
            if verbose:
                print(f'\t\tcleaning up font layers...')
            for layer in f.layers:
                if layer.name == 'public.default':
                    layer.name = 'foreground'
            for layerName in f.layerOrder:
                if layerName not in ignoreLayers:
                    if layerName not in layerNames:
                        layerNames.append(layerName)
                    f.removeLayer(layerName)

        if clearFontLibs:
            if verbose:
                print(f'\t\tcleaning up font libs...')
            for k in f.lib.keys():
                if k.startswith('public.') or k in ignoreFontLibs:
                     continue
                if k not in fontLibKeys:
                    fontLibKeys.append(k)
                del f.lib[k]

        if clearGlyphLibs:
            if verbose:
                print(f'\t\tcleaning up glyph libs...')
            for g in f:
                for k in g.lib.keys():
                    if k not in glyphLibKeys:
                        glyphLibKeys.append(k)
                    del g.lib[k]

        if clearFontGuides:
            if verbose:
                print(f'\t\tcleaning up font guidelines...')
            f.clearGuidelines()

        if clearGlyphGuides:
            if verbose:
                print(f'\t\tcleaning up glyph guidelines...')
            for g in f:
                if not len(g.guidelines):
                    continue
                g.clearGuidelines()

        if clearMarks:
            if verbose:
                print(f'\t\tcleaning up mark colors...')
            for g in f:
                g.markColor = None

        if not preflight:
            if verbose:
                print(f'\t\tsaving UFO source...')
            f.save()

        f.close()

    print()
    if clearFontLibs:
        print('deleted font libs:')
        for k in fontLibKeys:
            print(f'- {k}')
        print()

    if clearGlyphLibs:
        print('deleted glyph libs:')
        for k in glyphLibKeys:
            print(f'- {k}')
        print()

    if layerNames:
        print('deleted layers:')
        for k in layerNames:
            print(f'- {k}')
        print()

    print('...done!\n')


def normalizeSources(sourcesFolder, verbose=True):
    ufoPaths  = glob.glob(f'{sourcesFolder}/*.ufo')
    print(f'normalizing UFO sources...\n')
    for ufoPath in ufoPaths:
        print(f'\tnormalizing {os.path.split(ufoPath)[-1]}...')
        normalizeUFO(ufoPath, onlyModified=False, writeModTimes=False)
    print('\n...done!\n')

