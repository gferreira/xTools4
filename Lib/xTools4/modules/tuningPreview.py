import os, glob
import drawBot as DB
from fontTools.ufoLib.glifLib import glyphNameToFileName
from ufoProcessor.ufoOperator import UFOOperator
from mojo.roboFont import RGlyph
from xTools4.modules.glyphutils import drawGlyph
from xTools4.modules.measurements import *
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


def _drawVerticalMetrics(pos, yMetrics, scale_, guidesColor=(0.85,)):
    x, y = pos
    with DB.savedState():
        DB.stroke(*guidesColor)
        for _y in yMetrics:
            DB.line((0, y + _y * scale_), (DB.width(), y + _y * scale_))

def _drawGlyph(glyph, pos, scale_, label, points=True, index=True, color=(0.5,), drawFill=True, radius=7):

    x, y = pos
    r = radius

    with DB.savedState():
        DB.stroke(*color, 0.5)
        for _x in [0, glyph.width]:
            DB.line((x + _x * scale_, 0), (x + _x * scale_, DB.height()))

    DB.save()
    DB.translate(x, y)
    DB.scale(scale_)

    with DB.savedState():
        if drawFill:
            DB.fill(*color, 0.2)
            DB.stroke(None)
        else:
            DB.fill(None)
            DB.stroke(*color, 0.5)
        drawGlyph(glyph)

    if points:
        with DB.savedState():
            DB.fill(*color)
            DB.stroke(None)
            DB.font('Menlo')
            DB.fontSize(28)
            n = 0
            for c in glyph.contours:
                for p in c.points:
                    DB.oval(p.x-r, p.y-r, r*2, r*2)
                    if index:
                        DB.text(str(n), (p.x, p.y-36), align='center')
                    n += 1

    with DB.savedState():
        DB.fill(*color)
        DB.fontSize(81)
        DB.text(label, (glyph.width/2, -400), align='center')

    DB.restore()

def _drawMeasurements(glyph, glyphMeasurements, pos, scale_):

    measurementsColor = 0,
    measurementsDash = 3, 12
    measurementsStrokeWidth = 5

    DB.save()
    DB.translate(*pos)
    DB.scale(scale_)
    DB.strokeWidth(measurementsStrokeWidth)
    DB.stroke(*measurementsColor)
    DB.lineDash(*measurementsDash)
    DB.lineCap('round')

    for ID, m in glyphMeasurements.items():
        pt1_index, pt2_index = ID.split()
        try:
            pt1 = getPointAtIndex(glyph, int(pt1_index))
        except:
            pt1 = getAnchorPoint(glyph.font, pt1_index)
        try:
            pt2 = getPointAtIndex(glyph, int(pt2_index))
        except:
            pt2 = getAnchorPoint(glyph.font, pt2_index)

        if pt1 is None or pt2 is None:
            print(pt1, pt2)
            continue

        DB.line((pt1.x, pt1.y), (pt2.x, pt2.y))

    DB.restore()

def _drawDeltas(glyph1, glyph2, pos, scale_, matchingPoints=None, color=None):

    DB.save()
    DB.translate(*pos)
    DB.scale(scale_)
    DB.strokeWidth(5)
    DB.lineCap('round')

    if not matchingPoints: # assume matching point indexes
        matchingPoints = []
        for ci, c in enumerate(glyph1.contours):
            for pi, p in enumerate(c.points):
                matchingPoints.append( ((ci, pi), (ci, pi)) )

    for mp1, mp2 in matchingPoints:
        ci1, pi1 = mp1
        ci2, pi2 = mp2
        p1 = glyph1.contours[ci1].points[pi1]
        p2 = glyph2.contours[ci2].points[pi2]

        if color is not None:
            DB.stroke(*color)
        else:
            if p1.x == p2.x or p1.y == p2.y:
                DB.stroke(*colorCheckTrue)
            else:
                DB.stroke(*colorCheckFalse)

        if p1.x == p2.x and p1.y == p2.y:
            continue

        DB.line((p1.x, p1.y), (p2.x, p2.y))

    DB.restore()


