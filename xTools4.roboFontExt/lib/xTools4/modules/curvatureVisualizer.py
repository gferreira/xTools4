'''
Tools to visualize the curvature of Bezier segments.

Math formulas converted from `Drawing better looking curves`_.

.. _Drawing better looking curves: http://beta.observablehq.com/@dhotson/drawing-better-looking-curves

'''

from colorsys import *
from xTools4.modules.bezier import *
from drawBot import BezierPath


def makeCurvatureCombSegment(segment, steps, scale=1000):

    lines = []
    for i in range(steps + 1):
        t  = i * (1.0 / steps)
        c  = segment.curvature(t)
        n  = segment.d(t).normal().normalise() * c * -scale
        p1 = segment.position(t)
        p2 = p1 + n
        lines.append((p1, p2))

    shapes = []
    for i, (p3, p4) in enumerate(lines):
        if i == 0:
            p1, p2 = p3, p4
            continue
        P = ((p1.x, p1.y), (p2.x, p2.y), (p4.x, p4.y), (p3.x, p3.y))
        shapes.append(P)
        p1, p2 = p3, p4

    return lines, shapes

def curvatureCombSteps(glyph, steps, scale):

    B = BezierPath()
    glyph.draw(B)

    linesBezier  = []
    shapesBezier = []
    for contour in B.contours:

        lines  = []
        shapes = []
        for i, segment in enumerate(contour):

            if i == 0:
                lastPt = segment[0]
                continue

            p0 = lastPt

            if len(segment) == 3:
                p1, p2, p3 = segment
                P0, P1, P2, P3 = Point(p0), Point(p1), Point(p2), Point(p3)
                segment = BezierSegment(P0, P1, P2, P3)
                L, S = makeCurvatureCombSegment(segment, steps, scale)
            else:
                p1 = p0
                p2 = p3 = segment[0]
                L = []
                S = []

            lines.append(L)
            shapes.append(S)

            lastPt = p3

        linesBezier.append(lines)
        shapesBezier.append(shapes)

    return linesBezier, shapesBezier


