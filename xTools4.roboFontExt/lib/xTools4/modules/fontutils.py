'''Tools to work with fonts.'''

import os
import plistlib
from colorsys import hsv_to_rgb
from fontParts.world import OpenFont
from fontPens.penTools import distance
from xTools4.extras.fontAppTools import *

try:
    from mojo.roboFont import CurrentGlyph, CurrentFont, NewFont, RFont, RGlyph
except:
    from fontParts.world import CurrentGlyph, CurrentFont, NewFont, RFont, RGlyph

try:
    from mojo.UI import getDefault, CurrentWindow
except ModuleNotFoundError:
    # print('mojo.UI is not available in this environment')
    pass


def getGlyphs2(font, glyphNames=True, template=False):
    '''
    Return the current glyph selection in the font as a list of glyph names or glyph objects.

    Args:
        glyphNames: Return the result as a list of glyph names. If set to ``False``, return the result as a list of glyph objects.
        template: Include template glyphs in selection.

    ::

        >>> from xTools4.modules.fontutils import getGlyphs2
        >>> f = CurrentFont()
        >>> getGlyphs2(f)
        ['emacron', 'Emacron']
        >>> getGlyphs2(f, template=True)
        ['Emacron', 'emacron', 'Edotaccent', 'edotaccent']
        >>> getGlyphs2(f, glyphNames=False)
        [<RGlyph 'emacron' ('foreground') at 4778152272>, <RGlyph 'Emacron' ('foreground') at 4778372304>]

    '''

    if font is None:
        return

    window = CurrentWindow()
    if not window:
        return

    # ------------------
    # single window mode
    # ------------------

    if window.doodleWindowName == 'SingleFontWindow':

        # font selection
        if template:
            fontSelection = font.templateSelectedGlyphs
        else:
            fontSelection = font.selectedGlyphs

        # space center
        # sc = window.getSpaceCenter()
        # i = sc.glyphLineView.getSelection()
        # spaceCenterSelection = [] if i is None else [RGlyph(sc.glyphRecords[i].glyph)]

        # glyph view
        currentGlyph = RGlyph(window.getContentGlyph())

        if fontSelection:
            glyphs = fontSelection

        else:
            glyphs = [currentGlyph]

    # -----------------
    # multi window mode
    # -----------------

    elif window.doodleWindowName == 'GlyphWindow':
        glyphs = [window.getGlyph()] ### changed from [RGlyph(window.getGlyph())]

    else:
        if template:
            # WHY DO WE NEED TO CREATE NEW GLYPHS HERE?? 
            glyphs = [font.newGlyph(gn) for gn in font.templateSelectedGlyphNames]
        else:
            glyphs = list(font.selectedGlyphs)

    # done
    if glyphNames:
        return [g.name for g in glyphs]
    else:
        return glyphs

def getGlyphs(font):
    '''
    Return the current glyph selection in the font as a list of glyph names.

    - single window mode : currentGlyph AND fontSelection
    - multi-window mode : currentGlyph OR fontSelection

    .. warning::

        This function is deprecated, use :func:`getGlyphs2` instead.

    '''
    if font is None:
        return
        
    currentGlyph  = CurrentGlyph()
    fontSelection = font.selectedGlyphNames
    singleWindow  = [False, True][getDefault("singleWindowMode")]

    glyphNames = []

    if singleWindow:
        if currentGlyph is not None:
            glyphNames += [currentGlyph.name]
        glyphNames += fontSelection

    else:
        if len(fontSelection):
            glyphNames += fontSelection
        else:
            if currentGlyph is not None:
                glyphNames += [currentGlyph.name]

    # remove duplicates
    glyphNames_ = []
    for g in glyphNames:
        if g not in glyphNames_:
            glyphNames_.append(g)

    return glyphNames_