class TuningPreview:

    #: origin position
    x, y = 100, 220

    #: page size
    width, height = 5000, 1000

    #: glyph scale
    scale = 0.42

    #: margin between glyphs
    margin = 100

    color1 = 0, 1, 1
    color2 = 1, 0, 1

    def __init__(self, controller, referenceSource):
        self.controller = controller
        self.referenceSource = referenceSource

    def draw(self, glyphName, level=1):

        self.glyphName = glyphName

        x, y = self.x, self.y
        s = self.scale

        glyphDefault = self.controller.defaultFont[glyphName]

        yMetrics = set([
            self.controller.defaultFont.info.descender,
            0,
            self.controller.defaultFont.info.xHeight,
            self.controller.defaultFont.info.capHeight,
            self.controller.defaultFont.info.ascender
        ])

        referenceFont = OpenFont(self.referenceSource, showInterface=False)
        glyphReference = referenceFont[glyphName]

        # transfer glyph measurements to reference font
        glyphMeasurementsReference = transferGlyphMeasurements(self.controller.measurements['glyphs'][glyphName], glyphDefault, glyphReference)

        DB.newDrawing()
        DB.newPage(self.width, self.height)
        DB.blendMode('multiply')

        _drawVerticalMetrics((x, y), yMetrics, s)
        _drawGlyph(glyphDefault, (x, y), s, 'default')
        _drawMeasurements(glyphDefault, self.controller.measurements['glyphs'][glyphName], (x, y), s)

        x += glyphDefault.width * s + self.margin

        _drawGlyph(glyphReference, (x, y), s, 'reference')
        _drawMeasurements(glyphReference, glyphMeasurementsReference, (x, y), s)

        operator = UFOOperator()
        operator.read(self.controller.designspacePath)
        operator.loadFonts()

        referenceSources = {'_'.join(k.split('_')[1:]): OpenFont(v, showInterface=False) for k, v in self.controller.referenceSources.items()}

        for styleName, ufoPath in self.controller.tuningSources.items():
            styleNameParts = styleName.split('_')

            if len(styleNameParts) > level:
                continue

            # get blended glyph (parametric)
            blendedLocation = { part[:4]: int(part[4:]) for part in styleNameParts }
            parametricLocation = getEffectiveLocation(self.controller.designspacePath, blendedLocation)
            blendedGlyph = RGlyph(instantiateGlyph(operator, glyphName, parametricLocation))

            # get reference glyph
            blendedReference = referenceSources[styleName][glyphName]

            # make tuning glyph
            matchingPoints = getMatchingPoints(glyphDefault, glyphReference)
            tuningGlyph = makeTuningGlyph(blendedGlyph, blendedReference, glyphDefault, matchingPoints)

            # draw page
            x, y = self.x, self.y
            DB.newPage(self.width, self.height)
            DB.blendMode('multiply')
            _drawVerticalMetrics((x, y), yMetrics, s)    
            _drawGlyph(blendedGlyph, (x, y), s, styleName, color=self.color1)

            x += blendedGlyph.width * s + self.margin

            _drawGlyph(blendedReference, (x, y), s, 'reference', color=self.color2)

            x += blendedReference.width * s + self.margin
            
            _drawGlyph(blendedGlyph, (x, y), s, 'diff', points=True, index=False, color=self.color1, drawFill=False)
            _drawGlyph(blendedReference, (x, y), s, 'diff', points=True, index=False, color=self.color2, drawFill=False)
            _drawDeltas(blendedGlyph, blendedReference, (x, y), s, matchingPoints=matchingPoints, color=(0, 0, 1))

            x += max(blendedGlyph.width, blendedReference.width) * s + self.margin 

            _drawGlyph(tuningGlyph, (x, y), s, 'tuning', points=True, index=False, drawFill=False)
            _drawGlyph(glyphDefault, (x, y), s, '', points=False, index=False, drawFill=True)
            _drawDeltas(tuningGlyph, glyphDefault, (x, y), s)

    def save(self, folder, fileName):

        glifName = os.path.splitext(glyphNameToFileName(self.glyphName, None))[0]
        pdfFileName = f'{fileName}_{glifName}.pdf'

        if not os.path.exists(folder):
            os.makedirs(folder)

        pdfPath = os.path.join(folder, pdfFileName)

        print(f'saving {pdfFileName}...', end=' ')

        DB.saveImage(pdfPath)

        print(os.path.exists(pdfPath))