class SegmentCurvatureVisualizer:

    '''An object to visualize the curvature of a Bezier segment.'''

    curvatureDraw             = False
    curvatureColor            = 1, 0, 0
    curvatureLineDash         = 2, 2
    curvatureStrokeWidth      = 1

    curvatureCombDraw         = True
    curvatureCombColor        = 0, 1, 0
    curvatureCombSteps        = 50
    curvatureCombScale        = 2500
    curvatureCombStrokeWidth  = 1
    curvatureCombStrokeWidth2 = 2

    handlesDraw               = False
    handlesColor              = 0, 0, 1
    handlesLineDash           = 2, 2
    handlesStrokeWidth        = 2

    tangentDraw               = False
    tangentColor              = 0, 0, 1
    tangentLineDash           = 2, 2
    tangentStrokeWidth        = 1

    curveDraw                 = False
    curveColor                = 0,
    curveStrokeWidth          = 3

    pointsDraw                = False
    pointsColor               = 0,
    pointsRadius              = 4

    linesAtTDraw              = False
    linesAtTColor             = 1, 0, 0
    linesAtTLineDash          = 2, 2
    linesAsTStrokeWidth       = 1

    def __init__(self, ctx):
        '''
        Initialize the object for a given context.

        Args:
            ctx (module): A drawing context (``drawBot`` or ``mojo.drawingTools``).

        '''
        self.ctx = ctx

    def _drawCurve(self, segment):
        '''
        Draw BezierPath for segment.

        '''
        p0, p1, p2, p3 = segment.p0, segment.p1, segment.p2, segment.p3

        self.ctx.save()
        self.ctx.fill(None)
        self.ctx.stroke(*self.curveColor)
        self.ctx.strokeWidth(self.curveStrokeWidth)
        self.ctx.newPath()
        self.ctx.moveTo((p0.x, p0.y))
        self.ctx.curveTo((p1.x, p1.y), (p2.x, p2.y), (p3.x, p3.y))
        self.ctx.drawPath()
        self.ctx.restore()

    def _drawPoints(self, segment, t, r=4):
        '''
        Draw a segment’s 4 points + a new point at a given ratio.

        Args:
            r (int or float): The radius for the points.

        '''
        p0, p1, p2, p3 = segment.p0, segment.p1, segment.p2, segment.p3
        pt = segment.position(t)

        self.ctx.save()
        self.ctx.stroke(None)
        self.ctx.fill(*self.pointsColor)
        self.ctx.oval(pt.x - r, pt.y - r, r*2, r*2)
        self.ctx.oval(p0.x - r, p0.y - r, r*2, r*2)
        self.ctx.oval(p3.x - r, p3.y - r, r*2, r*2)
        self.ctx.oval(p1.x - r, p1.y - r, r*2, r*2)
        self.ctx.oval(p2.x - r, p2.y - r, r*2, r*2)
        self.ctx.restore()

    def _drawHandles(self, segment):
        '''
        Draw the handles of a given segment.

        '''
        p0, p1, p2, p3 = segment.p0, segment.p1, segment.p2, segment.p3

        self.ctx.save()
        self.ctx.stroke(*self.handlesColor)
        self.ctx.lineDash(*self.handlesLineDash)
        self.ctx.fill(None)
        self.ctx.line((p0.x, p0.y), (p1.x, p1.y))
        self.ctx.line((p1.x, p1.y), (p2.x, p2.y))
        self.ctx.line((p2.x, p2.y), (p3.x, p3.y))
        self.ctx.restore()

    def _drawLinesAtT(self, segment, t):
        '''
        Draw Bezier construction lines for segment at a given ratio.

        '''
        p0, p1, p2, p3 = segment.p0, segment.p1, segment.p2, segment.p3
        a = lerp(p0, p1, t)
        b = lerp(p1, p2, t)
        c = lerp(p2, p3, t)
        d = lerp(a, b, t)
        e = lerp(b, c, t)

        self.ctx.save()
        self.ctx.lineDash(*self.linesAtTLineDash)
        self.ctx.stroke(*self.linesAtTColor)
        self.ctx.line((a.x, a.y), (b.x, b.y))
        self.ctx.line((b.x, b.y), (c.x, c.y))
        self.ctx.line((d.x, d.y), (e.x, e.y))
        self.ctx.restore()

    def _drawTangent(self, segment, t):
        '''
        Draw tangent lines for segment at a given ratio.

        '''
        pt = segment.position(t)
        pd = segment.d(t)
        p0 = pt.x - pd.x, pt.y - pd.y
        p1 = pt.x + pd.x, pt.y + pd.y
        p2 = pt.x, pt.y
        p3 = pt.x - pd.y, pt.y + pd.x

        self.ctx.save()
        self.ctx.stroke(*self.tangentColor)
        self.ctx.strokeWidth(self.tangentStrokeWidth)
        self.ctx.lineDash(*self.tangentLineDash)
        self.ctx.line(p0, p1)
        self.ctx.line(p2, p3)
        self.ctx.restore()

    def _drawCurvature(self, segment, t):
        '''
        Draw curvature for segment at a given ratio.

        '''
        r  = 1.0 / segment.curvature(t)
        n  = segment.d(t).normal().normalise() * r
        p1 = segment.position(t)
        p2 = p1 + n

        self.ctx.save()
        self.ctx.stroke(*self.curvatureColor)
        self.ctx.strokeWidth(self.curvatureStrokeWidth)
        self.ctx.lineDash(*self.curvatureLineDash)
        self.ctx.fill(None)
        self.ctx.line((p1.x, p1.y), (p2.x, p2.y))
        self.ctx.oval(p2.x - r, p2.y - r, r*2, r*2)
        self.ctx.restore()

    def _makeCurvatureComb(self, segment, steps, factor=1000):

        lines = []
        for i in range(steps + 1):
            t  = i * (1.0 / steps)
            c  = segment.curvature(t)
            n  = segment.d(t).normal().normalise() * c * -factor
            p1 = segment.position(t)
            p2 = p1 + n
            lines.append((p1, p2))

        polygons = []
        for i, (p3, p4) in enumerate(lines):
            if i == 0:
                p1, p2 = p3, p4
                continue
            P = ((p1.x, p1.y), (p2.x, p2.y), (p4.x, p4.y), (p3.x, p3.y))
            polygons.append(P)
            p1, p2 = p3, p4

        return lines, polygons

    def _drawCurvatureComb(self, lines, polygons):
        '''
        Draw curvature comb for segment.

        '''

        combFillColor = list(self.curvatureCombColor)[:3] + [0.2]

        # draw polygons

        self.ctx.save()
        self.ctx.fill(*combFillColor)
        self.ctx.stroke(None)

        for pts in polygons:
            self.ctx.polygon(*pts)

        # draw lines

        self.ctx.stroke(*self.curvatureCombColor)
        self.ctx.lineDash(None)
        self.ctx.fill(None)

        for i, (p1, p2) in enumerate(lines):
            if i == 0 or i == (len(lines) - 1):
                self.ctx.strokeWidth(self.curvatureCombStrokeWidth2)
            else:
                self.ctx.strokeWidth(self.curvatureCombStrokeWidth)
            self.ctx.line((p1.x, p1.y), (p2.x, p2.y))

        self.ctx.restore()

    def draw(self, segment, t=None):
        '''
        Draw the curvature visualization for a Bezier segment and a given ratio.

        Args:
            segment (RSegment): A Bezier segment.
            t (float): The ratio for a point in the segment.

        '''

        if self.curvatureCombDraw:
            lines, polygons = self._makeCurvatureComb(segment, self.curvatureCombSteps, self.curvatureCombScale)
            self._drawCurvatureComb(lines, polygons)

        if self.curvatureDraw and t is not None:
            self._drawCurvature(segment, t)

        if self.tangentDraw and t is not None:
            self._drawTangent(segment, t)

        if self.linesAtTDraw and t is not None:
            self._drawLinesAtT(segment, t)

        if self.handlesDraw:
            self._drawHandles(segment)

        if self.curveDraw:
            self._drawCurve(segment)

        if self.pointsDraw and t is not None:
            self._drawPoints(segment, t, r=self.pointsRadius)