def getFontID(fontOrFontPath):
    '''
    Creates a unique font ID string in the format "familyName styleName (fontPath)".

    Args:
        fontOrFontPath (RFont or str): A font object or a path to a font file.

    Returns:
        A font ID string.

    ::

        >>> from xTools4.modules.fontutils import getFontID
        >>> f = CurrentFont()
        >>> getFontID(f)
        Publica 555A (/_fonts/Publica/_ufos/555A.ufo)

    '''

    # `fontOrFontPath` is an RFont object
    if isinstance(fontOrFontPath, RFont):
        font       = fontOrFontPath
        fontPath   = font.path
        familyName = font.info.familyName
        styleName  = font.info.styleName

    # `fontOrFontPath` is a UFO path
    elif isinstance(fontOrFontPath, str):
        fontPath      = fontOrFontPath
        infoPlistPath = os.path.join(fontPath, 'fontinfo.plist')

        with open(infoPlistPath, 'rb') as f:
            fontInfo = plistlib.load(f)

        familyName = fontInfo['familyName'] if 'familyName' in fontInfo else None
        styleName  = fontInfo['styleName']  if 'styleName'  in fontInfo else None

    # `fontOrPath` is neither a font objcect or a UFO path
    else:
        print('invalid font: %s\n' % fontOrFontPath)
        return

    # done!
    return "%s %s (%s)" % (familyName, styleName, fontPath)

def parseGString(font, gString):
    '''
    Convert an input string into a list of glyph names.

    Args:
        font (RFont): A font object.
        gString (str): A text input string.

    ::
    
        >>> from xTools4.modules.fontutils import parseGString
        >>> f = CurrentFont()
        >>> gstring = 'abc0123/a.sc/a.alt ABC'
        >>> parseGString(f, gstring)
        ['a', 'b', 'c', 'zero', 'one', 'two', 'three', 'a.sc', 'a.alt', 'A', 'B', 'C']

    '''

    # build cmap
    cmap = dict(hyperCMAP(font))

    # reverse cmap
    cmap = {v: k for k, v in cmap.items()}
    glyphNames = splitText(gString, cmap)

    return glyphNames

def isQuadratic(font):
    '''
    Check if a given font is quadratic or cubic.

    Args:
        font (RFont): A font object.

    ::
        >>> from xTools4.modules.fontutils import isQuadratic
        >>> isQuadratic(CurrentFont()))
        False
        >>> isQuadratic(OpenFont('MyFont.ttf', showInterface=False)))
        True
        >>> isQuadratic(OpenFont('MyFont.otf', showInterface=False)))
        False

    '''
    segmentTypeKey = 'com.typemytype.robofont.segmentType'
    if segmentTypeKey not in font.lib:
        return False
    segmentType = font.lib[segmentTypeKey]
    return False if segmentType == 'curve' else True

def swapGlyphs(font, glyphName1, glyphName2):
    '''Swap the contents of two glyphs in the same font.'''

    g1 = font[glyphName1].copy()
    g2 = font[glyphName2]

    font[glyphName1].prepareUndo('swap glyphs')
    font[glyphName1].clear() 
    font[glyphName1].appendGlyph(g2)
    font[glyphName1].width = g2.width
    font[glyphName1].performUndo()

    font[glyphName2].prepareUndo('swap glyphs')
    font[glyphName2].clear() 
    font[glyphName2].appendGlyph(g1)
    font[glyphName2].width = g1.width
    font[glyphName2].performUndo()

# ----------
# clear data
# ----------

def clearUnicodes(font):
    '''
    Clear unicodes of all glyphs in the font.

    ::

        from xTools4.modules.fontutils import clearUnicodes
        f = CurrentFont()
        clearUnicodes(f)

    '''
    for g in font:
        if g.unicodes:
            g.unicodes = []
            g.changed()

    font.changed()

def clearAllGuidelines(font):
    '''
    Clear all font-level and glyph-level guidelines in the font.

    ::

        from xTools4.modules.fontutils import clearAllGuidelines
        f = CurrentFont()
        clearAllGuidelines(f)

    '''
    # clear font-level guides
    font.clearGuidelines()

    # clear glyph-level guides
    for g in font:
        g.clearGuidelines()
        g.changed()

    font.changed()

# -----------
# mark colors
# -----------

