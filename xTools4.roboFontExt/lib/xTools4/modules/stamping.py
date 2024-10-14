'''
Create synthetic glyphs to insert when generating fonts.

'''

from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from xTools4.modules.encoding import char2psname
from xTools4.modules.unicode import autoUnicode as setAutoUnicode
from xTools4.modules.primitives import drawRectInGlyph

def makeVersionGlyph(font, captionFontPath, versionNumber, timestamp, glyphName='apple', scale=0.3, padding=120, lineHeight=1.2, autoUnicode=True):

    # based on example by Frederik Berlaen & Frank Grießhammer
    # http://groups.google.com/g/robofab/c/m8bvFVLtaWg
    # removed compositor dependency

    if glyphName not in font:
        font.newGlyph(glyphName)
    g = font[glyphName]
    g.clear()

    captionFont = TTFont(captionFontPath)
    glyphSet = captionFont.getGlyphSet()

    for i, txt in enumerate([timestamp, versionNumber]):
        glyphNames = [char2psname(char) for char in txt]

        y = i * captionFont['head'].unitsPerEm * lineHeight
        t = Transform()
        t = t.scale(scale)
        t = t.translate(0, y)

        for gName in glyphNames:
            pen = TransformPen(g.getPen(), t)
            sourceGlyph = glyphSet[gName]
            sourceGlyph.draw(pen)
            t = t.translate(sourceGlyph.width, 0)
            
    g.changed()
    captionFont.close()

    L, B, R, T = g.bounds
    W, H = R - L, T - B

    g.width = W + padding*2

    dx = (g.width - W) / 2
    dy = (font.info.capHeight - H) / 2

    g.moveBy((dx, dy))

    if autoUnicode:
        setAutoUnicode(g, verbose=False)

def makeNotdefGlyph(font, captionFontPath, strokeWidth=30, margin=60, scale=0.7):

    glyphName = '.notdef'
    sw = strokeWidth

    if glyphName not in font:
        font.newGlyph(glyphName)
    g = font[glyphName]
    g.clear()

    captionFont = TTFont(captionFontPath)
    glyphSet = captionFont.getGlyphSet()

    h = abs(font.info.descender) + font.info.ascender
    w = h * 0.7
    x = 0
    y = font.info.descender

    g.width = w

    t = Transform()
    t = t.scale(scale)
    pen = TransformPen(g.getPen(), t)
    sourceGlyph = glyphSet['question']
    sourceGlyph.draw(pen)

    L, B, R, T = g.bounds
    W, H = R-L, T-B
    x0 = (w - W) / 2
    y0 = (h - H) / 2

    g.moveBy((x0-L, y0+y))

    drawRectInGlyph(g, x, y, w, h)
    g[-1].reverse()
    drawRectInGlyph(g, x+sw, y+sw, w-sw*2, h-sw*2)

    g.leftMargin = margin
    g.width = w + margin*2
    g.changed()
