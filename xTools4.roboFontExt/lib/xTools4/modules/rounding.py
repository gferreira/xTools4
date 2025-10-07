from math import sin, cos, atan2, degrees, radians, sqrt
from fontTools.pens.pointPen import AbstractPointPen
from fontParts.world import RGlyph


def getSelectedPointIndexes(glyph):
    '''Get selected points as tuples of (contourIndex, pointIndex).'''
    selection = []
    index = 0
    for ci, contour in enumerate(glyph.contours):
        for pi, pt in enumerate(contour.points):
            if pt.selected:
                selection.append((ci, pi))
    return selection

def getDistance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    w = p2[0] - p1[0]
    h = p2[1] - p1[1]
    return sqrt(w ** 2 + h ** 2)

def getAngle(p1, p2):
    ang1 = atan2(p2[1]-p1[1], p2[0]-p1[0])
    return degrees(ang1)

def vector(pos, distance, angle):
    x, y = pos
    x += cos(radians(angle)) * distance
    y += sin(radians(angle)) * distance
    return x, y


class RoundingCapPointPen(AbstractPointPen):

    def __init__(self, otherPointPen, selection, points, mode=0):
        select1, select2 = selection

        # selected points must be in the same contour
        assert select1[0] == select2[0]

        # non-adjacent points: assume it’s the last and first
        # TO-DO: make sure that points are really adjacent
        self.isEdgeCase = False
        if not select2[1] - select1[1] == 1:
            select1, select2 = select2, select1
            self.isEdgeCase = True

        self.otherPointPen = otherPointPen
        self.selection = [select1, select2]
        self.mode = mode
        self._currentContourIndex = 0
        self._currentPointIndex = 0
        self._points = points

    def beginPath(self, identifier=None, **kwargs):
        self.otherPointPen.beginPath(**kwargs)

    def endPath(self):
        self._currentPointIndex = 0
        self._currentContourIndex += 1
        self.otherPointPen.endPath()

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):

        if (self._currentContourIndex, self._currentPointIndex) in self.selection:

            select1, select2 = self.selection

            if self.mode == 0:

                self.otherPointPen.addPoint(pt, segmentType, smooth, name, **kwargs)
                self.otherPointPen.addPoint(pt, None)
                self.otherPointPen.addPoint(pt, None)
                self.otherPointPen.addPoint(pt, 'qcurve')

            else:
                # skip 1st selected point, draw both when handling the 2nd
                if (self._currentContourIndex, self._currentPointIndex) != select2:

                    # get the original points
                    _pt1 = self._points[select1[0]][select1[1]]
                    _pt2 = self._points[select2[0]][select2[1]]

                    # get previous and next points
                    index_prev = (select1[1] - 1) % len(self._points[select1[0]])
                    index_next = (select2[1] + 1) % len(self._points[select2[0]])
                    _pt1_prev = self._points[select1[0]][index_prev]
                    _pt2_next = self._points[select2[0]][index_next]

                    # calculate the middle point
                    midX = _pt1[0] + (_pt2[0] - _pt1[0]) / 2
                    midY = _pt1[1] + (_pt2[1] - _pt1[1]) / 2
                    midPt = midX, midY

                    # get angles between original points and prev/next points
                    angle1 = getAngle(_pt1, _pt1_prev)
                    angle2 = getAngle(_pt2, _pt2_next)

                    # get radius as distance from original point to mid point
                    radius = getDistance(_pt1, midPt)

                    # calculate new positions for the original points
                    pt1 = vector(_pt1, radius, angle1)
                    pt2 = vector(_pt2, radius, angle2)

                    # calculate positions of BCP handles
                    pt1_bcpInX  =  pt1[0] + ( _pt1[0]  - pt1[0]  ) / 2
                    pt1_bcpInY  =  pt1[1] + ( _pt1[1]  - pt1[1]  ) / 2
                    pt1_bcpOutX = _pt1[0] + ( midPt[0] - _pt1[0] ) / 2
                    pt1_bcpOutY = _pt1[1] + ( midPt[1] - _pt1[1] ) / 2
                    pt2_bcpInX  = _pt2[0] + ( midPt[0] - _pt2[0] ) / 2
                    pt2_bcpInY  = _pt2[1] + ( midPt[1] - _pt2[1] ) / 2
                    pt2_bcpOutX =  pt2[0] + ( _pt2[0]  - pt2[0]  ) / 2
                    pt2_bcpOutY =  pt2[1] + ( _pt2[1]  - pt2[1]  ) / 2
                    pt1_bcpIn   = pt1_bcpInX,  pt1_bcpInY
                    pt1_bcpOut  = pt1_bcpOutX, pt1_bcpOutY
                    pt2_bcpIn   = pt2_bcpInX,  pt2_bcpInY
                    pt2_bcpOut  = pt2_bcpOutX, pt2_bcpOutY

                    # finally, add all the new points
                    self.otherPointPen.addPoint(pt1, segmentType, smooth, name, **kwargs)
                    self.otherPointPen.addPoint(pt1_bcpIn, None)
                    self.otherPointPen.addPoint(pt1_bcpOut, None)
                    self.otherPointPen.addPoint(midPt, 'qcurve')

                    self.otherPointPen.addPoint(midPt, 'line')
                    self.otherPointPen.addPoint(pt2_bcpIn, None)
                    self.otherPointPen.addPoint(pt2_bcpOut, None)
                    self.otherPointPen.addPoint(pt2, 'qcurve')

        # repeat any unselected point
        else:
            self.otherPointPen.addPoint(pt, segmentType, smooth, name, **kwargs)

        self._currentPointIndex += 1

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        self.otherPointPen.addComponent(baseGlyphName, transformation, identifier)


