import os
from fontParts.world import OpenFont, RGlyph
from fontPens.digestPointPen import DigestPointPen
from defcon.pens.transformPointPen import TransformPointPen
from defcon.objects.component import _defaultTransformation
from xTools4.modules.decomposePointPen import DecomposePointPen


colorComponentsDifferent = 1.00, 0.30, 0.00, 0.35
colorComponentsEqual     = 1.00, 0.65, 0.00, 0.35
colorContoursDifferent   = 0.00, 0.65, 1.00, 0.35
colorContoursEqual       = None
colorWarning             = 1.00, 0.00, 0.00, 0.65

# ----------------------
# glyph-level validation
# ----------------------

def getSegmentTypes(glyph):
    '''
    Get a flat representation of all contour segments in a glyph, and their type.

    Returns:
        A list of 1-letter strings representing contour segments.

    WARNING: This form of representation does not account for off-curve points!

    '''
    segments = []
    for ci, c in enumerate(glyph):
        for si, s in enumerate(c.segments):
            if s.type == 'curve':
                segmentType = 'C' # cubic
            elif s.type == 'qcurve':
                segmentType = 'Q' # quadratic
            else:
                segmentType = 'L' # straight
            segments.append(segmentType)
    return segments

def getPointTypes(glyph):
    '''
    Get a flat representation of all points in a glyph, and their type.

    Returns:
        A list of strings with the type of each point: either `line`, `curve`, `qcurve`, or `offcurve`.

    '''
    return [p.type for c in glyph for p in c.points]

def getNestingLevels(g, levels=0, verbose=True):
    if g.components:
        levels += 1
        for c in g.components:
            if c.baseGlyph not in g.font:
                if verbose:
                    print(f'ERROR in "{g.name}": glyph {c.baseGlyph} not in font')
                continue
            baseGlyph = g.font[c.baseGlyph]
            levels = getNestingLevels(baseGlyph, levels)
    return levels

# compatibility

def checkAnchorsCompatible(g1, g2):
    '''
    Check if the anchors in two glyphs match.

    - same number of anchors
    - same anchor names
    - same anchor order

    Returns: `True` or `False`.

    '''
    anchors1 = [a.name for a in g1.anchors]
    anchors2 = [a.name for a in g2.anchors]
    return anchors1 == anchors2

def checkComponentsCompatible(g1, g2):
    '''
    Check if the components in two glyphs match.

    - same number of components
    - same component names
    - same component order

    Returns: `True` or `False`.

    '''
    if not len(g1.components) or not len(g2.components):
        return True
    components1 = [c.baseGlyph for c in g1.components]
    components2 = [c.baseGlyph for c in g2.components]
    return components1 == components2

def checkContoursCompatible(g1, g2):
    '''
    Check if the contours in two glyphs match.

    - same number of contours
    - same number of segments
    - same segment types
    - same number of points (implied)

    Returns: `True` or `False`.

    TO-DO: rewrite with DigestPointStructurePen
    http://doc.robofont.com/documentation/tutorials/using-pens/#digestpointstructurepen

    '''
    if len(g1) != len(g2):
        return False
    # segments1 = getSegmentTypes(g1)
    # segments2 = getSegmentTypes(g2)
    # return segments1 == segments2
    points1 = getPointTypes(g1)
    points2 = getPointTypes(g2)
    return points1 == points2

# equality

def checkEqualContours(g1, g2):
    '''
    Check if the contours in two glyphs are equal.

    - compatible points AND
    - same point positions

    Returns: `True` or `False`.

    '''
    if not len(g1) or not len(g2):
        return False

    pen1 = DigestPointPen()
    g1.drawPoints(pen1)
    pts1 = pen1.getDigest()

    pen2 = DigestPointPen()
    g2.drawPoints(pen2)
    pts2 = pen2.getDigest()

    return pts1 == pts2

def checkEqualComponents(g1, g2):
    if not len(g1.components) or not len(g2.components):
        return False

    # decompose glyphs
    _g1 = RGlyph()
    pointPen = _g1.getPointPen()
    decomposePen = DecomposePointPen(g1.font, pointPen)
    g1.drawPoints(decomposePen)
    _g1.width   = g1.width

    _g2 = RGlyph()
    pointPen = _g2.getPointPen()
    decomposePen = DecomposePointPen(g2.font, pointPen)
    g2.drawPoints(decomposePen)
    _g2.width   = g2.width

    return checkEqualContours(_g1, _g2)

