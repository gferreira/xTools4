import drawBot as DB
from fontParts.world import OpenFont
from xTools4.modules.linkPoints2 import readMeasurements, getPointAtIndex, getAnchorPoint


class MeasurementsViewer:

    margin         = 20
    fontSize       = 12
    lineHeight     = 1.5
    fontSizePoints = 9

    def __init__(self, measurementsPath, fontPath):
        self.measurements = readMeasurements(measurementsPath)
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

    def drawMeasurementoInfo(self):
        pass
    
    def drawGlyph(self):
        pass

    def drawMeasurementZone(self):
        pass

    def drawMeasurementLink(self):
        pass
    
    def drawFontMeasurements(self, sectionTitle=True):

        if sectionTitle:
            self.drawSectionTitlePage('font-level measurements')

        for measurement in self.fontMeasurements.keys():
            m = self.fontMeasurements[measurement]

            DB.newPage('A4Landscape')
            DB.blendMode('multiply')

            H = DB.height() - self.margin * 2
            W = H

            x = W + self.margin * 2
            y = DB.height() - self.margin - self.fontSize * 0.7

            DB.fontSize(self.fontSize)
            DB.lineHeight(self.fontSize * self.lineHeight)
            DB.text(measurement, (x, y))
            y -= self.fontSize * self.lineHeight
            description = m['description']
            DB.text(description, (x, y))    
            y -= self.fontSize * self.lineHeight

            direction = m['direction']
            glyph1    = m['glyph 1']
            glyph2    = m['glyph 2']
            point1    = m['point 1']
            point2    = m['point 2']
            DB.text(f'{direction}\n{glyph1} {point1}\n{glyph2} {point2}', (x, y))    

            glyph = self.font[glyph2]

            try:
                pt1 = getPointAtIndex(glyph, int(point1))
            except:
                pt1 = getAnchorPoint(self.font, point1)

            try:
                pt2 = getPointAtIndex(glyph, int(point2))
            except:
                pt2 = getAnchorPoint(self.font, point2)

            if direction == 'x':
                P1 = pt1.x, pt1.y
                P2 = pt2.x, pt1.y
            elif direction == 'y':
                P1 = pt2.x, pt1.y
                P2 = pt2.x, pt2.y
            else: # angled
                P1 = pt1.x, pt1.y
                P2 = pt2.x, pt2.y

            s = 0.185
            x = (W - (glyph.width*s)) / 2
            y = H * 0.27

            B = DB.BezierPath()
            B.rect(self.margin, self.margin, W, W)

            DB.save()
            DB.clipPath(B)

            vmetrics = set([
                0,
                self.font.info.xHeight,
                self.font.info.descender,
                self.font.info.ascender,
                self.font.info.capHeight,
            ])
            DB.translate(self.margin, self.margin)
            DB.stroke(0.85)
            DB.strokeWidth(1)
            for vy in vmetrics:
                DB.line((0, y + vy * s), (W, y + vy * s))
            for vx in [0, glyph.width * s]:
                DB.line((x + vx, 0), (x + vx, H))

            DB.translate(x, y)
            DB.scale(s)

            # draw direction
            DB.lineDash(None)
            DB.strokeWidth(100000)
            DB.stroke(1, 0, 0, 0.1)
            DB.line(P1, P2)

            # draw glyph
            DB.strokeWidth(1 * 1/s)
            DB.stroke(0.85)
            DB.fill(0.9)
            DB.drawGlyph(glyph)

            # draw measurement
            DB.stroke(1, 0, 0)
            DB.lineDash(4, 4)
            DB.strokeWidth(2)
            DB.line((pt1.x, pt1.y), (pt2.x, pt2.y))

            # draw points
            r = 8
            DB.stroke(None)
            DB.fontSize(self.fontSizePoints * 1/s)
            DB.font('Menlo')
            i = 0
            for c in glyph:
                for p in c.points:
                    if str(i) in [point1, point2]:
                        DB.fill(1, 0, 0)
                    else:
                        DB.fill(0.65)
                    DB.oval(p.x - r, p.y - r, r * 2, r * 2)            
                    DB.text(str(i), (p.x - r * 2, p.y - self.fontSizePoints * 1/s * 0.35), align='right')
                    i += 1

            DB.restore()

            # draw frame around glyph view
            DB.stroke(0)
            DB.fill(None)
            DB.strokeWidth(1)
            DB.rect(self.margin, self.margin, W, W)


    def drawTitlePage(self):
        print(f'making title page: {self.title}...')

    def drawSectionTitlePage(self, sectionTitle):
        print(f'making section title page: {sectionTitle}...')

    def drawGlyphMeasurements(self, sectionTitle=True):
        if sectionTitle:
            self.drawSectionTitlePage('glyph-level measurements')

    def makePDF(self, fontMeasurements=True, glyphMeasurements=True, sectionTitle=True, title=True):
        print('making PDF...')
        if title:
            self.drawTitlePage()
        if fontMeasurements:
            self.drawFontMeasurements(sectionTitle=sectionTitle)
        if glyphMeasurements:
            self.drawGlyphMeasurements(sectionTitle=sectionTitle)

    def savePDF(self, pdfPath):
        print('saving PDF...')