class RoundingCornerPointPen(AbstractPointPen):

    def __init__(self, otherPointPen, selection, points, mode=0, radius=100):
        self.otherPointPen = otherPointPen
        self.selection = selection
        self.mode = mode
        self.radius = radius
        self._currentContourIndex = 0
        self._currentPointIndex = 0
        self._points = points

    def beginPath(self, identifier=None, **kwargs):
        self.otherPointPen.beginPath(**kwargs)

    def endPath(self):
        self._currentPointIndex = 0
        self._currentContourIndex += 1
        self.otherPointPen.endPath()

    def addPoint(self, pt, segmentType=None, smooth=False, name=None, **kwargs):

        if (self._currentContourIndex, self._currentPointIndex) == self.selection:

            if self.mode == 0:
                self.otherPointPen.addPoint(pt, segmentType, smooth, name, **kwargs)
                self.otherPointPen.addPoint(pt, None)
                self.otherPointPen.addPoint(pt, None)
                self.otherPointPen.addPoint(pt, 'qcurve')

            else:
                index_prev = (self.selection[1] - 1) % len(self._points[self.selection[0]])
                index_next = (self.selection[1] + 1) % len(self._points[self.selection[0]])

                _pt_prev = self._points[self.selection[0]][index_prev]
                _pt_next = self._points[self.selection[0]][index_next]

                anglePrev = getAngle(pt, _pt_prev)
                angleNext = getAngle(pt, _pt_next)

                pt_prev = vector(pt, self.radius, anglePrev)
                pt_next = vector(pt, self.radius, angleNext)

                pt_bcpInX = pt[0] + (pt_prev[0] - pt[0]) / 2
                pt_bcpInY = pt[1] + (pt_prev[1] - pt[1]) / 2
                pt_bcpIn = pt_bcpInX, pt_bcpInY

                pt_bcpOutX = pt[0] + (pt_next[0] - pt[0]) / 2
                pt_bcpOutY = pt[1] + (pt_next[1] - pt[1]) / 2
                pt_bcpOut = pt_bcpOutX, pt_bcpOutY

                self.otherPointPen.addPoint(pt_prev, segmentType, True, name, **kwargs)
                self.otherPointPen.addPoint(pt_bcpIn, None)
                self.otherPointPen.addPoint(pt_bcpOut, None)
                self.otherPointPen.addPoint(pt_next, 'qcurve', True)

        # repeat any unselected point
        else:
            self.otherPointPen.addPoint(pt, segmentType, smooth, name, **kwargs)

        self._currentPointIndex += 1

    def addComponent(self, baseGlyphName, transformation, identifier=None):
        self.otherPointPen.addComponent(baseGlyphName, transformation, identifier)


def addRoundingCorner(srcGlyph, mode=0, radius=100):

    srcGlyph.prepareUndo('add new points for rounded corner')
    dstGlyph = RGlyph()
    dstPen = dstGlyph.getPointPen()
    selection = getSelectedPointIndexes(srcGlyph)

    if len(selection) == 1:
        points = []
        for c in srcGlyph.contours:
            points.append([(p.x, p.y) for p in c.points])

        roundingPen = RoundingCornerPointPen(dstPen, selection[0], points, mode, radius=radius)
        srcGlyph.drawPoints(roundingPen)
        dstGlyph.width = srcGlyph.width
        srcGlyph.clearContours()
        srcGlyph.appendGlyph(dstGlyph)

    srcGlyph.performUndo()


def addRoundingCap(srcGlyph, mode=0):

    srcGlyph.prepareUndo('add new points for rounded stroke cap')
    dstGlyph = RGlyph()
    dstPen = dstGlyph.getPointPen()
    selection = getSelectedPointIndexes(srcGlyph)

    if len(selection) == 2:
        points = []
        for c in srcGlyph.contours:
            points.append([(p.x, p.y) for p in c.points])

        roundingPen = RoundingCapPointPen(dstPen, selection, points, mode)
        srcGlyph.drawPoints(roundingPen)
        dstGlyph.width = srcGlyph.width

        # fix mismatched start point in edge case - this should be done by the pen!
        if mode == 1 and roundingPen.isEdgeCase:
            contour = dstGlyph.contours[selection[0][0]]
            contour.setStartSegment(4)

        srcGlyph.clearContours()
        srcGlyph.appendGlyph(dstGlyph)

    srcGlyph.performUndo()