def checkEqualAnchors(g1, g2):
    '''
    Check if the anchors in two glyphs are equal.

    - compatible anchors AND
    - same anchor positions

    Returns: `True` or `False`.

    '''
    if not len(g1.anchors) or not len(g2.anchors):
        return False

    anchors1 = [(a.name, (a.x, a.y)) for a in g1.anchors]
    anchors2 = [(a.name, (a.x, a.y)) for a in g2.anchors]

    return anchors1 == anchors2

def checkEqualWidth(g1, g2):
    '''
    Check if the width of two glyphs are equal.

    Returns: `True` or `False`.

    '''
    return g1.width == g2.width

def checkEqualMarginLeft(g1, g2, roundToInt=True):
    '''
    Check if the left margin of two glyphs are equal.

    Returns: `True` or `False`.

    '''
    if not g1.bounds and not g2.bounds:
        return True
    elif not g1.bounds or not g2.bounds:
        return False
    if roundToInt:
        return round(g1.leftMargin) == round(g2.leftMargin)
    else:
        return g1.leftMargin == g2.leftMargin

def checkEqualMarginRight(g1, g2, roundToInt=True):
    '''
    Check if the right margin of two glyphs are equal.

    Returns: `True` or `False`.

    '''
    if not g1.bounds and not g2.bounds:
        return True
    elif not g1.bounds or not g2.bounds:
        return False
    if roundToInt:
        return round(g1.rightMargin) == round(g2.rightMargin)
    else:
        return g1.rightMargin == g2.rightMargin

def checkEqualUnicodes(g1, g2):
    '''
    Check if the unicode(s) of two glyphs are equal.

    Returns: `True` or `False`.

    '''
    return g1.unicodes == g2.unicodes

# checkers

def validateGlyph(g1, g2, options):
    '''
    Check if two glyphs match.

    Returns:
        A dictionary of glyph attribute names and `True` or `False` results.

    DEPRECATED: use checkCompatibility and/or checkEquality instead.

    '''
    results = {}
    if options['width']:
        results['width']          = checkEqualWidth(g1, g2)
    if options['points']:
        results['points']         = checkContoursCompatible(g1, g2)
        results['pointPositions'] = checkEqualContours(g1, g2)
    if options['components']:
        results['components']     = checkComponentsCompatible(g1, g2)
    if options['anchors']:
        results['anchors']        = checkAnchorsCompatible(g1, g2)
    if options['unicodes']:
        results['unicodes']       = checkEqualUnicodes(g1, g2)
    return results

def checkGlyph(g1, g2):
    # DEPRECATED: use checkCompatibility and/or checkEquality instead.
    return {
        'width'          : checkEqualWidth(g1, g2),
        'points'         : checkContoursCompatible(g1, g2),
        'pointPositions' : checkEqualContours(g1, g2),
        'components'     : checkComponentsCompatible(g1, g2),
        'anchors'        : checkAnchorsCompatible(g1, g2),
        'unicodes'       : checkEqualUnicodes(g1, g2),
    }

def checkCompatibility(g1, g2):
    return {
        'points'     : checkContoursCompatible(g1, g2),
        'components' : checkComponentsCompatible(g1, g2),
        'anchors'    : checkAnchorsCompatible(g1, g2),
    }

def checkEquality(g1, g2):
    return {
        'width'      : checkEqualWidth(g1, g2),
        'left'       : checkEqualMarginLeft(g1, g2),
        'right'      : checkEqualMarginRight(g1, g2),
        'points'     : checkEqualContours(g1, g2),
        'components' : checkEqualComponents(g1, g2),
        'anchors'    : checkEqualAnchors(g1, g2),
        'unicodes'   : checkEqualUnicodes(g1, g2),
    }

# ---------------------
# font-level validation
# ---------------------