class CurvatureVisualizer:

    '''
    An object to visualize the curvature of a BezierPath.

    ::

        import drawbot
        from xTools4.modules.curvatureVisualizer import CurvatureVisualizer

        B = BezierPath()
        B.oval(512, 360, 300, 300)
        B.text('g', font='IBMPlexMono-Bold', fontSize=720)

        g = CurrentGlyph()
        if g:
            g = g.copy()
            g.scaleBy(0.6)
            g.moveBy((450, 0))
            g.draw(B)

        translate(50, 250)
        fill(1, 1, 0, 0.5)
        stroke(0, 1, 1)
        strokeWidth(4)
        drawPath(B)

        V = CurvatureVisualizer(drawBot)
        V.visualizer.curvatureCombSteps = 20
        V.visualizer.curvatureCombScale = 1500
        V.visualizer.curvatureCombColor = 1, 0, 1
        V.draw(B)

    '''

    def __init__(self, ctx):
        '''
        Initialize the object for a given context.

        '''
        self.visualizer = SegmentCurvatureVisualizer(ctx)

    def setParameters(self, parameters):
        '''
        Set object attributes from a parameters dict.

        '''
        for attr, value in parameters.items():
            setattr(self.visualizer, attr, value)

    def _drawCurvatureComb(self, lines, polygons):
        for ci, c in enumerate(lines):
            for si, s in enumerate(c):
                self.visualizer._drawCurvatureComb(s, polygons[ci][si])

    def draw(self, bezierPath, t=None):
        '''
        Draw the curvature visualization for a given Bezier path.

        Args:
            bezierPath: A BezierPath object.

        '''
        for contour in bezierPath.contours:
            for i, segment in enumerate(contour):
                if i == 0:
                    lastPt = segment[0]
                    continue

                p0 = lastPt
                if len(segment) == 3:
                    p1, p2, p3 = segment
                    segment = BezierSegment(Point(p0), Point(p1), Point(p2), Point(p3))
                    self.visualizer.draw(segment, t=t)
                else:
                    p1 = p0
                    p2 = p3 = segment[0]

                lastPt = p3




class SegmentCurvatureVisualizer_Merz(SegmentCurvatureVisualizer):

    def __init__(self, container):
        self.container = container

    def _drawCurve(self, segment):
        pass

    def _drawPoints(self, segment, t, r=4):
        pass

    def _drawHandles(self, segment):
        pass

    def _drawLinesAtT(self, segment, t):
        pass

    def _drawTangent(self, segment, t):
        pass

    def _drawCurvature(self, segment, t):
        pass

    def _drawCurvatureComb(self, lines, polygons):
        c = self.curvatureCombColor
        combFillColor = c[0], c[1], c[2], 0.2

        # draw polygons
        polygonsLayer = self.container.appendPathSublayer(
            fillColor=combFillColor,
            strokeColor=None,
        )
        pen = polygonsLayer.getPen()
        for pts in polygons:
            for i, pt in enumerate(pts):
                if i == 0:
                    pen.moveTo(pt)
                else:
                    pen.lineTo(pt)
            pen.closePath()

        # draw lines
        for i, (p1, p2) in enumerate(lines):
            if i == 0 or i == (len(lines) - 1):
                sw = self.curvatureCombStrokeWidth2
            else:
                sw = self.curvatureCombStrokeWidth
            linesLayer = self.container.appendLineSublayer(
               startPoint=(p1.x, p1.y),
               endPoint=(p2.x, p2.y),
               strokeWidth=sw,
               strokeColor=self.curvatureCombColor
            )
