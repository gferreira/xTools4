import os
from fontParts.world import OpenFont
from xTools4.modules.validation import assignValidationGroup


measurementsPathKey       = 'com.xTools4.xProject.measurementsPath'
smartSetsPathKey          = 'com.xTools4.xProject.smartSetsPath'
glyphConstructionsPathKey = 'com.xTools4.xProject.glyphConstructionsPath'
referenceFontPathKey      = 'com.xTools4.xProject.referenceFontPath'


def updateGlyphsFromDefault(currentFont, oldDefaultFont, newDefaultFont, glyphNames, preflight=False):

    name = os.path.splitext(os.path.split(currentFont.path)[-1])[0].split('_')[-1]

    print(f'updating glyphs in font {name}...')

    fontChanged = False
    for glyphName in glyphNames:
        if glyphName not in oldDefaultFont or glyphName not in currentFont or glyphName not in newDefaultFont:
            continue

        oldDefaultGlyph = oldDefaultFont[glyphName]
        currentGlyph    = currentFont[glyphName]
        newDefaultGlyph = newDefaultFont[glyphName]

        validationGroupOldNew = assignValidationGroup(oldDefaultGlyph, newDefaultGlyph)
        if validationGroupOldNew == 'contoursEqual':
            print(f'\told default /{glyphName} is equal to new default, skipping...')
            continue

        validationGroupOldCurrent = assignValidationGroup(oldDefaultGlyph, currentGlyph)
        if validationGroupOldCurrent == 'contoursEqual':
            # current glyph is equal to old default!
            print(f'\tupdating /{glyphName} from default...')
            currentFont.insertGlyph(newDefaultGlyph, name=glyphName)
            if not fontChanged:
                fontChanged = True

    if fontChanged and not preflight:
        print('\tsaving font...')
        currentFont.save()
        currentFont.close()

    # print()
    # print('...done!\n')

def batchUpdateGlyphsFromDefault(glyphNames, ufoPaths, newDefaultPath, oldDefaultPath, preflight=False):

    newDefault = OpenFont(newDefaultPath, showInterface=False)
    oldDefault = OpenFont(oldDefaultPath, showInterface=False)

    for ufoPath in [newDefaultPath, oldDefaultPath]:
        if ufoPath in ufoPaths:
            ufoPaths.remove(ufoPath)

    for ufoPath in sorted(ufoPaths):
        font = OpenFont(ufoPath, showInterface=False)
        updateGlyphsFromDefault(font, oldDefault, newDefault, glyphNames)

    updateGlyphsFromDefault(oldDefault, oldDefault, newDefault, glyphNames, preflight=preflight)


