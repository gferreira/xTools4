import drawBot as DB
from fontParts.world import OpenFont
from xTools4.modules.linkPoints2 import getPointAtIndex, getAnchorPoint
from xTools4.modules.measurements import Measurement


class MeasurementsViewer:

    margin          = 20
    fontSize        = 12
    fontSizeLabels  = 9
    lineHeight      = 1.5
    fontSizePoints  = 6
    fontSizeTitle   = 48
    fontSizeSection = 36
    glyphScale      = 0.19

    colorMeasurementLink  = 1, 0, 0
    colorGlyphShapeFill   = 0.9,
    colorGlyphShapeStroke = 0.85,
    colorGlyphMetrics     = 0.85,

    def __init__(self, measurements, fontPath):
        self.measurements = measurements
        self.font = OpenFont(fontPath, showInterface=False)

    @property
    def fontMeasurements(self):
        return self.measurements['font']

    @property
    def glyphMeasurements(self):
        return self.measurements['glyphs']

    @property
    def title(self):
        return self.font.info.familyName

    @property
    def boxSize(self):
        w, h = DB.sizes()['A4Landscape']
        return h - self.margin * 2

    def glyphOrigin(self, glyph):
        x = (self.boxSize - (glyph.width * self.glyphScale)) / 2
        y = self.boxSize * 0.27
        return x, y

    def drawFontMeasurementInfo(self, measurementName, measurement):
        x = self.boxSize + self.margin * 2
        y = DB.height() - self.margin - self.fontSize * 0.7

        attrs = ['description', 'direction', 'glyph 1', 'point 1', 'glyph 2', 'point 2']

        txt = DB.FormattedString()
        txt.fontSize(self.fontSize)
        txt.lineHeight(self.fontSize * self.lineHeight)
        txt.paragraphBottomSpacing(None)
        txt.append(f'{measurementName}\n')
        txt.fontSize(self.fontSizeLabels)
        txt.lineHeight(self.fontSizeLabels * self.lineHeight)
        txt.paragraphBottomSpacing(5)
        txt.append('name\n')

        for attr in attrs:
            txt.fontSize(self.fontSize)
            txt.lineHeight(self.fontSize * self.lineHeight)
            txt.paragraphBottomSpacing(None)
            txt.append(f'{measurement[attr]}\n')
            txt.fontSize(self.fontSizeLabels)
            txt.lineHeight(self.fontSizeLabels * self.lineHeight)
            txt.paragraphBottomSpacing(5)
            txt.append(f'{attr}\n')

        M = Measurement(
            measurementName,
            measurement['direction'],
            measurement['glyph 1'], measurement['point 1'],
            measurement['glyph 2'], measurement['point 2'],
        )
        distanceUnits   = M.measure(self.font)
        distancePermill = round(distanceUnits * 1000 / self.font.info.unitsPerEm)

        for key, value in {'units': distanceUnits, 'permill': distancePermill}.items():
            txt.fontSize(self.fontSize)
            txt.lineHeight(self.fontSize * self.lineHeight)
            txt.paragraphBottomSpacing(None)
            txt.append(f'{value}\n')
            txt.fontSize(self.fontSizeLabels)
            txt.lineHeight(self.fontSizeLabels * self.lineHeight)
            txt.paragraphBottomSpacing(5)
            txt.append(f'{key}\n')

        # parent = measurement.get('parent')
        # if not parent.strip():
        #     parent  = '—'
        #     scale_p = '—'
        # else:
        #     scale_p = 1.0

        #     # get parent value
        #     distanceParent = None
        #     for m in self.fontMeasurements.keys():
        #         if m['name'] == parent:
        #             distanceParent = i['units']
        #     # calculate p-scale
        #     if distanceParent:
        #         scaleParent = item['units'] / distanceParent
        #         item['scale_p'] = scaleParent

        # txt.fontSize(self.fontSize)
        # txt.lineHeight(self.fontSize * self.lineHeight)
        # txt.paragraphBottomSpacing(None)
        # txt.append(f'{parent}\n')
        # txt.fontSize(self.fontSizeLabels)
        # txt.lineHeight(self.fontSizeLabels * self.lineHeight)
        # txt.paragraphBottomSpacing(5)
        # txt.append('parent\n')

        # txt.fontSize(self.fontSize)
        # txt.lineHeight(self.fontSize * self.lineHeight)
        # txt.paragraphBottomSpacing(None)
        # txt.append(f'{scale_p}\n')
        # txt.fontSize(self.fontSizeLabels)
        # txt.lineHeight(self.fontSizeLabels * self.lineHeight)
        # txt.paragraphBottomSpacing(5)
        # txt.append('p-scale\n')

        DB.text(txt, (x, y))

    def drawGlyphMetrics(self, glyph):
        s = self.glyphScale
        x, y = self.glyphOrigin(glyph)
        W = H = self.boxSize

        vmetrics = set([
            0,
            self.font.info.xHeight,
            self.font.info.descender,
            self.font.info.ascender,
            self.font.info.capHeight,
        ])
        DB.translate(self.margin, self.margin)
        DB.stroke(*self.colorGlyphMetrics)
        DB.strokeWidth(1)
        for vy in vmetrics:
            DB.line((0, y + vy * s), (W, y + vy * s))
        for vx in [0, glyph.width * s]:
            DB.line((x + vx, 0), (x + vx, H))

    def drawMeasurementDirection(self, pt1, pt2, direction):
        if direction == 'x':
            P1 = pt1.x, pt1.y
            P2 = pt2.x, pt1.y
        elif direction == 'y':
            P1 = pt2.x, pt1.y
            P2 = pt2.x, pt2.y
        else: # angled
            P1 = pt1.x, pt1.y
            P2 = pt2.x, pt2.y
        DB.lineDash(None)
        DB.strokeWidth(100000)
        c = self.colorMeasurementLink + (0.1,)
        DB.stroke(*c)
        DB.line(P1, P2)

    def drawGlyphShape(self, glyph):
        DB.strokeWidth(1 / self.glyphScale)
        DB.stroke(*self.colorGlyphShapeStroke)
        DB.fill(*self.colorGlyphShapeFill)
        DB.drawGlyph(glyph)

    def drawMeasurementLink(self, pt1, pt2):
        DB.stroke(*self.colorMeasurementLink)
        DB.lineDash(4, 4)
        DB.strokeWidth(2)
        DB.line((pt1.x, pt1.y), (pt2.x, pt2.y))

    def drawGlyphPoints(self, glyph, selectedPoints):
        r = 8
        DB.stroke(None)
        DB.fontSize(self.fontSizePoints * 1 / self.glyphScale)
        DB.font('Menlo')
        i = 0
        for c in glyph:
            for p in c.points:
                if str(i) in selectedPoints:
                    DB.fill(1, 0, 0)
                else:
                    DB.fill(0.65)
                DB.oval(p.x - r, p.y - r, r * 2, r * 2)
                DB.text(str(i), (p.x - r * 2, p.y - self.fontSizePoints * 1 / self.glyphScale * 0.35), align='right')
                i += 1
        namedPoints = {
            'A'  : (0, self.font.info.ascender),
            'B'  : (0, 0),
            'C'  : (0, self.font.info.capHeight),
            'D'  : (0, self.font.info.descender),
            'X'  : (0, self.font.info.xHeight),
            '-1' : (0, 0),
            '99' : (glyph.width, 0),
        }
        for name, pos in namedPoints.items():
            if name in selectedPoints:
                DB.fill(1, 0, 0)
                x, y = pos
                DB.oval(x - r, y - r, r * 2, r * 2)
                DB.text(name, (x - r * 2, y - self.fontSizePoints * 1 / self.glyphScale * 0.35), align='right')

    def drawFrame(self):
        DB.stroke(0)
        DB.fill(None)
        DB.strokeWidth(1)
        DB.rect(self.margin, self.margin, self.boxSize, self.boxSize)

    def drawFontMeasurements(self, sectionTitle=True):

        if sectionTitle:
            self.drawSectionTitlePage('font-level measurements')

        s = self.glyphScale

        for measurement in self.fontMeasurements.keys():
            m = self.fontMeasurements[measurement]

            DB.newPage('A4Landscape')
            DB.blendMode('multiply')

            self.drawFontMeasurementInfo(measurement, m)

            glyph2    = m['glyph 2']
            point1    = m['point 1']
            point2    = m['point 2']
            direction = m['direction']

            glyph = self.font[glyph2]
            try:
                pt1 = getPointAtIndex(glyph, int(point1))
            except:
                pt1 = getAnchorPoint(self.font, point1)
            try:
                pt2 = getPointAtIndex(glyph, int(point2))
            except:
                pt2 = getAnchorPoint(self.font, point2)

            # enter clipping path
            B = DB.BezierPath()
            B.rect(self.margin, self.margin, self.boxSize, self.boxSize)
            DB.save()
            DB.clipPath(B)

            self.drawGlyphMetrics(glyph)

            DB.translate(*self.glyphOrigin(glyph))
            DB.scale(s)

            self.drawMeasurementDirection(pt1, pt2, direction)
            self.drawGlyphShape(glyph)
            self.drawMeasurementLink(pt1, pt2)
            self.drawGlyphPoints(glyph, [point1, point2])

            # exit clipping path
            DB.restore()

            self.drawFrame()

    def drawMeasurementLinks(self, glyph):

        if glyph.name not in self.glyphMeasurements:
            return

        glyphMeasurements = self.glyphMeasurements[glyph.name]
        for ID in glyphMeasurements:
            pt1_index, pt2_index = ID.split()
            
            try:
                pt1 = getPointAtIndex(glyph, int(pt1_index))
            except:
                pt1 = getAnchorPoint(glyph.font, pt1_index)

            try:
                pt2 = getPointAtIndex(glyph, int(pt2_index))
            except:
                pt2 = getAnchorPoint(glyph.font, pt2_index)

            self.drawMeasurementLink(pt1, pt2)

    def drawGlyphMeasurementsInfo(self, glyphName):

        if glyphName not in self.font:
            return

        glyph = self.font[glyphName]

        x = self.boxSize + self.margin * 2
        y = DB.height() - self.margin - self.fontSize * 0.7

        txt = DB.FormattedString()
        txt.fontSize(self.fontSize)
        txt.lineHeight(self.fontSize * self.lineHeight)
        txt.paragraphBottomSpacing(None)
        txt.append(f'{glyphName}\n')
        txt.fontSize(self.fontSizeLabels)
        txt.lineHeight(self.fontSizeLabels * self.lineHeight)
        txt.paragraphBottomSpacing(5)
        txt.append('glyph name\n')

        txt.paragraphBottomSpacing(0)
        txt.tabs((50, "left"), (100, "left"), (150, "left"))

        measurements = self.glyphMeasurements.get(glyphName, {})
        for ID in measurements.keys():
            pt1, pt2 = ID.split()
            m = measurements[ID]
            txt.append(f'{m["name"]}\t{pt1}\t{pt2}\n')

        DB.text(txt, (x, y))

    def drawTitlePage(self):
        DB.newPage('A4Landscape')
        txt = f'{self.font.info.familyName}\nmeasurements'
        x = y = m = self.margin
        DB.fontSize(self.fontSizeTitle)
        DB.textBox(txt, (x, y, DB.width() - m*2, DB.height() - m*2))

    def drawSectionTitlePage(self, sectionTitle):
        DB.newPage('A4Landscape')
        x = y = m = self.margin
        DB.fontSize(self.fontSizeSection)
        DB.textBox(sectionTitle, (x, y, DB.width() - m*2, DB.height() - m*2))

    def drawGlyphMeasurements(self, sectionTitle=True, glyphNames=[]):
        if sectionTitle:
            self.drawSectionTitlePage('glyph-level measurements')

        s = self.glyphScale

        for glyphName in glyphNames:

            if not self.glyphMeasurements.get(glyphName):
                continue

            DB.newPage('A4Landscape')
            self.drawGlyphMeasurementsInfo(glyphName)

            if glyphName not in self.font:
                continue

            glyph = self.font[glyphName]

            # enter clipping path
            B = DB.BezierPath()
            B.rect(self.margin, self.margin, self.boxSize, self.boxSize)
            DB.save()
            DB.clipPath(B)

            self.drawGlyphMetrics(glyph)

            DB.translate(*self.glyphOrigin(glyph))
            DB.scale(s)

            self.drawGlyphShape(glyph)
            self.drawMeasurementLinks(glyph)
            self.drawGlyphPoints(glyph, [])

            # exit clipping path
            DB.restore()

            self.drawFrame()

    def makePDF(self, fontMeasurements=True, glyphMeasurements=False, sectionTitle=False, title=False, glyphNames=None):
        if glyphNames is None:
            glyphNames = self.font.glyphOrder
        if title:
            self.drawTitlePage()
        if fontMeasurements:
            self.drawFontMeasurements(sectionTitle=sectionTitle)
        if glyphMeasurements:
            self.drawGlyphMeasurements(sectionTitle=sectionTitle, glyphNames=glyphNames)

    def savePDF(self, pdfPath):
        DB.saveImage(pdfPath)


