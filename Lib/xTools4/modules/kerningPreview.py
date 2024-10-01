from importlib import reload
import variableValues.kerningPairPlus 
reload(variableValues.kerningPairPlus)

import os
import drawBot as DB
from fontParts.world import OpenFont, NewFont, RGlyph
from fontTools.pens.transformPen import TransformPointPen
from fontTools.designspaceLib import DesignSpaceDocument
from defcon import Font
from defcon.objects.component import _defaultTransformation
from variableValues.designspacePlus import DesignSpacePlus
from variableValues.kerningPairPlus import KerningPairPlus


def drawGlyph(g):
    B = DB.BezierPath()
    g.draw(B)
    DB.drawPath(B)


class DecomposePointPen:

    def __init__(self, glyphSet, outPointPen):
        self._glyphSet = glyphSet
        self._outPointPen = outPointPen
        self.beginPath = outPointPen.beginPath
        self.endPath = outPointPen.endPath
        self.addPoint = outPointPen.addPoint

    def addComponent(self, baseGlyphName, transformation, *args, **kwargs):
        if baseGlyphName in self._glyphSet:
            baseGlyph = self._glyphSet[baseGlyphName]
            if transformation == _defaultTransformation:
                baseGlyph.drawPoints(self)
            else:
                transformPointPen = TransformPointPen(self, transformation)
                baseGlyph.drawPoints(transformPointPen)


class VariableKerningPreview:

    sampleWidth    = 1000
    sampleHeight   = 100
    sampleScale    = 0.045
    sampleFontSize = 120

    verbose = True

    showMetrics  = False
    showKerning  = False
    showValue    = True
    showFontName = False

    _kerning = {}
    _allPairs = []

    selectedSources = []

    category1 = None
    category2 = None

    def __init__(self, designspacePath):
        self.designspace = DesignSpacePlus(designspacePath)

    @property
    def sources(self):
        return { os.path.splitext(os.path.split(src.path)[-1])[0]: src.path for src in self.designspace.document.sources }

    def loadKerning(self):

        # collect pairs and kerning values in selected sources
        self._allPairs = []
        self._kerning = {}

        for source in self.selectedSources:
            # print(source)

            sourcePath = self.sources[source]
            f = OpenFont(sourcePath, showInterface=False)

            self._allPairs += f.kerning.keys()
            self._kerning[source] = {}
            for pair, value in f.kerning.items():
                g1, g2 = pair
                if g1 not in f and g1 not in f.groups:
                    continue
                if g2 not in f and g2 not in f.groups:
                    continue
                self._kerning[source][pair] = value

        self._allPairs = list(set(self._allPairs))
        self._allPairs.sort()

    def _drawPreview(self, font, fontName, glyphNames, gNames, pos):

        x, y = pos

        DB.save()
        for i, glyphName in enumerate(glyphNames):
            if glyphName is None:
                continue

            if glyphName not in font:
                if self.verbose:
                    print(f'ERROR: glyph {glyphName} not in {fontName}...')
                continue

            g = font[glyphName]

            # flatten components
            if len(g.components):
                _g = RGlyph()
                pointPen = _g.getPointPen()
                decomposePen = DecomposePointPen(font, pointPen)
                g.drawPoints(decomposePen)
                _g.width = g.width
                g = _g

            DB.save()
            DB.translate(x, y)
            DB.scale(self.sampleScale)

            # draw font name caption    
            if i == 0 and self.showFontName:
                DB.fill(1, 0, 0)
                DB.fontSize(self.sampleFontSize)
                DB.text(fontName, (x, -font.info.unitsPerEm*0.15), align='left')

            # draw glyph margins
            if self.showMetrics:
                DB.strokeWidth(1)
                DB.stroke(1, 0, 0)
                DB.line((0, -font.info.unitsPerEm*0.2), (0, font.info.unitsPerEm*0.8))

            DB.stroke(None)
            DB.fill(0)
            drawGlyph(g)

            if not i < len(glyphNames)-1:
                continue

            # get glyph for preview
            gNameNext = gNames[i+1]
            if gNameNext.startswith('public.kern'):
                glyphNameNext = font.groups[gNameNext][0]
            else:
                glyphNameNext = gNameNext
            
            if glyphNameNext not in font:
                continue

            gNext = font[glyphNameNext]

            # get glyph/group for current glyph name
            gName = gNames[i]

            # get value for pair
            value = self._kerning[fontName].get((gName, gNameNext)) # font.kerning.get((gName, gNameNext)) # font.kerning.find((gName, gNameNext))

            if value:
                # draw kerning value
                if self.showKerning:
                    DB.fill(1, 0, 0, 0.3)
                    DB.rect(g.width + value, -font.info.unitsPerEm*0.2, -value, font.info.unitsPerEm)
                # draw caption value
                if self.showValue:
                    DB.fill(1, 0, 0)
                    DB.fontSize(self.sampleFontSize)
                    DB.text(str(value), (g.width -10, -font.info.unitsPerEm*0.15), align='right')

                # apply kern value with next glyph
                x += value * self.sampleScale

            DB.restore()

            # advance to next glyph
            x += g.width * self.sampleScale

        DB.restore()

    def draw(self):

        # print('KERNING', self._kerning.keys())
        # print()
        # print('SOURCES', self.sources.keys())
        # print()

        pairs = []
        for i, pair in enumerate(self._allPairs):
            drawn = self.drawPair((pair, i))
            if drawn:
                pairs.append(pair)
        return pairs

    def drawPair(self, currentPair):

        pair, pairIndex = currentPair

        for n, fontName in enumerate(self._kerning.keys()):
            ufoPath = self.sources[fontName]

            f = Font(ufoPath) # OpenFont(ufoPath, showInterface=False)
            P = KerningPairPlus(f, pair)

            if not (self.category1 is None and self.category2 is None):
                if not (self.category1 == P.category1 and self.category2 == P.category2):
                    return

            s  = self.sampleScale
            x  = 10
            fs = self.sampleFontSize

            if n == 0:
                DB.newPage(self.sampleWidth, len(self._kerning) * self.sampleHeight)
                DB.blendMode('multiply')
                y = DB.height() - self.sampleHeight * 0.8

            # draw the preview
            self._drawPreview(f, fontName, P.glyphNames, P.gNames, (x, y))

            y -= self.sampleHeight

        return True


if __name__ == '__main__':

    # run in RF DrawBot extension

    designspacePath = '/Users/gferreira/hipertipo/fonts/roboto-flex/sources/RobotoFlex.designspace'

    V = VariableKerningPreview(designspacePath)
    V.showMetrics  = True
    V.showKerning  = True
    V.showValue    = True
    V.showFontName = True

    # select some sources
    V.selectedSources = list(V.sources.keys())[:5]
    
    # load kerning for these sources
    V.loadKerning()

    # select a kerning pair by index
    pairIndex = 2
    
    # preview selected pair / sources 
    V.drawPair((V._allPairs[pairIndex], pairIndex))

