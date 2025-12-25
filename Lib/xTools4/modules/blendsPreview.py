import os
from random import random
from datetime import datetime
from functools import cached_property
import drawBot as DB
import uharfbuzz as hb
from defcon.objects.glyph import Glyph
from defcon.objects.font import Font
from fontTools.ttLib import TTFont
from fontTools.varLib.avar.build import build as avar2_build
from fontTools.varLib.avar.map import map as avar2_map
from mutatorMath.objects.location import Location
from ufoProcessor.ufoOperator import UFOOperator
from glyphNameFormatter.reader import n2u

def getEffectiveLocation(designspacePath, blendedLocation):
    font = TTFont()
    avar2_build(font, designspacePath)
    return avar2_map(font, blendedLocation)

def instantiateGlyph(operator, glyphName, location):
    glyphMutator, uni = operator.getGlyphMutator(glyphName)
    if not glyphMutator:
        return
    instance = glyphMutator.makeInstance(Location(**location))
    g = instance.extractGlyph(Glyph())
    return g

def drawGlyph(g):
    B = DB.BezierPath()
    g.draw(B)
    DB.drawPath(B)

def drawGlyphTTF(ttfPath, glyphName):
    char = chr(n2u(glyphName))
    upm = TTFont(ttfPath)['head'].unitsPerEm
    B = BezierPath()
    B.text(char, font=ttfPath, fontSize=upm)
    DB.drawPath(B)

def getGlyphTTF_old(ttfPath, glyphName, location):
    glyphSet = TTFont(ttfPath).getGlyphSet()
    ttGlyph = glyphSet[glyphName]
    glyph = RGlyph()
    pen = glyph.getPen()
    ttGlyph.draw(pen)
    glyph.width = ttGlyph.width
    return glyph

def getVarDistance(location, defaultLocation):
    n = 1
    for key, value in location.items():
        defaultValue = defaultLocation.get(key)
        if value != defaultValue:
            n += 1
    return n

def getTTFGlyphForChar(ttfPath, char, location):
    hb_text = char
    hb_blob = hb.Blob.from_file_path(ttfPath)
    hb_face = hb.Face(hb_blob)
    hb_font = hb.Font(hb_face)

    hb_font.set_variations(location)

    buf = hb.Buffer()
    buf.add_str(hb_text)
    buf.guess_segment_properties()

    features = {"kern": True, "liga": True}
    hb.shape(hb_font, buf, features)

    info = buf.glyph_infos[0]
    positions = buf.glyph_positions[0]

    gid = info.codepoint
    x_advance = positions.x_advance

    glyph = Glyph()
    pen = glyph.getPen()

    hb_font.draw_glyph_with_pen(gid, pen)

    glyph.width = x_advance

    return glyph

def getGlyphTTF(ttfPath, glyphName, location):
    char = chr(n2u(glyphName))
    if not char:
        return

    return getTTFGlyphForChar(ttfPath, char, location)


