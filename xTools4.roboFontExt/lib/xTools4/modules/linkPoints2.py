import json
from math import sqrt, tan, pi, radians
from fontParts.fontshell.point import RPoint

'''
Tools to make various kinds of measurements in a font.

# based on xTools4.modules.linkPoints

'''

KEY = 'com.xTools4.measurements'


def angledPoint(point, angle):
    x, y = point
    d = tan(radians(angle)) * y
    return x - d, y

def offsetAngledPoint(point, angle, offset):
    x, y = angledPoint(point, -angle)
    return x - offset, y


def getPointAtIndex(glyph, ptIndex, isDefcon=False):
    '''Get the point at the given linear point index.

    Supports "ghost points" for left/right edges.

    Args:
        glyph (RGlyph): A glyph object.
        ptIndex (int): A point index.

    Returns:
        An `RPoint` object.

    '''
    n = 0
    points = {}
    for ci, c in enumerate(glyph):
        pointsList = c.points if not isDefcon else c
        for pi, p in enumerate(pointsList):
            points[n] = ci, pi
            n += 1

    offset = glyph.font.lib.get('com.typemytype.robofont.italicSlantOffset')

    # n+1 : right margin
    if ptIndex > len(points)-1:
        P = RPoint()
        P.x = glyph.width
        P.y = 0
        if offset:
            P.x += offset
        return P

    # -1 : left margin
    if ptIndex < 0:
        P = RPoint()
        P.x = 0
        P.y = 0
        if offset:
            P.x += offset
        return P

    # get point at index
    ci, pi = points[ptIndex]
    return glyph[ci].points[pi] if not isDefcon else glyph[ci][pi]

def getAnchorPoint(font, anchor):
    '''
    A -> ascender
    B -> baseline
    C -> capheight
    D -> descender
    X -> xheight
    '''
    P = RPoint()
    P.x = 0
    if anchor == 'X':
        P.y = font.info.xHeight
    elif anchor == 'C':
        P.y = font.info.capHeight
    elif anchor == 'D':
        P.y = font.info.descender
    elif anchor == 'A':
        P.y = font.info.ascender
    else: # baseline
        P.y = 0

    # angle  = font.info.italicAngle
    # offset = font.lib.get('com.typemytype.robofont.italicSlantOffset') or 0
    # if angle or offset:
    #     x, y = offsetAngledPoint((P.x, P.y), angle, offset)
    #     P.x = x

    return P

def getIndexForPoint(glyph, pt):
    '''Get the linear point index for a given point.

    Args:
        glyph (RGlyph): A glyph object.
        pt (RPoint): A point.

    Returns:
        An integer.

    '''
    n = 0
    for ci, c in enumerate(glyph):
        for pi, p in enumerate(c.points):
            if p == pt:
                return n
            n += 1

def getPointFromID(glyph, pointID):
    '''
    Get point object from a point identifier.

    Args:
        glyph (RGlyph): A glyph object.
        pointID (str): A point identifier.

    Returns:
        A point object (RPoint).

    '''
    for contour in glyph:
        for pt in contour.points:
            if pt.identifier == pointID:
                return pt

def getSelectedIDs(glyph):
    '''
    Get identifiers of selected points in glyph.

    Args:
        glyph (RGlyph): A glyph object.

    Returns:
        A list of identifiers of selected points.

    '''
    return [pt.identifier if pt.identifier else pt.getIdentifier() for pt in glyph.selectedPoints]

def getDistance(p1, p2, direction=None):
    '''
    Get the distance between two points.

    Args:
        p1 and p2 (tuple): The position of a point as a pair of `x, y` values.
        direction (str): A x/y constrain direction for the measurement (optional).

    Returns:
        The distance as number of font units.

    '''
    if direction == 'x':
        value = p2[0] - p1[0]
    elif direction == 'y':
        value = p2[1] - p1[1]
    else:
        value = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    return abs(value)

### GLYPH-LEVEL MEASUREMENT