def markGlyphs(font, glyphNames, color, verbose=True):
    '''
    Set mark color for a list of glyph names in the font.

    Args:
        font (RFont): A font object.
        glyphNames (list): A list of glyph names.
        color (tuple or None): A mark color as a RGBA tuple or ``None``.

    ::

        from xTools4.modules.fontutils import markGlyphs
        f = CurrentFont()
        markGlyphs(f, ['a', 'b', 'c'], (1, 0, 0, 0.3))

    '''
    if verbose:
        print('marking selected glyphs...\n')
        if color is None:
            print('\tcolor: (None)\n')
        else:
            print('\tcolor: %s, %s, %s, %s\n' % color)
        print('\t', end='')

    # mark glyphs
    for i, glyphName in enumerate(glyphNames):
        if verbose:
            if i == 0:
                print(glyphName, end='')
            else:
                print(', %s' % glyphName, end='')
        font[glyphName].markColor = color
        font[glyphName].changed()

    # done
    if verbose:
        print('\n\n...done.\n')

    font.changed()

def clearMarkColors(font):
    '''
    Clear all mark colors for all glyphs in the font.

    ::

        from xTools4.modules.fontutils import clearMarkColors
        f = CurrentFont()
        clearMarkColors(f)

    '''
    markGlyphs(font, font.keys(), None, verbose=False)

# -----------
# find glyphs
# -----------

def findMarkColor(font, color):
    '''
    Find all glyphs in the font with a given mark color.

    '''
    return [g.name for g in font if g.markColor == color]

def findContoursOnly(font):
    '''
    Find all glyphs in the font which contain only contours (no components).

    '''
    return [g.name for g in font if len(g.contours) and not len(g.components)]

def findComponentsOnly(font):
    '''
    Find all glyphs in the font which contain only components (no contours).

    '''
    return [g.name for g in font if not len(g.contours) and len(g.components)]

def findContoursAndComponents(font):
    '''
    Find all glyphs in the font which contain contours _and_ components.

    '''
    return [g.name for g in font if len(g.contours) and len(g.components)]

def findEmptyGlyphs(font):
    '''
    Find all glyphs in the font which contain neither contours nor components.

    '''
    return [g.name for g in font if not len(g.contours) and not len(g.components)]

def findOpenContours(font):
    '''
    Find all glyphs in the font which contain open contours.

    '''
    return [g.name for g in font for c in g.contours if c.open]

def findShortSegments(font, threshold=10):
    '''
    Find all glyphs in the font which contain a segment smaller than the given threshold value.

    '''
    glyphNames = []
    for glyphName in font.keys():
        for c in font[glyphName].contours:
            if glyphName in glyphNames:
                continue
            for i, bPoint in enumerate(c.bPoints):
                if i < len(c.bPoints) - 1:
                    bPointNext = c.bPoints[i+1]
                    pt1 = bPoint.anchor
                    pt2 = bPointNext.anchor
                    if not distance(pt1, pt2) < threshold:
                        continue
                    if glyphName in glyphNames:
                        continue
                    glyphNames.append(glyphName)
    return glyphNames

def findClosePoints(font, threshold=0):
    '''
    Find all glyphs in the font which contain points which are closer than the given threshold value.

    '''
    # not implemented yet
    return []

def findAttribute(font, attr, mark=True, sort=False, cluster=1):

    # collect values
    values = {}
    for glyphName in font.glyphOrder:
        g = font[glyphName]

        try:
            L = getattr(g, attr)
        except:
            continue

        # round value
        if cluster:
            L = int(L)

        if L not in values:
            values[L] = []
        values[L].append(g.name)

    if not len(values):
        return

    # process glyphs
    glyphOrder = []
    colorStep = 1.0 / (len(values) - 1)

    for i, L in enumerate(sorted(values)):
        if mark:
            hue = i * colorStep
            color = hsv_to_rgb(hue, 1, 1) + (0.5,)
        for glyphName in values[L]:
            glyphOrder.append(glyphName)
            # set mark color
            if mark:
                font[glyphName].markColor = color

    # set glyph order
    if sort:
        font.glyphOrder = glyphOrder

    # done
    return values

def findGlyphComponents(font, srcName):
    '''
    Find all components of a given glyph in the font.

    ::

        >>> from xTools4.modules.fontutils import findGlyphComponents
        >>> f = CurrentFont()
        >>> findGlyphComponents(f, 'a')
        ['aacute', 'agrave', 'atilde', 'acircumflex', 'adieresis', 'aring']

    '''
    composed = []
    for glyphName in font.glyphOrder:
        g = font[glyphName]
        if len(g.components):
            for c in g.components:
                if c.baseGlyph == srcName:
                    if glyphName not in composed:
                        composed.append(glyphName)
    return composed