def validateFont(f1, f2, options):
    '''
    Check if the *glyphs* in two fonts match.

    TO-DO: add checks for font-level data?

      - font dimensions
      - vertical metrics
      - kerning groups
      - kerning pairs/values

    Returns:
        A string with a report of all differences found.

    '''
    txt = f"validating '{f1.info.familyName} {f1.info.styleName}'...\n\n"
    for gName in f1.glyphOrder:
        if gName not in f2:
            txt += f'\t{gName}:\n'
            txt += f"\t- glyph not in font\n"
            txt += '\n'
            continue
        checks = validateGlyph(f1[gName], f2[gName], options)
        if 'pointPositions' in checks:
            del checks['pointPositions']
        if not all(checks.values()):
            txt += f'\t{gName}:\n'
            for check, result in checks.items():
                if result is False:
                    txt += f"\t- {check} not matching\n"
            txt += '\n'

    return txt

def validateFonts(targetFonts, sourceFont, options):
    '''
    Batch check if all fonts in `targetFonts` match the ones in sourceFont.

    Returns:
        A string with a report of all differences found in all fonts.

    '''
    txt = ''
    for targetFont in targetFonts:
        txt += validateFont(targetFont, sourceFont, options)
    return txt

def validateFont2(f1, f2, width=True, points=True, components=True, anchors=True, unicodes=True):
    '''
    Check if the *glyphs* in two fonts match.

    Returns:
        A dict with check results for each glyph in the target font.

    '''
    results = {}
    for gName in f1.glyphOrder:
        if gName not in g1 or gName not in f2:
            continue
        checks = validateGlyph(f1[gName], f2[gName])
        results[gName] = {}
        for check, result in checks.items():
            results[gName][check] = result
    return results

def validateFonts2(targetFonts, sourceFont, width=True, points=True, components=True, anchors=True, unicodes=True):
    '''
    Check if the *glyphs* in target fonts match with glyphs in a reference font.

    Returns:
        A dict with check results for each glyph in each target font.

    '''
    results = {}
    for targetFont in targetFonts:
        fileName = os.path.splitext(os.path.split(targetFont.path)[-1])[0]
        results[fileName] = validateFont2(targetFont, sourceFont, width=width, points=points, components=components, anchors=anchors, unicodes=unicodes)
    return results

def applyValidationColors(font, defaultFont, colors=None, glyphNames=None):

    if colors is None:
        colors = {
            'components'      : colorComponentsDifferent,
            'componentsEqual' : colorComponentsEqual,
            'default'         : colorContoursEqual,
            'warning'         : colorWarning,
        }

    if glyphNames is None:
        glyphNames = font.glyphOrder

    for glyphName in glyphNames:
        currentGlyph = font[glyphName]
        currentGlyph.markColor = None

        if glyphName not in defaultFont:
            continue

        defaultGlyph = defaultFont[glyphName]

        results = {
            'compatibility' : checkCompatibility(currentGlyph, defaultGlyph),
            'equality'      : checkEquality(currentGlyph, defaultGlyph),
        }

        if currentGlyph.components:
            levels = getNestingLevels(currentGlyph)
            # warning: nested components of mixed contour/components
            if levels > 1 or len(currentGlyph.contours):
                currentGlyph.markColor = colors['warning']
            else:
                # components equal to default
                if all(results['compatibility']) and results['equality']['components']:
                    currentGlyph.markColor = colors['componentsEqual']
                # components different from default
                else:
                    currentGlyph.markColor = colors['components']
        else:
            if results['compatibility']['points'] and results['equality']['points']:
                # contours equal to default
                if font.path != defaultFont.path:
                    currentGlyph.markColor = colors['default']
                # contours different from default
                else:
                    currentGlyph.markColor = None

    font.changed()

# ----------------------
# designspace validation
# ----------------------

# DEPRECATED: use `validateFonts` instead

def validateDesignspace(designspace):
    txt = 'validating designspace...\n\n'
    defaultSrc = designspace.findDefault()
    defaultFont = OpenFont(defaultSrc.path, showInterface=False)
    txt += f'\tdefault source: {defaultSrc.filename}\n\n'
    for src in designspace.sources:
        if src == defaultSrc:
            continue
        srcFont = OpenFont(src.path, showInterface=False)
        txt += f'\tchecking {src.filename}...\n\n'
        for gName in defaultFont.glyphOrder:
            g1 = srcFont[gName]
            g2 = defaultFont[gName]
            checks = validateGlyph(g1, g2)
            if not all(checks.values()):
                txt += f'\t\t{gName}:\n'
                for check, result in checks.items():
                    if result is False:
                        txt += f"\t\t- {check} not matching\n"
                txt += '\n'
        srcFont.close()
    txt += '...done.\n\n'
    return txt