def linkSelectedPoints(glyph, verbose=True):
    '''
    Create a new link between two selected points.

    Args:
        glyph (RGlyph): A glyph object.

    Returns:
        A tuple of two identifiers, one for each selected point.

    '''
    def makeLink(glyph, pt1, pt2):
        index1 = getIndexForPoint(glyph, pt1)
        index2 = getIndexForPoint(glyph, pt2)
        return index1, index2

    if not len(glyph.selectedPoints) == 2:
        if verbose:
            print('please select two points')
        return

    pt1 = glyph.selectedPoints[0]
    pt2 = glyph.selectedPoints[1]

    return makeLink(glyph, pt1, pt2)

def saveLinkToLib(glyph, link, name=None, direction=None, key=KEY, verbose=True):
    '''
    Save a given link to the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        link (tuple): A pair of point indexes defining a link.
        name (str): The name of the link. (optional)
        direction (str): The direction of the measurement (x/y/a).
        key (str): The key to the lib where the links will be stored.

    '''
    if key not in glyph.lib:
        glyph.lib[key] = {}

    if link in glyph.lib[key] or reversed(link) in glyph.lib[key]:
        if verbose:
            print('link already in lib')
        return

    linkID = f'{link[0]} {link[1]}'
    glyph.lib[key][linkID] = {}

    if verbose:
        print(f'saving link "{linkID}" to the glyph lib ({glyph.name})...')

    if name is not None:
        glyph.lib[key][linkID]['name'] = name

    if direction is not None:
        glyph.lib[key][linkID]['direction'] = direction

def linkPoints(glyph, name=None, direction=None, key=KEY):
    '''
    Create a link between two selected points and save it in the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        name (str): The name of the link.
        direction (str): The direction of the measurement (x/y). ### TO-DO: add angled
        key (str): The key to the lib where the links will be stored.

    '''
    L = linkSelectedPoints(glyph)
    if L is None:
        return
    saveLinkToLib(glyph, L, name=name, direction=direction, key=key)

def deleteLink(glyph, link, key=KEY):
    '''
    Delete the given link from the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        link (tuple): A pair of point identifiers defining a link.
        key (str): The key to the lib where the links are stored.

    '''
    if key not in glyph.lib:
        print('no lib with this key.')
        return

    if link not in glyph.lib[key]:
        print('link not in lib.')
        return

    del glyph.lib[key][link]

def deleteAllLinks(glyph, key=KEY):
    '''
    Delete all links from the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links are stored.

    '''
    if key not in glyph.lib:
        # print('no lib with this key.')
        return
    glyph.lib[key] = {}

def deleteSelectedLinks(glyph, key=KEY):
    '''
    Delete selected links from the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links are stored.

    '''
    allLinks = set(getLinks(glyph))
    selectedLinks = set(getSelectedLinks(glyph))
    newLinks = allLinks.difference(selectedLinks)
    setLinks(glyph, list(newLinks))

def getLinks(glyph, key=KEY):
    '''
    Get all links in glyph.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links are stored.

    Returns:
        A list of all links in the glyph.

    '''
    if key not in glyph.lib:
        return {}
    return glyph.lib[key]

def setLinks(glyph, links, key=KEY):
    '''
    Store the given links in the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        links (list): A list of links as tuples of point identifiers.
        key (str): The key to the lib where the links are stored.

    '''
    glyph.lib[key] = links

def getSelectedLinks(glyph, key=KEY):
    '''
    Get selected links in glyph.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links are stored.

    Returns:
        A list of links which are selected in the glyph.

    '''
    links = getLinks(glyph)
    IDs = getSelectedIDs(glyph)
    return [(ID1, ID2) for ID1, ID2 in links if (ID1 in IDs or ID2 in IDs)]

makeGlyphMeasurementID          = linkSelectedPoints
saveGlyphMeasurement            = saveLinkToLib
newGlyphMeasurement             = linkPoints
deleteGlyphMeasurement          = deleteLink
clearGlyphMeasurements          = deleteAllLinks
getSelectedGlyphMeasurements    = getSelectedLinks
deleteSelectedGlyphMeasurements = deleteSelectedLinks

