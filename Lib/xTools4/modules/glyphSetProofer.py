import os, glob, datetime
import drawBot as DB
from fontParts.world import OpenFont
from xTools4.modules.validation import *


def drawGlyph(glyph):
    B = DB.BezierPath()
    glyph.draw(B)
    DB.drawPath(B)

def decomposeGlyph(glyph):
    if glyph.components:
        g = RGlyph()
        pointPen = g.getPointPen()
        decomposePen = DecomposePointPen(glyph.font, pointPen)
        glyph.drawPoints(decomposePen)
        g.name    = glyph.name
        g.unicode = glyph.unicode
        g.width   = glyph.width
    else:
        g = glyph.copy()
    return g


class GlyphSetProofer:
    '''
    Visualize glyphset of UFO sources with validation checks against a default font.

    '''
    margins               = 25, 10, 10, 10
    stepsX                = 41
    stepsY                = 26
    colorContours         = 0,
    colorContoursEqual    = 0, 0.65, 1
    colorComponents       = 1, 0.35, 0
    colorComponentsEqual  = 1, 0.75, 0
    colorWarning          = 1, 0, 0
    colorAlpha            = 0.2
    colorCheckTrue        = 0.00, 0.85, 0.00
    colorCheckFalse       = 1.00, 0.00, 0.00
    colorCheckEqual       = 0.00, 0.33, 1.00
    headerFont            = 'Menlo'
    headerFontSize        = 8
    glyphScale            = 0.0047
    glyphBaseline         = 0.36
    cellStrokeColor       = 1,
    cellStrokeWidth       = 0.5
    cellLabelFont         = 'Menlo-Bold'
    cellLabelSize         = 3.5
    cellLabelEqual        = 0, 0, 1
    cellLabelCompatible   = 0, 1, 0
    cellLabelIncompatible = 1, 0, 0
    cellMarginsColor      = 0.93,

    checks = {
        'width'      : True,
        'left'       : True,
        'right'      : True,
        'points'     : True,
        'components' : True,
        'anchors'    : True,
        'unicodes'   : True,
    }

    def __init__(self, familyName, defaultFontPath, sourcePaths):
        self.familyName = familyName
        self.defaultFontPath = defaultFontPath
        self.sourcePaths = sourcePaths

    def _drawHeader(self, fontName, now, isDefault=False):
        m = self.margins
        if isDefault:
            fontName += ' (default)'
        DB.font(self.headerFont)
        DB.fontSize(self.headerFontSize)
        DB.text(f'{self.familyName}', (m[3], DB.height() - m[0] * 0.66), align='left')
        DB.text(fontName, (DB.width() / 2, DB.height() - m[0] * 0.66), align='center')
        DB.text(now, (DB.width() - m[1], DB.height() - m[0] * 0.66), align='right')

    def _drawGlyphCell(self, glyphName, font, defaultFont, pos, cellSize):

        s = self.glyphScale

        x, y = pos
        stepX, stepY = cellSize

        # glyph not in font: draw empty cell
        if glyphName not in font:
            with DB.savedState():
                DB.fill(*self.cellMarginsColor)
                DB.rect(x, y, stepX, stepY)
                DB.stroke(0.85)
                DB.line((x, y), (x + stepX, y + stepY))
                DB.line((x, y + stepY), (x + stepX, y))
            return

        currentGlyph = font[glyphName]
        defaultGlyph = defaultFont[glyphName]

        # decompose glyphs
        currentGlyph_flat = decomposeGlyph(currentGlyph)
        defaultGlyph_flat = decomposeGlyph(defaultGlyph)

        results = {
          'compatibility' : checkCompatibility(currentGlyph, defaultGlyph),
          'equality'      : checkEquality(currentGlyph, defaultGlyph),
        }

        # -------------
        # define colors
        # -------------

        glyphColor = bgColor = None

        # glyphs with components
        if currentGlyph.components:
            levels = getNestingLevels(currentGlyph)
            # warning: nested components of mixed contour/components
            if levels > 1 or len(currentGlyph.contours):
                bgColor    = self.colorWarning + (self.colorAlpha * 2,)
                glyphColor = self.colorWarning
            else:
                # components equal to default
                if all(results['compatibility']) and results['equality']['components']:
                    bgColor    = self.colorComponentsEqual + (self.colorAlpha,)
                    glyphColor = self.colorComponentsEqual
                # components different from default
                else:
                    bgColor    = self.colorComponents + (self.colorAlpha,)
                    glyphColor = self.colorComponents

        else:
            # contours equal to default
            if results['compatibility']['points'] and results['equality']['points']:
                if currentGlyph.width == defaultGlyph.width:
                    bgColor    = self.colorContoursEqual + (self.colorAlpha,)
                    glyphColor = self.colorContoursEqual
            else:
                # empty glyphs
                if not len(defaultGlyph) and not len(currentGlyph):
                    # width equal to default
                    if currentGlyph.width == defaultGlyph.width:
                        bgColor    = self.colorContoursEqual + (self.colorAlpha,)
                        glyphColor = self.colorContoursEqual

        # ---------
        # draw cell
        # ---------

        _x = x + (stepX - currentGlyph.width * s) / 2
        _y = y + stepY * self.glyphBaseline

        # draw left/right margins
        with DB.savedState():
            _margin = (stepX - currentGlyph.width * s) / 2
            DB.stroke(None)
            DB.fill(*self.cellMarginsColor)
            DB.rect(x, y, _margin, stepY)
            DB.rect(x + stepX, y, -_margin, stepY)

        # draw background color
        if bgColor is not None:
            with DB.savedState():
                DB.stroke(None)
                DB.translate(x, y)
                DB.fill(*bgColor)
                DB.rect(0, 0, stepX, stepY)

        # draw check results
        if font is not defaultFont and \
                glyphColor != self.colorContoursEqual and \
                glyphColor != self.colorComponentsEqual:

            with DB.savedState():
                DB.stroke(None)
                DB.translate(x, y)
                DB.font(self.cellLabelFont)
                DB.fontSize(self.cellLabelSize)

                for checkName in self.checks.keys():
                    # check is hidden
                    if not self.checks[checkName]:
                        continue

                    isCompatible = results['compatibility'].get(checkName)
                    isEqual      = results['equality'].get(checkName)

                    if isCompatible and isEqual:
                        DB.fill(*self.colorCheckEqual)
                        drawCheck = True
                    elif isCompatible or isEqual:
                        DB.fill(*self.colorCheckTrue)
                        drawCheck = False
                    else:
                        DB.fill(*self.colorCheckFalse)
                        drawCheck = True

                    if drawCheck:
                        label = checkName[0].upper()
                        DB.text(label, (1, 1))
                        w, h = DB.textSize(label)
                        DB.translate(w + 0.5, 0)

        # draw contours / components
        if currentGlyph.bounds:
            if glyphColor is None:
                glyphColor = 0,
            with DB.savedState():
                DB.stroke(None)
                DB.translate(_x, _y)
                DB.scale(s)
                DB.fill(*glyphColor)
                drawGlyph(currentGlyph_flat)

        # draw cell border
        DB.rect(x, y, stepX, stepY)


    def _makePage(self, font, defaultFont, now):

        m = self.margins

        glyphNames = defaultFont.glyphOrder

        DB.newPage('A4Landscape')

        stepX = (DB.width()  - m[1] - m[3]) / self.stepsX
        stepY = (DB.height() - m[0] - m[2]) / self.stepsY

        self._drawHeader(font.info.styleName, now, isDefault=(font.path == defaultFont.path))

        # draw cells
        DB.fill(None)
        DB.stroke(*self.cellStrokeColor)
        DB.strokeWidth(self.cellStrokeWidth)
        DB.fontSize(self.cellLabelSize)

        n = 0
        for i in range(self.stepsY):
            for j in range(self.stepsX):
                x = m[3] + j * stepX
                y = DB.height() - m[0] - (i + 1) * stepY

                if n > len(glyphNames) - 1:
                    break

                glyphName = glyphNames[n]

                self._drawGlyphCell(glyphName, font, defaultFont, (x, y), (stepX, stepY))

                n += 1

    def build(self, savePDF=False, folder=None):

        defaultFont = OpenFont(self.defaultFontPath, showInterface=False)
        sources     = [OpenFont(srcPath, showInterface=False) for srcPath in self.sourcePaths]
        sources.insert(0, defaultFont)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        DB.newDrawing()
        for font in sources:
            self._makePage(font, defaultFont, now)

        if savePDF:
            if folder is None:
                folder = os.getcwd()
            pdfPath = os.path.join(folder, f"glyphset_{self.familyName.replace(' ', '-')}.pdf")
            DB.saveImage(pdfPath)


class GlyphSetProoferDesignspace:
    '''
    TO-DO: Same as GlyphSetProofer but built around a designspace file.

    so instead of:
        GlyphSetProofer(familyName, defaultFontPath, sourcePaths)
    
    we can do:
        GlyphSetProoferDesignspace(designspace, sourceNames)

    as implemented in dialogs.GlyphSetProoferUI

    '''
    pass


