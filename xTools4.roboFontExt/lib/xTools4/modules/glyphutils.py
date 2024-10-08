'''Tools to work with glyphs.'''

import operator
import math

from fontPens.guessSmoothPointPen import GuessSmoothPointPen
from fontParts.world import RGlyph

def autoStartPoints(glyph):
    '''
    Automatically set starting points in a glyph’s contours.

    '''
    if not glyph.bounds:
        return

    # glyph.prepareUndo('auto start points')

    for contour in glyph:
        points = [(pt.x, pt.y, pt) for pt in contour.points if pt.type != 'offcurve']
        sortedPoints = sorted(points, key=operator.itemgetter(1, 0))
        firstPoint = sortedPoints[0][2]
        startSegmentIndex = [i for i, segment in enumerate(contour) if firstPoint in segment.points][0]
        contour.setStartSegment(startSegmentIndex)

    glyph.changed()
    # glyph.performUndo()

def getOriginPosition(glyph, posName):
    '''
    Get a position based on the glyph bounds and a named reference point.

    Args:
        glyph (RGlyph): A glyph object.
        posName (str): The name of a reference point. Supported keywords: `topLeft`, `topCenter`, `topRight`, `middleLeft`, `middleCenter`, `middleRight`, `bottomLeft`, `bottomCenter`, `bottomRight`.

    Returns:
        A position as a tuple of (x,y) values.

    ::

        >>> from hTools3.modules.glyphutils import getOriginPosition
        >>> getOriginPosition(CurrentGlyph(), 'middleCenter')
        (243.5, 237.5)

    '''
    if not glyph.bounds:
        return
    left, bottom, right, top = glyph.bounds
    center = left   + (right - left)   * 0.5
    middle = bottom + (top   - bottom) * 0.5
    positions = {
        'topLeft'      : (left,   top),
        'topCenter'    : (center, top),
        'topRight'     : (right,  top),
        'middleLeft'   : (left,   middle),
        'middleCenter' : (center, middle),
        'middleRight'  : (right,  middle),
        'bottomLeft'   : (left,   bottom),
        'bottomCenter' : (center, bottom),
        'bottomRight'  : (right,  bottom),
    }
    if posName not in positions:
        return
    return positions[posName]

def deselectPoints(glyph):
    '''
    Deselect all points in a glyph.

    '''
    for c in glyph.contours:
        for p in c.points:
            p.selected = False

def selectPointsLine(glyph, pos, axis='x', side=0):
    '''
    Select all points below/above a given position.

    Args:
        glyph (RGlyph): A glyph object.
        pos (int or float): The position of an imaginary line.
        axis (str): The selection axis perpendicular to the line. (*x* or *y*)
        side (int): The side of the selection in relation to the line. ``0``: smaller or ``1``: greater than pos.

    ::

        from hTools3.modules.glyphutils import selectPointsLine
        glyph = CurrentGlyph()
        selectPointsLine(glyph, 300, axis='x', side=1)

    '''
    for c in glyph.contours:
        for p in c.points:
            value = p.x if axis == 'x' else p.y
            if not side:
                if value <= pos:
                    p.selected = True
            else:
                if value >= pos:
                    p.selected = True

def shiftSelectedPoints(glyph, delta, axis='x'):
    '''
    Shift all selected points along one axis by a given amount of units.

    Args:
        glyph (RGlyph): A glyph object.
        delta (int or float): The distance to move the selected points.
        axis (str): The axis along which to move the selected points.

    ::

        g = CurrentGlyph()
        g.prepareUndo('shift points')
        deselectPoints(g)
        selectPointsLine(g, 200, axis='y', side=0)
        shiftSelectedPoints(g, -100, axis='y')
        g.changed()
        g.performUndo()

    '''
    for c in glyph.contours:
        for p in c.selectedPoints:
            if axis == 'x':
                p.x += delta
            else:
                p.y += delta

def setSmoothPoints(glyph):
    if len(glyph) == 0:
        return glyph
    result = RGlyph()
    pen = GuessSmoothPointPen(result.getPointPen())
    glyph.drawPoints(pen)
    glyph.clearContours()
    glyph.appendGlyph(result)

# --------
# rounding
# --------

def roundPoints(glyph, gridSize):
    '''
    Round all point positions to a given grid.

    '''
    for contour in glyph.contours:
        for pt in contour.points:
            pt.x = round(pt.x / gridSize) * gridSize
            pt.y = round(pt.y / gridSize) * gridSize

def roundBPoints(glyph, gridSize):
    '''
    Round all bPoint positions to a given grid.

    '''
    for contour in glyph.contours:
        for bPoint in contour.bPoints:
            x, y = bPoint.anchor
            x = round(x / gridSize) * gridSize
            y = round(y / gridSize) * gridSize
            bPoint.anchor = x, y

def roundAnchors(glyph, gridSize):
    '''
    Round all anchor positions to a given grid.

    '''
    for anchor in glyph.anchors:
        anchor.x = round(anchor.x / gridSize) * gridSize
        anchor.y = round(anchor.y / gridSize) * gridSize