# single-point measurements

def newMeasurePoint(glyph, name=None, direction=None, key=KEY):
    if not len(glyph.selectedPoints) == 1:
        if verbose:
            print('please select one point')
        return

    selectedPoint = glyph.selectedPoints[0]
    ptIndex = getIndexForPoint(glyph, selectedPoint)
    saveMeasurePointToLib(glyph, ptIndex, name=name, direction=direction, key=KEY)

def saveMeasurePointToLib(glyph, ptIndex, name=None, direction=None, key=KEY, verbose=True):
    if key not in glyph.lib:
        glyph.lib[key] = {}

    if type(ptIndex) is not str:
        ptIndex = str(ptIndex)

    glyph.lib[key][ptIndex] = {}

    if verbose:
        print(f'saving point measurement "{ptIndex}" to the glyph lib ({glyph.name})...')

    if direction is not None:
        glyph.lib[key][ptIndex]['direction'] = direction

    if name is not None:
        glyph.lib[key][ptIndex]['name'] = name

### FONT-LEVEL MEASUREMENT

def saveLinkToLib_font(font, name, link, key=KEY, verbose=True):

    if key not in font.lib:
        font.lib[key] = {}

    if verbose:
        print(f'saving link "{name}" to the font lib ({font.info.familyName} {font.info.styleName})...')

    if name not in font.lib[key]:
        font.lib[key][name] = {}

    for k, v in link.items():

        if k is None or v is None:
            continue

        k, v = str(k), str(v)

        if k == '<null>' or v == '<null>':
            continue

        font.lib[key][name][k] = v

def deleteLink_font(font, name, key=KEY):
    pass

def deleteAllLinks_font(font, key=KEY):
    pass

def getLinks_font(font, key=KEY):
    if key not in font.lib:
        return {}
    return font.lib[key]

# def setLinks_font(font, links, key=KEY):
#     font.lib[key] = links

### IMPORT / EXPORT

def exportMeasurements(font, jsonPath, verbose=True, key=KEY):
    '''
    Export measurement data from the current font as an external JSON file.

    '''
    # get font measurements
    fontMeasurements = getLinks_font(font, key=key)

    # get glyph measurements
    glyphsMeasurements = {}
    for glyphName in font.glyphOrder:
        if glyphName not in font:
            continue
        glyphMeasurements = getLinks(font[glyphName], key=key)
        if not len(glyphMeasurements):
            continue
        glyphsMeasurements[glyphName] = glyphMeasurements

    # combine font & glyph measurements into a single dict
    measurementsDict = {
        'font'   : fontMeasurements,
        'glyphs' : glyphsMeasurements,
    }

    # save measurements dict as a JSON file
    if verbose:
        print(f'exporting measurements to {jsonPath}...')

    with open(jsonPath, 'w', encoding='utf-8') as f:
        json.dump(measurementsDict, f, indent=2)

    if verbose:
        print('...done.\n')

def readMeasurements(jsonPath):
    '''
    Read measurement data from external JSON file into a dict.

    '''
    with open(jsonPath, 'r', encoding='utf-8') as f:
        measurementsDict = json.load(f)

    return measurementsDict

def importMeasurements(font, jsonPath, verbose=True, key=KEY):
    '''
    Import measurement data from external JSON file into the current font.

    '''
    if verbose:
        print(f'importing measurements from {jsonPath}...')

    measurements = readMeasurements(jsonPath)

    # store measurements in font lib
    if verbose:
        print('\timporting font measurements...')
    font.lib[key] = measurements['font']

    # store measurements in glyph libs
    if verbose:
        print('\timporting glyph measurements...')
    for glyphName in measurements['glyphs'].keys():
        if glyphName not in font:
            continue
        font[glyphName].lib[key] = measurements['glyphs'][glyphName]

    if verbose:
        print('...done.\n')

