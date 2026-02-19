import os
import drawBot as DB
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import glyphNameToFileName
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.xproject import measurementsPathKey
from xTools4.modules.measurements import Measurement
from xTools4.modules.validation import *
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


colorCheckTrueBG  = 0.7, 1.0, 0.7, 0.85
colorCheckFalseBG = 1.0, 0.7, 0.7, 0.85


class GlyphMemeProofer:
    
    glyphScale = 0.3
    canvasWidth = canvasHeight = 850

    panelWidth = canvasWidth * 0.3

    glyphInfoDraw = True

    captionSize = 13
    captionColor = 0.6,
    captionFont = 'Menlo'

    metricsDraw = True
    metricsColor = 0.85,
    
    anchorsDraw = True
    anchorsRadius = 7
    anchorsColor = 1, 0, 0
    
    contoursDraw = True
    contoursFill = 0.95,
    contoursStroke = 0.8,
    contoursStrokeWidth = 5

    pointsDraw = True
    pointsRadius = 7
    pointsFill = 0.35,
    pointsStroke = None

    pointLabelsDraw = True
    pointLabelsSize = 7
    pointLabelsColor = 0,

    measurementsDraw = True
    measurementsThreshold = 0.1
    
    deltasDraw = True
    validationDraw = True

    verbose = False
    
    def __init__(self, glyphName, designspacePath):
        self.glyphName = glyphName
        # get designspace
        self.designspace = DesignSpaceDocument()
        self.designspace.read(designspacePath)

    @property
    def measurementsPath(self):
        fileName = self.designspace.lib.get(measurementsPathKey)
        if fileName:
            sourcesFolder = os.path.dirname(self.designspace.path)
            return os.path.join(sourcesFolder, fileName)

    @property
    def glyphMeasurements(self):
        measurementsDict = readMeasurements(self.measurementsPath)
        return measurementsDict['glyphs'].get(self.glyphName)
        
    @property
    def parameters(self):        
        return sorted(list(set([m['name'] for m in self.glyphMeasurements.values()])))

    @property    
    def parametricSources(self):
        sources = {}
        for parameter in self.parameters:
            parameterHasSources = False
            for src in self.designspace.sources:
                if parameter in src.styleName:
                    srcName = os.path.splitext(src.filename)[0].split('_')[-1]
                    sources[srcName] = src.path
                    parameterHasSources = True
            if not parameterHasSources:
                if self.verbose:
                    print(f'no sources for {parameter}')
        return sources

    @property    
    def parametricGlyphs(self):
        glyphs = {}
        for srcName, srcPath in self.parametricSources.items():
            f = OpenFont(srcPath, showInterface=False)
            glyphs[srcName] = f[self.glyphName]
        return glyphs

    def draw(self):
        DB.newDrawing()
        for srcName, glyph in self.parametricGlyphs.items():
            self.drawGlyph(glyph, srcName)

    def drawGlyph(self, glyph, srcName):

        # get vertical metrics
        metricsY = {
            0,
            glyph.font.info.descender,
            glyph.font.info.xHeight,
            glyph.font.info.capHeight,
            glyph.font.info.ascender,
        }

        # get bounding box
        boxHeight = (max(metricsY) - min(metricsY)) * self.glyphScale
        boxY = (self.canvasHeight - boxHeight) * 0.5
        boxWidth = glyph.width * self.glyphScale

        defaultFont = OpenFont(self.designspace.default.path, showInterface=False)

        DB.newPage(self.canvasWidth + self.panelWidth, self.canvasHeight)
        DB.blendMode('multiply')

        # calculate origin point
        x = (self.canvasWidth - boxWidth) * 0.5
        y = boxY + abs(glyph.font.info.descender) * self.glyphScale

        # get horizontal metrics
        metricsX = {x, x + boxWidth}

        if self.metricsDraw:
            self._drawMetrics((x, y), metricsX, metricsY)

        if self.contoursDraw:
            self._drawContours(glyph, (x, y))

        if self.anchorsDraw:
            self._drawAnchors(glyph, (x, y))

        if self.glyphInfoDraw:
            self._drawInfo(glyph, (x, y), srcName)

        if self.measurementsDraw:
            self._drawMeasurements(glyph, defaultFont)

        if self.deltasDraw:
            self._drawDeltas(glyph, (x, y), defaultFont)

        if self.validationDraw:
            self._drawValidation(glyph, defaultFont)

    def save(self, folder, fileName):

        glifName = os.path.splitext(glyphNameToFileName(self.glyphName, None))[0]
        pdfFileName = f'{fileName}_{glifName}.pdf'

        pdfPath = os.path.join(folder, pdfFileName)
        if os.path.exists(pdfPath):
            os.remove(pdfPath)

        print(f'saving {pdfFileName}...', end=' ')

        DB.saveImage(pdfPath)

        print(os.path.exists(pdfPath))

    def _drawMetrics(self, pos, metricsX, metricsY):
        x, y = pos
        DB.save()
        DB.stroke(*self.metricsColor)
        for mx in metricsX:
            DB.line((mx, 0), (mx, DB.height()))
        for my in metricsY:
            my = y + my * self.glyphScale
            DB.line((0, my), (self.canvasWidth, my))
        DB.restore()

    def _drawContours(self, glyph, pos):
        x, y = pos

        DB.save()
        DB.strokeWidth(self.contoursStrokeWidth)
        DB.lineJoin('round')

        if self.contoursStroke is None:
            DB.stroke(self.contoursStroke)
        else:
            DB.stroke(*self.contoursStroke)
        if self.contoursFill is None:
            DB.fill(self.contoursFill)
        else: 
            DB.fill(*self.contoursFill)

        DB.translate(x, y)
        DB.scale(self.glyphScale)
        DB.drawGlyph(glyph)

        if self.pointsDraw:
            pointCaptionSize = self.pointLabelsSize / self.glyphScale

            DB.font(self.captionFont)
            DB.fontSize(pointCaptionSize)

            r = self.pointsRadius
            n = 0
            for c in glyph.contours:
                for pt in c.points:

                    if self.pointsStroke is None:
                        DB.stroke(self.pointsStroke)
                    else:
                        DB.stroke(*self.pointsStroke)
                    if self.pointsFill is None:
                        DB.fill(self.pointsFill)
                    else: 
                        DB.fill(*self.pointsFill)
                    DB.oval(pt.x - r, pt.y - r, r*2, r*2)

                    if self.pointLabelsDraw:
                        DB.fill(*self.pointLabelsColor)
                        DB.text(f'{n}', (pt.x, pt.y - r - pointCaptionSize), align='center')

                    n += 1

        DB.restore()

    def _drawAnchors(self, glyph, pos):
        x, y = pos
        r = self.pointsRadius
        pointCaptionSize = self.pointLabelsSize / self.glyphScale

        DB.save()
        DB.font(self.captionFont)
        DB.fontSize(pointCaptionSize)

        if self.pointsStroke is None:
            DB.stroke(self.pointsStroke)
        else:
            DB.stroke(*self.pointsStroke)
        if self.pointsFill is None:
            DB.fill(self.pointsFill)
        else: 
            DB.fill(*self.pointsFill)

        DB.translate(x, y)
        DB.scale(self.glyphScale)
        for anchor in glyph.anchors:
            aX, aY = anchor.position
            DB.oval(aX - r, aY - r, r*2, r*2)
            DB.fill(*self.pointLabelsColor)
            if self.pointLabelsDraw:
                DB.text(anchor.name, (aX, aY - r - pointCaptionSize), align='center')

        DB.restore()

    def _drawInfo(self, glyph, pos, srcName):
        x, y = pos
        captionX = self.captionSize
        captionW = self.canvasWidth - self.captionSize * 2
        captionH = self.captionSize * 2

        DB.save()
        DB.font(self.captionFont)
        DB.fontSize(self.captionSize)
        DB.fill(*self.captionColor)

        captionY = DB.height() - self.captionSize * 3
        captionBox = captionX, captionY, captionW, captionH
        DB.textBox(glyph.name, captionBox, align='left')
        DB.textBox(srcName, captionBox, align='center')
        if glyph.unicode:
            uni = str(hex(glyph.unicode)).replace("0x", '')
            uni = uni.zfill(4).upper()
            DB.textBox(uni, captionBox, align='right')

        captionY = 0
        captionBox = captionX, captionY, captionW, captionH
        DB.textBox(f'{glyph.width}', captionBox, align='center')
        if glyph.bounds:
            DB.textBox(f'{glyph.leftMargin}', captionBox, align='left')
            DB.textBox(f'{glyph.rightMargin}', captionBox, align='right')

        DB.restore()

    def _drawMeasurements(self, glyph, defaultFont):

        panelX = self.canvasWidth + self.captionSize
        panelY = self.captionSize
        panelW = self.panelWidth - self.captionSize * 2
        panelH = self.canvasHeight - self.captionSize * 2
        panelBox = panelX, panelY, panelW, panelH

        defaultGlyph = defaultFont[glyph.name]

        char = 7

        DB.save()

        T = DB.FormattedString()
        T.tabs((char*7, "left"), (char*12, "left"), (char*17, "left"), (char*24, "left"))
        T.font(self.captionFont)
        T.fontSize(self.captionSize)
        T.stroke(None)
        T.fill(*self.captionColor)
        T.append('name\tp1\tp2\tunits\tscale\n')
        T.append(f'{"-"*27}\n')

        for k, v in self.glyphMeasurements.items():
            pt1, pt2 = k.split()

            M = Measurement(
                v['name'],
                v['direction'],
                glyph.name, pt1,
                glyph.name, pt2,
            )
            value = M.measure(glyph.font, italicCorrection=True)
            valueDefault = M.measure(defaultFont, italicCorrection=True)
            scaleDefault = value / valueDefault

            if scaleDefault is None:
                color = colorCheckNone
            elif scaleDefault == 1:
                color = colorCheckEqual
            elif (1.0 - self.measurementsThreshold) < scaleDefault < (1.0 + self.measurementsThreshold):
                color = colorCheckTrue
            else:
                color = colorCheckFalse

            T.fill(*self.captionColor)
            T.append(f"{v['name']}\t{pt1}\t{pt2}\t{value}\t")

            T.fill(*color)
            T.append(f"{scaleDefault:.2f}\n")

        DB.textBox(T, panelBox, align='left')

        DB.save()

    def _drawDeltas(self, glyph, pos, defaultFont):

        x, y = pos

        defaultGlyph = defaultFont[glyph.name]

        DB.save()
        DB.strokeWidth(self.contoursStrokeWidth)

        if self.contoursStroke is None:
            DB.stroke(self.contoursStroke)
        else:
            DB.stroke(*self.contoursStroke)

        DB.fill(None)
        DB.lineDash(self.contoursStrokeWidth, self.contoursStrokeWidth)
        DB.lineJoin('round')
        DB.translate(x, y)

        with DB.savedState():
            DB.scale(self.glyphScale)
            DB.drawGlyph(defaultGlyph)

        dash = 2, 2
        r = self.pointsRadius * self.glyphScale
        r2 = 4
        s =  self.glyphScale

        DB.lineDash(None)
        for ci, c in enumerate(glyph):
            for pi, p in enumerate(c.points):
                p2 = defaultGlyph.contours[ci].points[pi]
                isEqual = p2.x == p.x and p2.y == p.y
                isOrthogonal = p2.x == p.x or p2.y == p.y

                color   = colorCheckTrue   if isOrthogonal else colorCheckFalse
                colorBG = colorCheckTrueBG if isOrthogonal else colorCheckFalseBG

                if isEqual:
                    DB.stroke(*colorCheckEqual)
                    DB.strokeWidth(1)
                    DB.fill(None)
                    DB.oval(p2.x * s - r2, p2.y * s - r2, r2*2, r2*2)

                else:
                    DB.stroke(*color)
                    DB.strokeWidth(1)
                    DB.line((p.x * s, p.y * s), (p2.x * s, p2.y * s))

                    DB.stroke(None)
                    DB.fill(*self.contoursStroke)
                    DB.oval(p2.x * s - r, p2.y * s - r, r*2, r*2)

        if self.anchorsDraw:
            for ai, a in enumerate(glyph.anchors):
                a2 = defaultGlyph.anchors[ai]
                isEqual = a2.x == a.x and a2.y == a.y
                isOrthogonal = a2.x == a.x or a2.y == a.y

                color   = colorCheckTrue   if isOrthogonal else colorCheckFalse
                colorBG = colorCheckTrueBG if isOrthogonal else colorCheckFalseBG

                if isEqual:
                    DB.stroke(*colorCheckEqual)
                    DB.strokeWidth(1)
                    DB.fill(None)
                    DB.oval(a2.x * s - r2, a2.y * s - r2, r2*2, r2*2)

                else:
                    DB.stroke(*color)
                    DB.strokeWidth(1)
                    DB.line((a.x * s, a.y * s), (a2.x * s, a2.y * s))

                    DB.stroke(None)
                    DB.fill(*self.contoursStroke)
                    DB.oval(a2.x * s - r, a2.y * s - r, r*2, r*2)



        DB.restore()

    def _drawValidation(self, glyph, defaultFont):

        defaultGlyph = defaultFont[glyph.name]

        checkResults = {
            'compatibility' : checkCompatibility(glyph, defaultGlyph),
            'equality'      : checkEquality(glyph, defaultGlyph),
        }

        T = DB.FormattedString()
        T.fontSize(self.captionSize)
        T.stroke(None)
        T.fill(*self.captionColor)

        for checkName, isEqual in checkResults['equality'].items():
            isCompatible = checkResults['compatibility'].get(checkName)
            if isCompatible and isEqual:
                color = colorCheckEqual
            elif isCompatible or isEqual:
                color = colorCheckTrue
            else:
                color = colorCheckFalse

            T.fill(*color)
            T.append(f'{checkName[0].upper()} ')

        vX = self.canvasWidth + self.captionSize
        vY = self.captionSize

        DB.text(T, (vX, vY))




if __name__ == '__main__':

    P = GlyphMemeProofer(glyphName, designspacePath)
    a.glyphScale = 0.25
    P.contoursDraw = True
    P.metricsDraw = True
    P.pointsDraw = True
    P.anchorsDraw = True
    P.pointLabelsDraw = True
    P.glyphInfoDraw = True
    P.measurementsDraw = True
    P.validationDraw = True
    P.deltasDraw = True
    P.draw()

    pdfFileName = os.path.splitext(os.path.split(designspacePath)[-1])[0]

    if savePDF:
        P.save(proofsFolder, pdfFileName)

