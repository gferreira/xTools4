'''
Tools to visualize the structure of Bezier curves.

'''

from math import atan, degrees
from drawBot import BezierPath

# ---------
# functions
# ---------

def getAngle(p1, p2):
    '''
    Get the angle between two points (in degrees).

    '''
    # unpack x,y tuples
    x1, y1 = p1
    x2, y2 = p2

    # get catheti (aka legs)
    w = x2 - x1
    h = y2 - y1

    # get angle (in degrees)
    if w != 0:
        angleRadians = atan(float(h) / w)
        angleDegrees = degrees(angleRadians)
    else:
        angleDegrees = 0

    return angleDegrees

# -------
# objects
# -------

class BezierStructureVisualizer:

    '''
    import drawBot
    from xTools4.modules.structureVisualizer import BezierStructureVisualizer

    g = CurrentGlyph()
    B = BezierStructureVisualizer(drawBot)
    B.scale = 1.4
    B.strokeWidthSegments = 5
    B.strokeWidthHandles = 5
    B.draw(g, (80, 200))

    '''

    scale                = 1.0
    strokeWidthSegments  = 2
    strokeWidthHandles   = 2
    colorCurves          = 0.0, 0.0, 1.0
    colorLines           = 0.0, 0.5, 1.0
    colorHandlesStraight = 1.0, 0.0, 0.0
    colorHandlesSlanted  = 1.0, 0.5, 0.0
    multiplyMode         = False

    def __init__(self, ctx):
        self.ctx = ctx

    def drawFill(self, glyph):
        self.ctx.fill(0.9)
        self.ctx.drawGlyph(glyph)

    def _structure(self, glyph):

        _lineSegments    = []
        _curveSegments   = []
        _handlesStraight = []
        _handlesSlanted  = []

        for ci, contour in enumerate(glyph.contours):

            # get segments
            for si, segment in enumerate(contour.segments):
                if len(segment) == 3:
                    p1 = glyph.contours[ci][(si-1)][-1]
                    p2, p3, p4 = segment
                    _curveSegments.append(( (p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y) ))
                else:
                    p1 = glyph.contours[ci][(si-1)][-1]
                    p2 = segment[-1]
                    _lineSegments.append(( (p1.x, p1.y), (p2.x, p2.y) ))

            # get handles
            for pt in contour.bPoints:
                ptIn  = pt.anchor[0] + pt.bcpIn[0],  pt.anchor[1] + pt.bcpIn[1]
                ptOut = pt.anchor[0] + pt.bcpOut[0], pt.anchor[1] + pt.bcpOut[1]
                angleIn  = getAngle(pt.anchor, ptIn)
                angleOut = getAngle(pt.anchor, ptOut)
                # straight
                if angleIn == 0:
                    _handlesStraight.append((pt.anchor, ptIn))
                else:
                    _handlesSlanted.append((pt.anchor, ptIn))
                if angleOut == 0:
                    _handlesStraight.append((pt.anchor, ptOut))
                else:
                    _handlesSlanted.append((pt.anchor, ptOut))

        return _lineSegments, _curveSegments, _handlesStraight, _handlesSlanted

    def _lineSegments(self, glyph):
        B = []
        for ci, contour in enumerate(glyph.contours):
            for si, segment in enumerate(contour.segments):
                if len(segment) == 1:
                    p1 = glyph.contours[ci][(si-1)][-1]
                    p2 = segment[-1]
                    B.append( ( (p1.x, p1.y), (p2.x, p2.y) ) )
        return B

    def _curveSegments(self, glyph):
        B = []
        for ci, contour in enumerate(glyph.contours):
            for si, segment in enumerate(contour.segments):
                if len(segment) == 3:
                    p1 = glyph.contours[ci][(si-1)][-1]
                    p2, p3, p4 = segment
                    B.append( ( (p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y) ) )
        return B

    def _handlesStraight(self, glyph):
        B = []
        for ci, contour in enumerate(glyph.contours):
            for pt in contour.bPoints:
                ptIn  = pt.anchor[0] + pt.bcpIn[0],  pt.anchor[1] + pt.bcpIn[1]
                ptOut = pt.anchor[0] + pt.bcpOut[0], pt.anchor[1] + pt.bcpOut[1]
                angleIn  = getAngle(pt.anchor, ptIn)
                angleOut = getAngle(pt.anchor, ptOut)
                if angleIn == 0:
                    B.append((pt.anchor, ptIn))

                if angleOut == 0:
                    B.append((pt.anchor, ptOut))

        return B

    def _handlesSlanted(self, glyph):
        B = []
        for ci, contour in enumerate(glyph.contours):
            for pt in contour.bPoints:
                ptIn  = pt.anchor[0] + pt.bcpIn[0],  pt.anchor[1] + pt.bcpIn[1]
                ptOut = pt.anchor[0] + pt.bcpOut[0], pt.anchor[1] + pt.bcpOut[1]
                angleIn  = getAngle(pt.anchor, ptIn)
                angleOut = getAngle(pt.anchor, ptOut)
                if angleIn != 0:
                    B.append((pt.anchor, ptIn))
                if angleOut != 0:
                    B.append((pt.anchor, ptOut))
        return B

    def drawSegments(self, glyph):
        lineSegments  = self._lineSegments(glyph)
        curveSegments = self._curveSegments(glyph)
        self.ctx.fill(None)
        self.ctx.strokeWidth(self.strokeWidthSegments)

        self.ctx.stroke(*self.colorCurves)
        for p1, p2 in lineSegments:
            self.ctx.newPath()
            self.ctx.moveTo(p1)
            self.ctx.lineTo(p2)
            self.ctx.drawPath()

        self.ctx.stroke(*self.colorLines)
        for p1, p2, p3, p4 in curveSegments:
            self.ctx.newPath()
            self.ctx.moveTo(p1)
            self.ctx.curveTo(p2, p3, p4)
            self.ctx.drawPath()

    def drawHandles(self, glyph):
        straightHandles = self._handlesStraight(glyph)
        slantedHandles  = self._handlesSlanted(glyph)
        self.ctx.fill(None)
        self.ctx.strokeWidth(self.strokeWidthHandles)

        self.ctx.stroke(*self.colorHandlesStraight)
        for p1, p2 in straightHandles:
            self.ctx.newPath()
            self.ctx.moveTo(p1)
            self.ctx.lineTo(p2)
            self.ctx.drawPath()

        self.ctx.stroke(*self.colorHandlesSlanted)
        for p1, p2 in slantedHandles:
            self.ctx.newPath()
            self.ctx.moveTo(p1)
            self.ctx.lineTo(p2)
            self.ctx.drawPath()

    def draw(self, glyph, pos=(0, 0)):
        self.ctx.translate(*pos)
        self.ctx.scale(self.scale)
        self.ctx.lineCap('round')
        if self.multiplyMode:
            try:
                self.ctx.blendMode('multiply')
            except:
                pass
        self.drawFill(glyph)
        self.drawHandles(glyph)
        self.drawSegments(glyph)
