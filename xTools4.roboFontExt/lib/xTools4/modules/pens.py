import os
from fontTools.pens.basePen import BasePen
from defcon.pens.transformPointPen import TransformPointPen
from defcon.objects.component import _defaultTransformation


class LinePen(BasePen):

    '''
    A pen which converts curve segments into line segments.

    ::

        from xTools4.modules.pens import LinePen

        dstGlyph = RGlyph()
        dstPen = dstGlyph.getPen()
        linePen = LinePen(dstPen)

        srcGlyph = CurrentGlyph()
        srcGlyph.draw(linePen)
        srcGlyph.clearContours()
        srcGlyph.appendGlyph(dstGlyph)

    '''

    def __init__(self, otherPen):
        BasePen.__init__(self, {})
        self.otherPen = otherPen
        self.currentPt = None
        self.firstPt = None

    def _moveTo(self, pt):
        self.otherPen.moveTo(pt)
        self.currentPt = pt
        self.firstPt = pt

    def _lineTo(self, pt):
        self.otherPen.lineTo(pt)
        self.currentPt = pt

    def _curveToOne(self, pt1, pt2, pt3):
        self.otherPen.lineTo(pt3)
        self.currentPt = pt3

    def _closePath(self):
        self.lineTo(self.firstPt)
        self.otherPen.closePath()
        self.currentPt = None

    def _endPath(self):
        self.otherPen.endPath()
        self.currentPt = None

    def addComponent(self, glyphName, transformation):
        self.otherPen.addComponent(glyphName, transformation)


class DecomposePointPen:

    '''
    A pen which decomposes components into contours.

    ::

        from xTools4.modules.pens import DecomposePointPen

        # get srcGlyph from current font or closed ufo

        dstGlyph = RGlyph()
        pointPen = dstGlyph.getPointPen()
        decomposePen = DecomposePointPen(srcGlyph.font, pointPen)
        srcGlyph.drawPoints(decomposePen)
        dstGlyph.width   = srcGlyph.width
    
        # insert dstGlyph into a font or layer

    '''

    def __init__(self, glyphSet, outPointPen):
        self._glyphSet = glyphSet
        self._outPointPen = outPointPen
        self.beginPath = outPointPen.beginPath
        self.endPath = outPointPen.endPath
        self.addPoint = outPointPen.addPoint

    def addComponent(self, baseGlyphName, transformation, *args, **kwargs):
        if baseGlyphName in self._glyphSet:
            baseGlyph = self._glyphSet[baseGlyphName]
            if transformation == _defaultTransformation:
                baseGlyph.drawPoints(self)
            else:
                transformPointPen = TransformPointPen(self, transformation)
                baseGlyph.drawPoints(transformPointPen)
