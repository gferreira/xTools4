measurementsPathKey       = 'com.xTools4.xProject.measurementsPath'
smartSetsPathKey          = 'com.xTools4.xProject.smartSetsPath'
glyphConstructionsPathKey = 'com.xTools4.xProject.glyphConstructionsPath'
referenceFontPathKey      = 'com.xTools4.xProject.referenceFontPath'


def makeParentAxis(parentName, parametricAxes, defaultName, matchRangeAxes):
    r'''
    Calculate a parent axis to control several parametric axes,
    with mappings to limit the range of each child axis.

    ::
        parentName  = 'XTRA'
        parametricAxes = {
            'XTUC' : dict(minimum=72, maximum=668, default=400),
            'XTUR' : dict(minimum=60, maximum=902, default=561),
            'XTUD' : dict(minimum=76, maximum=686, default=410),
            'XTLC' : dict(minimum=42, maximum=500, default=243),
            'XTLR' : dict(minimum=46, maximum=625, default=337),
            'XTLD' : dict(minimum=84, maximum=501, default=248),
            'XTFI' : dict(minimum=40, maximum=604, default=329),
        }
        defaultName = 'XTUC'
        matchRangeAxes = {
            'XQUC' : 'XTUR',
            'XQLC' : 'XTLR',
            'XQFI' : 'XTFI',
        }

        parentAxis, mappings = makeParentAxis(parentName, parametricAxes, defaultName, matchRangeAxes)

        print('parent parametric axis:')
        print(parentAxis)
        print()
        print('parent mappings to child parameters:')
        for parentValue, mapping in sorted(mappings.items()):
            print(f'\t{ parentValue } { mapping }')

    '''


    defaultValue = parametricAxes[defaultName]['default']
    minValues = []
    maxValues = []
    for axisName, axis in parametricAxes.items():
        # SKIP MATCHED RANGE AXES
        if axisName in matchRangeAxes:
            continue
        axisShift = defaultValue - axis['default']
        minValue  = axis['minimum'] + axisShift
        maxValue  = axis['maximum'] + axisShift
        minValues.append(minValue)
        maxValues.append(maxValue)

    parentAxis = {
        'name'    : parentName,
        'default' : defaultValue,
        'minimum' : min(minValues),
        'maximum' : max(maxValues),
    }

    mappingValues = set(minValues + maxValues)
    mappings = {}
    for mappingValue in sorted(mappingValues):
        mappings[mappingValue] = {}
        for axisName, axis in parametricAxes.items():
            # SKIP MATCHED RANGE AXES
            if axisName in matchRangeAxes:
                continue
            axisShift = defaultValue - axis['default']
            value = mappingValue - axisShift
            mappings[mappingValue][axisName] = value

    # ADD AXES WITH MATCHED RANGES

    for mappingValue, maps in mappings.items():
        for axisName, mapAxisName in matchRangeAxes.items():
            if mapAxisName in maps:

                axisDefault = parametricAxes[axisName]['default']
                axisMinimum = parametricAxes[axisName]['minimum']
                axisMaximum = parametricAxes[axisName]['maximum']

                mapAxisDefault = parametricAxes[mapAxisName]['default']
                mapAxisMinimum = parametricAxes[mapAxisName]['minimum']
                mapAxisMaximum = parametricAxes[mapAxisName]['maximum']

                mapAxisValue = maps[mapAxisName]

                if mappingValue < defaultValue:
                    axisRange = axisDefault    - axisMinimum
                    mapRange  = mapAxisDefault - mapAxisMinimum
                    mapScale  = axisRange / mapRange
                    mapValue  = (mapAxisValue - mapAxisMinimum) * mapScale
                    axisValue = axisMinimum + mapValue

                elif mappingValue > defaultValue:
                    axisRange = axisMaximum    - axisDefault
                    mapRange  = mapAxisMaximum - mapAxisDefault
                    mapScale  = axisRange / mapRange
                    mapValue  = (mapAxisValue - mapAxisDefault) * mapScale
                    axisValue = axisDefault + mapValue

                maps[axisName] = int(axisValue)

    return parentAxis, mappings

def updateGlyphsFromDefault(currentFont, oldDefaultFont, newDefaultFont, glyphNames, preflight=False):
    name = os.path.splitext(os.path.split(currentFont.path)[-1])[0].split('_')[-1]
    fontChanged = False
    for glyphName in glyphNames:
        if glyphName not in oldDefaultFont or glyphName not in currentFont or glyphName not in newDefaultFont:
            continue

        print(familyName, subFamilyName, name)

        oldDefaultGlyph = oldDefaultFont[glyphName]
        currentGlyph    = currentFont[glyphName]
        newDefaultGlyph = newDefaultFont[glyphName]

        validationGroupOldNew = assignValidationGroup(oldDefaultGlyph, newDefaultGlyph)
        if validationGroupOldNew == 'contoursEqual':
            print(familyName, subFamilyName, name)
            print(f'old default /{glyphName} is equal to new default, skipping...')
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
        font.save()
        font.close()

    print()

def batchUpdateGlyphsFromDefault(ufoPaths, newDefaultPath, oldDefaultPath, preflight=False):

    newDefault = OpenFont(newDefaultPath, showInterface=False)
    oldDefault = OpenFont(oldDefaultPath, showInterface=False)

    ufoPaths.remove(newDefaultPath)
    ufoPaths.remove(oldDefaultPath)

    for ufoPath in sorted(ufoPaths):
        font = OpenFont(ufoPath, showInterface=False)
        updateGlyphsFromDefault(font, oldDefault, newDefault, glyphNames)

    updateGlyphsFromDefault(oldDefault, oldDefault, newDefault, glyphNames, preflight=preflight)

