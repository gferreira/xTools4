# from importlib import reload
# import xTools4.modules.pens
# reload(xTools4.modules.pens)

# from fontPens.thresholdPen import thresholdGlyph
from fontParts.world import RGlyph
from xTools4.extras.equalize import *
from xTools4.modules.pens import LinePen


def equalizeCurves(glyph, roundPos=False):
    '''
    Balance handles of all contours in glyph.

    ::

        from xTools4.modules.optimize import equalizeCurves
        g = CurrentGlyph()
        equalizeCurves(g)
        g.changed()

    '''
    for cIndex, contour in enumerate(glyph.contours):
        for sIndex, segment in enumerate(contour.segments):
            if segment.type == "curve":
                # first pt is last pt of previous segment
                p0 = contour[sIndex-1][-1]
                if len(segment.points) == 3:
                    p1, p2, p3 = segment.points
                    p1, p2 = eqBalance(p0, p1, p2, p3)
                    if roundPos:
                        p1.round()
                        p2.round()

def curvesToLines(glyph):
    '''
    Convert all curve segments in glyph to line segments.

    ::

        from xTools4.modules.optimize import curvesToLines
        g = CurrentGlyph()
        curvesToLines(g)

    '''
    hasCurves = any([(True if s.type == 'curve' else False) for c in glyph for s in c])
    if not hasCurves:
        return
    g = RGlyph()
    drawPen = g.getPen()
    linePen = LinePen(drawPen)
    glyph.draw(linePen)
    glyph.clearContours()
    glyph.appendGlyph(g)


# def simplifyContours(glyph, tresholdValue):
#     thresholdGlyph(glyph, tresholdValue)
