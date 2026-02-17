import os
import drawBot as DB
from fontParts.world import OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.xproject import measurementsPathKey

class GlyphMemeProofer:
    
    glyphScale = 0.3
    canvasWidth = canvasHeight = 850

    panelWidth = canvasWidth / 4

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

    deltasDraw = True

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

                txt = ''
                for k, v in self.glyphMeasurements.items():
                    pt1, pt2 = k.split()
                    txt += f"{v['name']}\t{pt1}\t{pt2}\n"

                print(txt)

                with DB.savedState():
                    # DB.fill(1, 0, 0, 0.1)
                    # DB.rect(*panelBox)
                    DB.font(self.captionFont)
                    DB.fontSize(self.captionSize)
                    DB.fill(*self.captionColor)
                    DB.textBox(txt, panelBox, align='left')