class BlendsPreview:

    margin      = 20, 10
    glyphScale  = 0.045
    labelsSize  = 4

    compare     = False
    points      = False
    margins     = False
    labels      = False
    levels      = False
    header      = True
    footer      = True
    levelsShow  = [1, 2, 3, 4]
    pointRadius = 8

    debug = False

    headerHeight = 20
    footerHeight = 20

    axesList = []

    compareColors = [
        (1, 0, 1), # reference font
        (0, 1, 1), # blended font
    ]

    levelsColors = [
        (0.0, 0.5, 1.0), # monovar
        (1.0, 0.0, 0.5), # duovars
        (0.0, 1.0, 0.5), # trivars
        (1.0, 0.5, 0.0), # quadvars
    ]

    compareFontPath = None
    compareFont     = None

    def __init__(self, designspacePath):
        # initiate operator + sources
        self.designspacePath = designspacePath
        self.operator = UFOOperator()
        self.operator.read(self.designspacePath)
        self.operator.loadFonts()
        # initiate drawing
        DB.newDrawing()

    @cached_property
    def compareFont(self):
        return TTFont(self.compareFontPath)

    @cached_property
    def defaultFont(self):
        return Font(self.operator.doc.default.path)

    @property
    def cellSize(self):
        return self.defaultFont.info.unitsPerEm

    @property
    def parametricAxes(self):
        return self.operator.doc.default.location.keys()

    @property
    def blendedAxes(self):
        allAxes = [axis.name for axis in self.operator.doc.axes]
        return list(set(allAxes).difference(set(self.parametricAxes)))

    def getColors(self, level=1):
        colors = {
            'fillHeader2'    : (0,),
            'fill2'          : (0,),
            'stroke2'        : None,
            'points2'        : None,
            'strokeMargins2' : (0,),
        }
        if self.points:
            colors['fill2']   = None
            colors['stroke2'] = 0,
            colors['points2'] = 0,

        levelColor = self.levelsColors[level-1]

        if self.compare and not self.levels:
            colors['fillHeader2']    = self.compareColors[1]
            colors['fill2']          = self.compareColors[1]
            colors['strokeMargins2'] = self.compareColors[1]

            colors['fillHeader1']    = self.compareColors[0]
            colors['fill1']          = self.compareColors[0]
            colors['strokeMargins1'] = self.compareColors[0]
            colors['stroke1']        = None
            colors['points1']        = None

            if self.points:
                colors['fill2']   = None
                colors['stroke2'] = self.compareColors[1]
                colors['points2'] = self.compareColors[1]

                colors['fill1']   = None
                colors['stroke1'] = self.compareColors[0]
                colors['points1'] = self.compareColors[0]

        elif not self.compare and self.levels:
            colors['fill2']          = levelColor
            colors['strokeMargins2'] = levelColor

            if self.points:
                colors['fill2']   = None
                colors['stroke2'] = levelColor
                colors['points2'] = levelColor

        elif self.compare and self.levels:
            colors['fill2']          = levelColor
            colors['strokeMargins2'] = levelColor

            colors['fillHeader1']    = 0.8,
            colors['fill1']          = 0.9,
            colors['stroke1']        = None # 0.8,
            colors['points1']        = None
            colors['strokeMargins1'] = 0.8,

            if self.points:
                colors['fill1']   = None
                colors['stroke1'] = 0.7,
                colors['points1'] = 0.7,

                colors['fill2']   = None
                colors['stroke2'] = levelColor
                colors['points2'] = levelColor

        return colors

    def draw(self, glyphName):

        cellWidth  = self.cellSize * self.glyphScale * 1.5
        cellHeight = self.cellSize * self.glyphScale

        axis1Tag, axis1Values = self.axesList[0]
        axis2Tag, axis2Values = self.axesList[1]
        axis3Tag, axis3Values = self.axesList[2]

        w = cellWidth  * len(axis3Values) + self.margin[0] * 2
        h = cellHeight * len(axis2Values) * len(axis1Values) + self.margin[1] * 2

        x, y = self.margin

        if self.header:
            h += self.headerHeight

        if self.footer:
            h += self.footerHeight
            y += self.footerHeight

        DB.newPage(w, h)
        DB.blendMode('multiply')

        # no glyph = empty page
        if glyphName is None:
            return

        # get color scheme for current settings
        colors = self.getColors()

        defaultBlendedLocation = { a.tag : a.default for a in self.operator.doc.axes if a.name in self.blendedAxes }

        #------------------
        # draw page header
        #------------------

        m = self.margin[0]

        if self.header:
            with DB.savedState():
                DB.translate(0, DB.height() - self.headerHeight )
                if self.debug:
                    with DB.savedState():
                        DB.fill(0, 0.1)
                        DB.rect(0, 0, w, self.headerHeight)

                DB.fill(*colors['fillHeader2'])
                DB.text(self.defaultFont.info.familyName, (m, self.headerHeight/3))
                if self.compare and self.compareFont:
                    DB.save()
                    DB.translate(DB.textSize(f'{self.defaultFont.info.familyName} ')[0] + m, 0)
                    DB.fill(*colors['fillHeader1'])
                    DB.text(self.compareFont['name'].getDebugName(1), (0, self.headerHeight * 0.3))
                    DB.restore()

                DB.fill(0,)
                DB.text(glyphName, (DB.width()-m, self.headerHeight/3), align='right')

        if self.footer:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with DB.savedState():
                if self.debug:
                    DB.fill(0, 0.1)
                    DB.rect(0, 0, w, self.footerHeight)
                DB.fill(0,)
                DB.text(now, (DB.width()/2, self.footerHeight/3), align='center')

        #-------------
        # draw glyphs
        #-------------

        r = self.pointRadius

        DB.translate(x, y)

        # get UPM of the reference font (if available)
        if self.compare and self.compareFont:
            unitsPerEm2 = self.compareFont['head'].unitsPerEm

        for i, axisValue1 in enumerate(sorted(axis1Values)):
            for j, axisValue2 in enumerate(reversed(sorted(axis2Values))):
                for k, axisValue3 in enumerate(sorted(axis3Values)):
                    blendedLocation = {
                        axis1Tag: axisValue1,
                        axis2Tag: axisValue2,
                        axis3Tag: axisValue3,
                    }
                    styleName = f'{axis1Tag} {axisValue1}\n{axis2Tag} {axisValue2}\n{axis3Tag} {axisValue3}'

                    parametricLocation = getEffectiveLocation(self.designspacePath, blendedLocation)
                    g2 = instantiateGlyph(self.operator, glyphName, parametricLocation)

                    # if not g2:
                    #     continue

                    # get var distance
                    n = getVarDistance(blendedLocation, defaultBlendedLocation)

                    if n not in self.levelsShow:
                        continue

                    colors  = self.getColors(n)
                    yBottom = self.defaultFont.info.descender
                    yTop    = self.defaultFont.info.unitsPerEm - abs(yBottom)

                    DB.save()
                    DB.translate(k * cellWidth, j * cellHeight)

                    if self.debug:
                        with DB.savedState():
                            DB.fill(random(), random(), random(), 0.2)
                            DB.rect(0, 0, cellWidth, cellHeight)

                    #------------
                    # draw label
                    #------------

                    if self.labels:
                        with DB.savedState():
                            DB.fill(0)
                            DB.font('Menlo')
                            DB.fontSize(self.labelsSize)
                            DB.lineHeight(self.labelsSize * 1.25)
                            DB.text(styleName, (4, 4 + self.labelsSize*2.5))

                    DB.scale(self.glyphScale)

                    #--------------------
                    # draw blended glyph
                    #--------------------

                    if self.points:
                        DB.strokeWidth(2)

                    fill2   = colors['fill2']
                    stroke2 = colors['stroke2']
                    points2 = colors['points2']

                    if fill2 is not None:
                        DB.fill(*fill2)
                    else:
                        DB.fill(fill2)

                    if stroke2 is not None:
                        DB.stroke(*stroke2)
                    else:
                        DB.stroke(stroke2)

                    if DB.savedState():
                        DB.translate(0, -yBottom)
                        drawGlyph(g2)

                    if self.points and points2 is not None:
                        DB.fill(*points2)
                        DB.stroke(None)
                        for c in g2:
                            for p in c:
                                DB.oval(p.x-r, p.y-r, r*2, r*2)

                    if self.margins:
                        DB.strokeWidth(1)
                        DB.stroke(*colors['strokeMargins2'])
                        DB.line((0, yBottom), (0, yTop))
                        DB.line((g2.width, yBottom), (g2.width, yTop))

                    #----------------------
                    # draw reference glyph
                    #----------------------

                    if self.compare and self.compareFont:
                        if not self.defaultFont[glyphName].unicodes:
                            return
                        char = chr(self.defaultFont[glyphName].unicodes[0])
                        g1 = getTTFGlyphForChar(self.compareFontPath, char, blendedLocation)
                        if g1 is None:
                            return

                        if self.points:
                            DB.strokeWidth(2)

                        fill1   = colors['fill1']
                        stroke1 = colors['stroke1']
                        points1 = colors['points1']

                        if fill1 is not None:
                            DB.fill(*fill1)
                        else:
                            DB.fill(fill1)

                        if stroke1 is not None:
                            DB.stroke(*stroke1)
                        else:
                            DB.stroke(stroke1)

                        if DB.savedState():
                            # DB.translate(0, -yBottom)
                            drawGlyph(g1)

                        if self.points and points1 is not None:
                            DB.fill(*points1)
                            DB.stroke(None)
                            for c in g1:
                                for p in c:
                                    DB.oval(p.x-r, p.y-r, r*2, r*2)

                        if self.margins:
                            DB.strokeWidth(1)
                            DB.stroke(*colors['strokeMargins1'])
                            DB.line((0, yBottom), (0, yTop))
                            DB.line((g1.width, yBottom), (g1.width, yTop))

                    DB.restore()

            DB.translate(0, cellHeight * len(axis2Values))

    def save(self, pdfPath):
        DB.saveImage(pdfPath)

