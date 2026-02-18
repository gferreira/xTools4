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

    captionDraw = True
    captionSize = 13
    captionColor = 0.6,
    captionFont = 'Menlo'

    metricsDraw = True
    metricsColor = 0.85,
    
    anchorsDraw = False
    anchorsRadius = 7
    anchorsColor = 1, 0, 0
    
    glyphColorFill = 0.95,
    glyphColorStroke = 0.8,
    glyphWidthStroke = 5

    pointsDraw = True
    pointsRadius = 7
    pointsColorFill = 0.35,
    pointsColorStroke = None

    pointsIndexDraw = True
    pointsIndexSize = 7
    pointsIndexColor = 0,

    measurementsDraw = True

    defaultDraw = True
    defaultThreshold = 0.1

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
        defaultGlyph = defaultFont[glyph.name]

        DB.newPage(self.canvasWidth + self.panelWidth, self.canvasHeight)
        DB.blendMode('multiply')

        # calculate origin point
        x = (self.canvasWidth - boxWidth) * 0.5
        y = boxY + abs(glyph.font.info.descender) * self.glyphScale

        # get horizontal metrics
        metricsX = {x, x + boxWidth}

        if self.metricsDraw:
            with DB.savedState():
                DB.stroke(*self.metricsColor)
                for metricX in metricsX:
                    DB.line((metricX, 0), (metricX, DB.height()))
                for metricY in metricsY:
                    metricY = y + metricY * self.glyphScale
                    DB.line((0, metricY), (self.canvasWidth, metricY))

        # draw glyph
        with DB.savedState(): 
            DB.strokeWidth(self.glyphWidthStroke)
            if self.glyphColorStroke is None:
                DB.stroke(self.glyphColorStroke)
            else:
                DB.stroke(*self.glyphColorStroke)
            if self.glyphColorFill is None:
                DB.fill(self.glyphColorFill)
            else: 
                DB.fill(*self.glyphColorFill)
            DB.lineJoin('round')
            DB.translate(x, y)
            DB.scale(self.glyphScale)
            DB.drawGlyph(glyph)

            if self.pointsDraw:
                pointCaptionSize = self.pointsIndexSize / self.glyphScale

                DB.font(self.captionFont)
                DB.fontSize(pointCaptionSize)

                r = self.pointsRadius
                n = 0
                for c in glyph.contours:
                    for pt in c.points:

                        if self.pointsColorStroke is None:
                            DB.stroke(self.pointsColorStroke)
                        else:
                            DB.stroke(*self.pointsColorStroke)
                        if self.pointsColorFill is None:
                            DB.fill(self.pointsColorFill)
                        else: 
                            DB.fill(*self.pointsColorFill)
                        DB.oval(pt.x - r, pt.y - r, r*2, r*2)

                        if self.pointsIndexDraw:
                            DB.fill(*self.pointsIndexColor)
                            DB.text(f'{n}', (pt.x, pt.y - r - pointCaptionSize), align='center')

                        n += 1

        if self.anchorsDraw:
            r = self.anchorsRadius
            with DB.savedState():
                DB.fill(None)
                DB.stroke(*self.anchorsColor)
                DB.translate(x, y)
                for anchor in g.anchors:
                    aX, aY = anchor.position
                    aX *= self.glyphScale
                    aY *= self.glyphScale
                    DB.oval(aX - r, aY - r, r*2, r*2)
                    DB.line((aX - r, aY), (aX + r, aY))
                    DB.line((aX, aY - r), (aX, aY + r))

        if self.captionDraw:
            captionX = self.captionSize
            captionW = self.canvasWidth - self.captionSize * 2
            captionH = self.captionSize * 2

            with DB.savedState():
                DB.font(self.captionFont)
                DB.fontSize(self.captionSize)
                DB.fill(*self.captionColor)

                # top
                captionY = DB.height() - self.captionSize * 3
                captionBox = captionX, captionY, captionW, captionH
                DB.textBox(glyph.name, captionBox, align='left')
                DB.textBox(srcName, captionBox, align='center')
                if glyph.unicode:
                    uni = str(hex(glyph.unicode)).replace("0x", '')
                    uni = uni.zfill(4).upper()
                    DB.textBox(uni, captionBox, align='right')

                # bottom
                captionY = 0
                captionBox = captionX, captionY, captionW, captionH
                DB.textBox(f'{glyph.width}', captionBox, align='center')
                if glyph.bounds:
                    DB.textBox(f'{glyph.leftMargin}', captionBox, align='left')
                    DB.textBox(f'{glyph.rightMargin}', captionBox, align='right')

        if self.measurementsDraw:

            panelX = self.canvasWidth + self.captionSize
            panelY = self.captionSize
            panelW = self.panelWidth - self.captionSize * 2
            panelH = self.canvasHeight - self.captionSize * 2
            panelBox = panelX, panelY, panelW, panelH

            char = 7

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
                elif (1.0 - self.defaultThreshold) < scaleDefault < (1.0 + self.defaultThreshold):
                    color = colorCheckTrue
                else:
                    color = colorCheckFalse

                T.fill(*self.captionColor)
                T.append(f"{v['name']}\t{pt1}\t{pt2}\t{value}\t")

                T.fill(*color)
                T.append(f"{scaleDefault:.2f}\n")

            DB.textBox(T, panelBox, align='left')

        if self.deltasDraw:
            if self.defaultDraw:
                with DB.savedState():
                    DB.strokeWidth(self.glyphWidthStroke)
                    if self.glyphColorStroke is None:
                        DB.stroke(self.glyphColorStroke)
                    else:
                        DB.stroke(*self.glyphColorStroke)
                    DB.fill(None)
                    DB.lineDash(self.glyphWidthStroke, self.glyphWidthStroke)
                    DB.lineJoin('round')
                    DB.translate(x, y)

                    with DB.savedState():
                        DB.scale(self.glyphScale)
                        DB.drawGlyph(defaultGlyph)

                    dash = 2, 2
                    r = self.pointsRadius * self.glyphScale
                    r2 = 6
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
                                DB.strokeWidth(2)
                                DB.fill(None)
                                DB.oval(p2.x * s - r2, p2.y * s - r2, r2*2, r2*2)

                            else:
                                DB.stroke(*color)
                                DB.strokeWidth(1)
                                DB.line((p.x * s, p.y * s), (p2.x * s, p2.y * s))

                                DB.stroke(None)
                                DB.fill(*self.pointsColorFill)
                                DB.oval(p2.x * s - r, p2.y * s - r, r*2, r*2)

        if self.validationDraw:

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

    def save(self, folder, fileName):

        glifName = os.path.splitext(glyphNameToFileName(self.glyphName, None))[0]
        pdfFileName = f'{fileName}_{glifName}.pdf'

        pdfPath = os.path.join(folder, pdfFileName)
        if os.path.exists(pdfPath):
            os.remove(pdfPath)

        print(f'saving {pdfFileName}...', end=' ')

        DB.saveImage(pdfPath)

        print(os.path.exists(pdfPath))


