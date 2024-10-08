# coding: utf-8

'''
Tools to work with linked pairs of points.

'''

#: Default key of the glyph lib where links are stored.
KEY = 'com.hipertipo.linkPoints'

def makeLink(pt1, pt2):
    '''
    Create a link between two given points.

    Args:
        pt1 (RPoint): A point.
        pt2 (RPoint): Another point in the same glyph.

    Returns:
        A tuple of two identifiers, one for each point.

    '''
    ID1 = pt1.identifier if pt1.identifier else pt1.getIdentifier()
    ID2 = pt2.identifier if pt2.identifier else pt2.getIdentifier()
    return ID1, ID2

def linkSelectedPoints(glyph):

    '''
    Create a new link between two selected points.

    Args:
        glyph (RGlyph): A glyph object.

    Returns:
        A tuple of two identifiers, one for each selected point.

    '''

    if not len(glyph.selectedPoints) == 2:
        print('please select two points')
        return

    pt1 = glyph.selectedPoints[0]
    pt2 = glyph.selectedPoints[1]

    return makeLink(pt1, pt2)

def saveLinkToLib(glyph, link, key=KEY, verbose=True):
    '''
    Save a given link to the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        link (tuple): A pair of point identifiers defining a link.
        key (str): The key to the lib where the links will be stored.

    '''
    if key not in glyph.lib:
        glyph.lib[key] = []

    if link in glyph.lib[key]:
        if verbose:
            print('link already in lib')
        return

    glyph.lib[key].append(link)

def linkPoints(glyph, key=KEY):
    '''
    Create a link between two selected points and save it in the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links will be stored.

    '''
    L = linkSelectedPoints(glyph)
    saveLinkToLib(glyph, L, key)

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

    glyph.lib[key].remove(link)

def deleteAllLinks(glyph, key=KEY):
    '''
    Delete all links from the glyph lib.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links are stored.

    '''
    if key not in glyph.lib:
        print('no lib with this key.')
        return
    glyph.lib[key] = []

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
        return []
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

def getPoint(glyph, pointID):
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

def getSelectedIDs(glyph, key=KEY):
    '''
    Get identifiers of selected points in glyph.

    Args:
        glyph (RGlyph): A glyph object.
        key (str): The key to the lib where the links are stored.

    Returns:
        A list of identifiers of selected points.

    '''
    return [pt.identifier if pt.identifier else pt.getIdentifier() for pt in glyph.selectedPoints]

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