def roundComponents(glyph, gridSize):
    '''
    Round all components positions to a given grid.

    '''
    for component in glyph.components:
        x, y = component.offset
        x = round(x / gridSize) * gridSize
        y = round(y / gridSize) * gridSize
        component.offset = x, y

def roundMargins(glyph, gridSize):
    '''
    Round the margins of a glyph to a given grid.

    '''
    if glyph.bounds is None:
        return
    L, B, R, T  = glyph.bounds
    leftMargin  = round(glyph.leftMargin / gridSize) * gridSize
    rightMargin = round(glyph.rightMargin / gridSize) * gridSize
    width = leftMargin + (R - L) + rightMargin
    glyph.leftMargin = leftMargin
    glyph.width = width

def roundWidth(glyph, gridSize):
    '''
    Round the glyph width to a given grid.

    '''
    glyph.width = round(glyph.width / gridSize) * gridSize

# ----------
# glyph name
# ----------

def hasSuffix(glyph, suffix):
    '''
    Check if a glyph's name has a given ``suffix``.

    '''
    hasSuffix = False
    nameParts = glyph.name.split(".")

    # check for suffix
    if len(nameParts) == 2:
        if nameParts[1] == suffix:
            hasSuffix = True

    # check for no suffix
    else:
        if len(nameParts) == 1 and len(suffix) == 0:
            hasSuffix = True

    return hasSuffix

def changeSuffix(glyph, oldSuffix, newSuffix=None):
    '''
    Create a new glyph name with a different suffix.

    Args:
        glyph (RGlyph): A glyph object.
        oldSuffix (str): The old suffix to be replaced.
        newSuffix (str or None): The new suffix to be used in place of the old one.

    Returns:
        A new glyph name with a modified or removed suffix.

    '''
    baseName = glyph.name.split(".")[0]

    # replace suffix
    if newSuffix is not None:
        newName = "%s.%s" % (baseName, newSuffix)

    # clear suffix
    else:
        newName = baseName

    return newName

def renameGlyphSuffix(glyph, oldSuffix, newSuffix, overwrite=False, duplicate=False, verbose=True):
    '''
    Add, remove or modify a glyph name’s suffix.

    Args:
        glyph (RGlyph): A glyph object.
        oldSuffix (str): The old suffix to be replaced.
        newSuffix (str or None): The new suffix to be used in place of the old one.
        overwrite (bool): If a glyph with the new name already exist in the parent font, overwrite it (or not).
        duplicate (bool): Keep the original glyph with the old suffix name.

    '''

    # glyph does not have suffix
    if not hasSuffix(glyph, oldSuffix):
        return

    # switch suffixes : one.osf -> one.onum
    if len(oldSuffix) > 0 and len(newSuffix) > 0:
        newName = changeSuffix(glyph, oldSuffix, newSuffix)

    # remove suffix : one.osf -> one
    elif len(oldSuffix) > 0 and len(newSuffix) == 0:
        newName = changeSuffix(glyph, oldSuffix, None)

    # add suffix : one -> one.onum
    elif len(oldSuffix) == 0 and len(newSuffix) > 0:
        newName = '%s.%s' % (glyph.name, newSuffix)

    # don't change glyph name
    else:
        newName = glyph.name
        return

    # rename glyph
    renameGlyph(glyph, newName, overwrite=overwrite, duplicate=duplicate, verbose=verbose)

def renameGlyph(glyph, newName, overwrite=False, duplicate=False, verbose=True):

    if newName == glyph.name:
        return

    # get font
    font = glyph.font

    # orphan glyph, rename directly
    if font is None:
        glyph.name = newName
        glyph.changed()
        return

    # check for existing glyphs
    if newName in glyph.layer:

        # don't overwrite existing glyph
        if not overwrite:
            print("'%s' already exists in font, skipping..." % newName)
            return

        # delete existing glyph (overwrite)
        print("deleting '%s'..." % newName)
        glyph.layer.removeGlyph(newName)
        glyph.layer.changed()

    # rename glyph
    if not duplicate:
        if verbose:
            print("renaming '%s' as '%s'..." % (glyph.name, newName))
        glyph.name = newName
        glyph.changed()

    # rename as duplicate
    else:
        if verbose:
            print("duplicating '%s' as '%s'..." % (glyph.name, newName))
        glyph.layer.insertGlyph(glyph, name=newName)
        glyph.layer.changed()

def findReplaceGlyphName(glyph, findText, replaceText, overwrite=False, duplicate=False, verbose=True):

    if not findText in glyph.name:
        return

    # make new name
    newName = glyph.name.replace(findText, replaceText)

    # rename glyph
    renameGlyph(glyph, newName, overwrite=overwrite, duplicate=duplicate, verbose=verbose)

