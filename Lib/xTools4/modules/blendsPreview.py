import os, time
from functools import cached_property
import drawBot as DB
import uharfbuzz as hb
from defcon.objects.glyph import Glyph
from defcon.objects.font import Font
from fontTools.ttLib import TTFont
from fontTools.varLib.avar.build import build as avar2_build
from fontTools.varLib.avar.map import map as avar2_map
from ufoProcessor.ufoOperator import UFOOperator
from mutatorMath.objects.location import Location
from xTools4.modules.encoding import psname2char
from xTools4.modules.sys import timer


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
    char = psname2char(glyphName)
    upm = TTFont(ttfPath)['head'].unitsPerEm
    B = BezierPath()
    B.text(char, font=ttfPath, fontSize=upm)
    DB.drawPath(B)

def getGlyphTTF_old(ttfPath, glyphName, location):
    char = psname2char(glyphName)
    glyphSet = TTFont(ttfPath).getGlyphSet()
    ttGlyph = glyphSet[glyphName]
    glyph = RGlyph()
    pen = glyph.getPen()
    ttGlyph.draw(pen)
    glyph.width = ttGlyph.width
    return glyph

def getVarDistance(location, defaultLocation):
    n = 0
    for key, value in location.items():
        defaultValue = defaultLocation.get(key)
        if value != defaultValue:
            n += 1
    return n

def getGlyphTTF(ttfPath, glyphName, location):

    char = psname2char(glyphName)

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


