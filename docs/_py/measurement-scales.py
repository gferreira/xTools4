import os
from xTools4.modules.measurements import *

subfamily = ['Roman', 'Italic'][0]
amstevarA2Folder = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/'
sourcesFolder    = os.path.join(amstevarA2Folder, 'Sources', subfamily)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
measurements     = readMeasurements(measurementsPath)

def getSource(srcName):
    sourcePath = os.path.join(sourcesFolder, f'AmstelvarA2-{subfamily}_{srcName}.ufo')
    return OpenFont(sourcePath, showInterface=False)

def _drawGlyph(g, m, c, value):
    r = 6
    stroke(0)
    fill(None)
    drawGlyph(g)
    with savedState():
        stroke(*c)
        strokeWidth(20)
        line((m.point1.x, m.point1.y), (m.point2.x, m.point2.y))
        xx = m.point1.x + (m.point2.x - m.point1.x)/2
        yy = m.point1.y + (m.point2.y - m.point1.y)/2
        fill(*c)
        stroke(None)
        fontSize(fs*1.5)
        text(str(value), (xx, yy+fs*1.5), align='center')
        
def _drawTitle(g, txt1, txt2, c):
    stroke(None)
    fill(*c)
    fontSize(fs) 
    text(txt1, ((g.width/2)*s, yTop), align='center')
    fill(0)
    fontSize(fs/2) 
    text(txt2, ((g.width/2)*s, yTop-sy), align='center')   

def _drawScale(txtScale, value1, c1, value2, c2, sscale):
    T = FormattedString()
    T.fontSize(fs*0.75)
    T.append(txtScale)
    T.fill(*c1)
    T.append(str(value1))
    T.fill(0)
    T.append(' / ')
    T.fill(*c2)
    T.append(str(value2))
    T.fill(0)
    T.append(f' = {sscale:.3f}')

    text(T, (width()/2, my-dy), align='center')

# ---------
# variables
# ---------

my = 100
s  = 0.23
fs = 32
dy = 65
sy = 25
ty = 220
yt = 145

cF = 0.5, 0, 1
cG = 1, 0.5, 0
cD = 1, 0, 0.5

# ------------
# parent scale
# ------------

A   = 'XOLC'
B   = 'XOPQ' 
src = 'wght400'

txtA = 'font-level measurement\ncurrent font'
txtB = 'font-level measurement\ncurrent font'

txtScale = 'parent scale = '

f = getSource(src)

mA = Measurement(A, measurements['font'][A]['direction'], measurements['font'][A]['glyph 1'], measurements['font'][A]['point 1'], measurements['font'][A]['glyph 2'], measurements['font'][A]['point 2'])
valueUnitsA = mA.measure(f)

mB = Measurement(B, measurements['font'][B]['direction'], measurements['font'][B]['glyph 1'], measurements['font'][B]['point 1'], measurements['font'][B]['glyph 2'], measurements['font'][B]['point 2'])

valueUnitsB = mB.measure(f)
parentScale = valueUnitsA / valueUnitsB

glyphNameA = measurements['font'][A]['glyph 1']
gA = f[glyphNameA]

glyphNameB = measurements['font'][B]['glyph 1']
gB = f[glyphNameB]

W, H = sizes('A4Landscape')
H = f.info.capHeight*s + ty
yTop = H - yt

newPage(W, H)
save()

mx = (width() - (gA.width + gB.width) * s) / 2

translate(mx, my)

with savedState():
    _drawTitle(gA, A, txtA, cF)
    translate(gA.width*s, 0)
    _drawTitle(gB, B, txtB, cF)

with savedState():
    scale(s)
    _drawGlyph(gA, mA, cF, valueUnitsA)
    translate(gA.width)
    _drawGlyph(gB, mB, cF, valueUnitsB)

restore()

_drawScale(txtScale, valueUnitsA, cF, valueUnitsB, cF, parentScale)

# ----------
# font scale
# ----------

A      = 'XOLC' # glyph-level
B      = 'XOLC' # font-level
glyphA = 'u'

src = 'wght400'

txtA = 'glyph-level measurement\ncurrent font'
txtB = 'font-level measurement\ncurrent font'

txtScale = 'font scale = '

f = getSource(src)
gA = f[glyphA]

ID, gm = [(k, v) for k, v in measurements['glyphs'][glyphA].items() if v['name'] == A][1]

pt1, pt2 = ID.split()

mA = Measurement(A, gm['direction'], glyphA, pt1, glyphA, pt2)
valueUnitsA = mA.measure(f)

mB = Measurement(B, measurements['font'][B]['direction'], measurements['font'][B]['glyph 1'], measurements['font'][B]['point 1'], measurements['font'][B]['glyph 2'], measurements['font'][B]['point 2'])

valueUnitsB = mB.measure(f)
fontScale = valueUnitsA / valueUnitsB

gB = f[measurements['font'][B]['glyph 1']]

W, H = sizes('A4Landscape')
H = f.info.xHeight*s + ty
yTop = H - yt
newPage(W, H)
save()
fontSize(fs)

mx = (width() - (gA.width + gB.width) * s) / 2

translate(mx, my)

with savedState():
    _drawTitle(gA, A, txtA, cG)
    translate(gA.width*s, 0)
    _drawTitle(gB, B, txtB, cF)

with savedState():
    scale(s)
    _drawGlyph(gA, mA, cG, valueUnitsA)
    translate(gA.width)
    _drawGlyph(gB, mB, cF, valueUnitsB)

restore()

_drawScale(txtScale, valueUnitsA, cG, valueUnitsB, cF, fontScale)

# -------------
# default scale
# -------------

A     = 'XOLC' # glyph-level
B     = 'XOLC' # font-level
glyph = 'u'

srcA = 'XOLC293'
srcB = 'wght400'

txtA = 'glyph-level measurement\ncurrent font'
txtB = 'glyph-level measurement\ndefault font'

txtScale = 'default scale = '

fA = getSource(srcA)
gA = fA[glyph]

fB = getSource(srcB)
gB = fB[glyph]

ID, gm = [(k, v) for k, v in measurements['glyphs'][glyphA].items() if v['name'] == A][1]

pt1, pt2 = ID.split()

mA = Measurement(A, gm['direction'], glyph, pt1, glyph, pt2)
valueUnitsA = mA.measure(fA)

mB = Measurement(A, gm['direction'], glyph, pt1, glyph, pt2)
valueUnitsB = mB.measure(fB)
defaultScale = valueUnitsA / valueUnitsB

newPage(W, H)
save()
fontSize(fs)

mx = (width() - (gA.width + gB.width) * s) / 2

translate(mx, my)

with savedState():
    _drawTitle(gA, A, txtA, cG)
    translate(gA.width*s, 0)
    _drawTitle(gB, B, txtB, cD)

with savedState():
    scale(s)
    _drawGlyph(gA, mA, cG, valueUnitsA)
    translate(gA.width)
    _drawGlyph(gB, mB, cD, valueUnitsB)

restore()

_drawScale(txtScale, valueUnitsA, cG, valueUnitsB, cD, defaultScale)

folder = os.path.dirname(os.getcwd())
imgsFolder = os.path.join(folder, 'images')
imgPath = os.path.join(imgsFolder, 'measurement-scale.png')

saveImage(imgPath, multipage=True)