def addToGlyphName(glyph, addText, suffix=True, overwrite=False, duplicate=False, verbose=True):

    if not len(addText):
        return

    # make new name
    newName = glyph.name + addText if suffix else addText + glyph.name

    # rename glyph
    renameGlyph(glyph, newName, overwrite=overwrite, duplicate=duplicate, verbose=verbose)

# -------
# metrics
# -------

def setGlyphWidth(glyph, widthValue, positionMode='do not move'):
    '''
    Transform the width of a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        widthValue (int): A value to be used as input in the width modification.
        positionMode (str): The position mode. `center glyph`, `split margins`, `relative split` or ``None`` (do not move).

    ::

        from hTools3.modules.glyphutils import setGlyphWidth
        g = CurrentGlyph()
        setGlyphWidth(g, 700, 'relative split')

    '''
    # glyph is empty (no margins)
    if not len(glyph):
        glyph.width = widthValue
        return

    widthNew = widthValue
    leftOld  = glyph.leftMargin
    rightOld = glyph.rightMargin
    widthOld = glyph.width
    boxWidth = glyph.width - (glyph.leftMargin + glyph.rightMargin)

    # center glyph
    if positionMode == 'center glyph':
        glyph.width = widthNew
        centerGlyph(glyph)

    # split difference
    elif positionMode == 'split margins':
        try:
            diff = widthNew - widthOld
            leftNew = leftOld + (diff * 0.5)
        except:
            leftNew = 0
        glyph.leftMargin = leftNew
        glyph.width = widthNew

    # split relative
    elif positionMode == 'relative split':
        try:
            whitespace = widthNew - boxWidth
            leftNew = whitespace / (1 + (rightOld / leftOld))
        except:
            leftNew = 0
        glyph.leftMargin = leftNew
        glyph.width = widthNew

    # do not move
    else:
        glyph.width = widthNew

def centerGlyph(glyph, useSlantAngle=True, verbose=False):
    '''
    Center the glyph inside its advance width.

    ::

        from hTools3.modules.glyphutils import centerGlyph
        g = CurrentGlyph()
        centerGlyph(g)

    '''
    if glyph.bounds is None:
        return

    left, right, width = glyph.leftMargin, glyph.rightMargin, glyph.width
    whitespace = left + right
    leftNew = whitespace * 0.5


    if glyph.font is not None:
        angle = 0 if glyph.font.info.italicAngle is None else glyph.font.info.italicAngle
        if useSlantAngle and angle != 0:
            L, B, R, T = glyph.bounds
            xOffset = math.tan(angle * math.pi / 180) * B
            leftNew -= xOffset
            # apply slant offset ?
            slantOffset = glyph.font.lib.get("com.typemytype.robofont.italicSlantOffset")
            if slantOffset:
                leftNew += slantOffset

    if leftNew == left:
        return

    # center glyph
    glyph.prepareUndo('center glyph')
    glyph.leftMargin = leftNew
    glyph.width = width
    if verbose:
        print(f'centering {glyph.name} ({glyph.layer.name})...')
    glyph.performUndo()

# ------
# points
# ------

def getPointFromBPoint(bPoint):
    '''
    Get a Point for a given bPoint.

    ::

        >>> from hTools3.modules.glyphutils import getPointFromBPoint
        >>> glyph = CurrentGlyph()
        >>> bPoint = glyph.contours[0].bPoints[0]
        >>> print(bPoint)
        <RBPoint corner anchor='(315, 0)' at 4579032720>
        >>> pt = getPointFromBPoint(bPoint)
        >>> print(pt)
        <RPoint line (315, 0) at 4535967248>

    '''
    return bPoint._point

def getBPointFromPoint(point):
    '''
    Get a bPoint for a given point.

    ::

        >>> from hTools3.modules.glyphutils import getBPointFromPoint
        >>> glyph = CurrentGlyph()
        >>> pt = glyph.contours[0].points[0]
        >>> print(pt)
        <RPoint line (315, 0) at 4535965072>
        >>> bPoint = getBPointFromPoint(pt)
        >>> print(bPoint)
        <RBPoint corner anchor='(315, 0)' at 4535965840>

    '''
    from fontParts.fontshell import RBPoint

    bPoint = RBPoint()
    bPoint._setPoint(point)
    bPoint.contour = point.contour

    return bPoint

def getPointAtIndex(glyph, ptIndex):
    '''Get the point at the given linear point index.

    Args:
        glyph (RGlyph): A glyph object.
        ptIndex (int): A point index.

    Returns:
        An `RPoint` object, or `None` if the glyph does not a point at this index.

    '''
    n = 0
    points = {}
    for ci, c in enumerate(glyph.contours):
        for pi, p in enumerate(c.points):
            points[n] = ci, pi
            n += 1

    if ptIndex not in points:
        return

    ci, pi = points[ptIndex]
    return glyph.contours[ci].points[pi]

def getPointByID(glyph, pointID):
    point = None
    for c in glyph.contours:
        for pt in c.points:
            if pt.getIdentifier() == pointID:
                point = pt
                break
    return point