class BlendsPreview:

    margin      = 40
    glyphScale  = 0.045
    cellSize    = 2000
    labelsSize  = 5

    compare     = False
    wireframe   = False
    margins     = False
    labels      = False
    levels      = False
    levelsShow  = 1

    opszs = [8, 14, 144]
    wghts = [100, 400, 1000]
    wdths = [50, 100, 125]

    pointRadius = 10

    compareColors = [
        (1, 0, 1), # blended font
        (0, 1, 1), # reference font
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

    @property
    def parametricAxes(self):
        return self.operator.doc.default.location.keys()

    @property
    def blendedAxes(self):
        allAxes = [axis.name for axis in self.operator.doc.axes]
        return list(set(allAxes).difference(set(self.parametricAxes)))

    def getColors(self, level=0):
        colors = {
            'fillHeader2'    : (0,),
            'fill2'          : (0,),
            'stroke2'        : None,
            'points2'        : None,
            'strokeMargins2' : (0,),
        }
        if self.wireframe:
            colors['fill2']   = None
            colors['stroke2'] = 0,
            colors['points2'] = 0,

        levelColor = self.levelsColors[level]

        if self.compare and not self.levels:
            colors['fillHeader2']    = self.compareColors[1]
            colors['fill2']          = self.compareColors[1]
            colors['strokeMargins2'] = self.compareColors[1]

            colors['fillHeader1']    = self.compareColors[0]
            colors['fill1']          = self.compareColors[0]
            colors['strokeMargins1'] = self.compareColors[0]
            colors['stroke1']        = None
            colors['points1']        = None

            if self.wireframe:
                colors['fill2']   = None
                colors['stroke2'] = self.compareColors[1]
                colors['points2'] = self.compareColors[1]

                colors['fill1']   = None
                colors['stroke1'] = self.compareColors[0]
                colors['points1'] = self.compareColors[0]

        elif not self.compare and self.levels:
            colors['fill2']          = levelColor
            colors['strokeMargins2'] = levelColor

            if self.wireframe:
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

            if self.wireframe:
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

        w = cellWidth  * len(self.wdths) + self.margin * 2
        h = cellHeight * len(self.wghts) * len(self.opszs) + self.margin * 2
        x = y = self.margin

        DB.newPage(w, h)
        DB.blendMode('multiply')

        # no glyph = empty page
        if glyphName is None:
            return

        # get color scheme for current settings
        colors = self.getColors()

        defaultFont = Font(self.operator.doc.default.path)
        defaultBlendedLocation = { a.tag : a.default for a in self.operator.doc.axes if a.name in self.blendedAxes }

        # draw page header: font name(s) / glyph name
        with DB.savedState():
            m = self.margin / 2
            DB.translate(0, DB.height()-m)
            DB.fill(*colors['fillHeader2'])
            DB.text(defaultFont.info.familyName, (m, 0))
            if self.compare:
                DB.save()
                DB.translate(DB.textSize(f'{defaultFont.info.familyName} ')[0] + m, 0)
                DB.fill(*colors['fillHeader1'])
                DB.text(self.compareFont['name'].getDebugName(1), (0, 0))
                DB.restore()

            DB.fill(0,)
            DB.text(glyphName, (DB.width()-m, 0), align='right')

        #-------------
        # draw glyphs
        #-------------

        r = self.pointRadius

        DB.translate(x, y)

        axis1Tag, axis1Values = self.axesList[0]
        axis2Tag, axis2Values = self.axesList[1]
        axis3Tag, axis3Values = self.axesList[2]

        # get UPM of the reference font (if available)
        if self.compare and self.compareFont:
            unitsPerEm2 = self.compareFont['head'].unitsPerEm

        for i, axisValue1 in enumerate(axis1Values):
            for j, axisValue2 in enumerate(axis2Values):
                for k, axisValue3 in enumerate(axis3Values):
                    blendedLocation = {
                        axis1Tag: axisValue1,
                        axis2Tag: axisValue2,
                        axis3Tag: axisValue3,
                    }
                    styleName = f'{axis1Tag}{axisValue1} {axis2Tag}{axisValue2} {axis3Tag}{axisValue3}'

                    parametricLocation = getEffectiveLocation(self.designspacePath, blendedLocation)
                    g2 = instantiateGlyph(self.operator, glyphName, parametricLocation)

                    if not g2:
                        continue

                    # get var distance
                    n = getVarDistance(blendedLocation, defaultBlendedLocation)

                    if n >= self.levelsShow:
                        continue

                    colors = self.getColors(n)

                    DB.save()
                    DB.translate(k * cellWidth, j * cellHeight)

                    # draw location name
                    if self.labels:
                        with DB.savedState():
                            DB.rotate(90)
                            DB.fill(0)
                            DB.font('Menlo')
                            DB.fontSize(self.labelsSize)
                            DB.text(styleName, (0, 10))

                    DB.scale(self.glyphScale)

                    # draw blended glyph
                    if self.wireframe:
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

                    drawGlyph(g2)

                    if self.wireframe and points2 is not None:
                        DB.fill(*points2)
                        DB.stroke(None)
                        for c in g2:
                            for p in c:
                                DB.oval(p.x-r, p.y-r, r*2, r*2)

                    if self.margins:
                        yBottom = defaultFont.info.descender
                        yTop    = defaultFont.info.unitsPerEm - abs(yBottom)
                        DB.strokeWidth(1)
                        DB.stroke(*colors['strokeMargins2'])
                        DB.line((0, yBottom), (0, yTop))
                        DB.line((g2.width, yBottom), (g2.width, yTop))

                    # draw reference glyph
                    if self.compare and self.compareFont:

                        # TO-DO: switch to uharfbuzz
                        # T = DB.FormattedString()
                        # T.font(self.compareFontPath)
                        # T.fontVariations(**blendedLocation)
                        # T.fontSize(unitsPerEm2)
                        # T.appendGlyph(glyphName)

                        # B = DB.BezierPath()
                        # B.text(T, (0, 0))

                        g1 = getGlyphTTF(self.compareFontPath, glyphName, blendedLocation)

                        if self.wireframe:
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

                        # DB.drawPath(B)

                        # if self.wireframe and points1 is not None:
                        #     DB.stroke(None)
                        #     DB.fill(*points1)
                        #     for p in B.points:
                        #         DB.oval(p[0]-r, p[1]-r, r*2, r*2)

                        # if self.margins:
                        #     g1_width = DB.textSize(T)[0]
                        #     DB.strokeWidth(1)
                        #     DB.stroke(*colors['strokeMargins1'])
                        #     DB.line((0, yBottom), (0, yTop))
                        #     DB.line((g1_width, yBottom), (g1_width, yTop))

                        drawGlyph(g1)

                        if self.wireframe and points1 is not None:
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

            DB.translate(0, cellHeight*3)

    def save(self, pdfPath):
        DB.saveImage(pdfPath)


if __name__ == '__main__':

    start = time.time()

    srcFolder = '/Users/gferreira/hipertipo/fonts/fontbureau/amstelvar-avar2/'
    designspacePath = os.path.join(srcFolder, 'Sources', 'Roman', 'AmstelvarA2-Roman_avar2.designspace')
    compareFontPath = os.path.join(srcFolder, 'Fonts', 'legacy', 'Amstelvar-Roman[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,wdth,wght,opsz].ttf')

    axesList = [
        ('opsz', (8, 14, 144)),
        ('wght', (100, 400, 1000)),
        ('wdth', (50, 100, 125)),
    ]

    glyphNames = ['P']

    B = BlendsPreview(designspacePath)
    B.compareFontPath = compareFontPath
    B.axesList = axesList

    # proof settings
    B.compare    = True
    B.margins    = True
    B.labels     = True
    B.levels     = False
    B.wireframe  = False
    B.levelsShow = 2

    for glyphName in glyphNames:
        B.draw(glyphName)

    end = time.time()
    timer(start, end)
