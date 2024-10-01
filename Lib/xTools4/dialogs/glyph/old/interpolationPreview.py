import os
from colorsys import hsv_to_rgb, rgb_to_hsv
from vanilla import TextBox, CheckBox, PopUpButton, Slider, RadioGroup, ColorWell, HorizontalLine, Button, EditText
from mojo import drawingTools as ctx
from drawBot import BezierPath
from fontParts.base.bPoint import absoluteBCPIn, absoluteBCPOut
from mojo.roboFont import AllFonts, CurrentFont, CurrentGlyph, RGlyph
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView, getDefault, CurrentGlyphWindow
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.modules.color import rgb2nscolor, nscolor2rgb


class InterpolationPreviewDialog(GlyphsDialogBase):

    '''
    A drawing helper which shows another font and intermediate interpolation steps in the Glyph View.

    ::
    
        from hTools3.dialogs.glyph.interpolationPreview import InterpolationPreviewDialog
        InterpolationPreviewDialog()

    '''

    title = 'interpolation'
    key   = f'{GlyphsDialogBase.key}.interpolationPreview'
    settings = {
        'steps'       : 7,
        'stepsMin'    : 1,
        'stepsMax'    : 12,
        'color2'      : (1, 0, 1, 0.65),
        'showPoints'  : False,
        'showSteps'   : True,
        'showLines'   : True,
        'alignCenter' : False,
    }
    allFonts = {}

    _currentGlyph = None

    def __init__(self):
        self.height  = self.textHeight * 10
        self.height += self.buttonHeight * 3
        self.height += self.padding * 10
        self.w = self.window((self.width, self.height ), self.title)

        x = y = p = self.padding
        self.w.font2 = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updateFont2Callback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.fontLayers = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.otherGlyph = EditText(
                (x, y, -p, self.textHeight),
                '',
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        ticksCount = self.settings['stepsMax'] - self.settings['stepsMin'] + 1
        self.w.steps = Slider(
                (x, y, -p, self.textHeight),
                value=self.settings['steps'],
                minValue=self.settings['stepsMin'],
                maxValue=self.settings['stepsMax'],
                tickMarkCount=ticksCount,
                stopOnTickMarks=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.color2 = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.settings['color2']),
                callback=self.updatePreviewCallback)

        y += self.buttonHeight + p
        self.w.showLines = CheckBox(
                (x, y, -p, self.textHeight),
                "show lines",
                value=self.settings['showLines'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.showSteps = CheckBox(
                (x, y, -p, self.textHeight),
                "show steps",
                value=self.settings['showSteps'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.alignCenter = CheckBox(
                (x, y, -p, self.textHeight),
                "align center",
                value=self.settings['alignCenter'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight # + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "show preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.separator = HorizontalLine((x, y, -p, 1))

        y += p + 2

        w = (self.width - p * 3) / 2
        self.w.startPointLabel = TextBox(
                (x, y, -p, self.textHeight),
                'starting point',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.2
        self.w.prevPoint = Button(
                (x, y, w, self.textHeight),
                "←",
                callback=self.prevPointCallback)

        x += w + p
        self.w.nextPoint = Button(
                (x, y, w, self.textHeight),
                "→",
                callback=self.nextPointCallback)

        x = self.padding
        y += self.textHeight + p
        self.w.contourIndexLabel = TextBox(
                (x, y, -p, self.textHeight),
                'contour index',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.2
        self.w.prevContour = Button(
                (x, y, w, self.textHeight),
                "←",
                callback=self.prevContourCallback)

        x += w + p
        self.w.nextContour = Button(
                (x, y, w, self.textHeight),
                "→",
                callback=self.nextContourCallback)

        self.updateFonts()
        # self.updateGlyph()
        self.updateLayers()

        self.initGlyphsWindowBehaviour()

        addObserver(self, "updateListsObserver",  "newFontDidOpen")
        addObserver(self, "updateListsObserver",  "fontDidOpen")
        addObserver(self, "updateListsObserver",  "fontDidClose")
        addObserver(self, "updateListsObserver",  "fontBecameCurrent")
        addObserver(self, "updateGlyphObserver",  "currentGlyphChanged")

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def font2(self):
        i = self.w.font2.get()
        font2 = self.allFonts[sorted(self.allFonts.keys())[i]]
        return font2

    @property
    def fontLayer(self):
        if not self.font2:
            return

        fontLayers = self.w.fontLayers.getItems()
        if not len(fontLayers):
            return

        i = self.w.fontLayers.get()
        return fontLayers[i]

    @property
    def steps(self):
        return int(self.w.steps.get()) + 1

    @property
    def showLines(self):
        return bool(self.w.showLines.get())

    @property
    def showSteps(self):
        return bool(self.w.showSteps.get())

    @property
    def alignCenter(self):
        return bool(self.w.alignCenter.get())

    @property
    def pointSize(self):
        return getDefault('glyphViewOffCurvePointsSize')

    @property
    def color2(self):
        return nscolor2rgb(self.w.color2.get())

    @property
    def otherGlyph(self):
        return self.w.otherGlyph.get()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontWillClose")
        removeObserver(self, "fontBecameCurrent")
        removeObserver(self, "drawBackground")
        removeObserver(self, "currentGlyphChanged")
        super().windowCloseCallback(sender)
        UpdateCurrentGlyphView()

    def updateFont2Callback(self, sender):
        self.updateLayers()
        UpdateCurrentGlyphView()

    def prevPointCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        for contour in g.selectedContours:
            contour.setStartSegment(-1)

    def nextPointCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        for contour in g.selectedContours:
            contour.setStartSegment(+1)

    def prevContourCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        for contour in g.selectedContours:
            contour.index = (contour.index - 1) % len(g)

    def nextContourCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        for contour in g.selectedContours:
            contour.index = (contour.index + 1) % len(g)

    # ---------
    # observers
    # ---------

    def updateListsObserver(self, notification):
        self.updateFonts()
        self.updateLayers()
        UpdateCurrentGlyphView()

    # def updateLayersObserver(self, notification):
    #     glyph = notification['glyph']
    #     if not glyph:
    #         return
    #     self.updateLayers()
    #     UpdateCurrentGlyphView()
        # self._currentGlyph = glyph.name

    def updateGlyphObserver(self, notification):
        glyph = notification['glyph']
        if glyph is None:
            return
        # self.updateGlyph()
        self._currentGlyph = glyph.name
        # self.w.otherGlyph.set(self._currentGlyph)
        # print(self._currentGlyph)

    def backgroundPreview(self, notification):

        g1    = notification['glyph']
        scale = notification['scale']

        # -----------------
        # assert conditions
        # -----------------

        if not g1 or not self.font1:
            return

        if not self.w.preview.get():
            return

        # if len(g1.components):
        #     if self.verbose:
        #         print('%s has components' % g1.name)
        #     return

        try:
            font2 = self.font2.getLayer(self.fontLayer)
        except:
            return

        # glyph not in font2 / layer
        if g1.name not in font2:
            # if self.verbose:
            #     print(f'{g1.name} not in font 2')
            return

        otherGlyph = self.otherGlyph if self.otherGlyph else g1.name

        try:
            g2 = font2[otherGlyph]
        except:
            return

        # ------------
        # draw preview
        # ------------

        self.drawPreview(g1, g2, scale)

    # -------
    # methods
    # -------

    def updateFonts(self):

        self.font1 = CurrentFont()

        allFonts = AllFonts()

        if not len(allFonts):
            self.allFonts = {}
            self.w.font2.setItems([])
            return

        self.allFonts = {f"{f.info.familyName} {f.info.styleName}" : f for f in allFonts}
        self.w.font2.setItems(sorted(self.allFonts.keys()))

    def updateGlyph(self):
        glyph = CurrentGlyph()
        if glyph is None:
            return
        self._currentGlyph = glyph.name
        self.w.otherGlyph.set(self._currentGlyph)
        # self.updateLayers()
        # UpdateCurrentGlyphView()

    def updateLayers(self):

        glyph1 = CurrentGlyph()

        if not self.font1 or not self.font2 or not glyph1:
            self.w.fontLayers.setItems([])
            return

        # 1. switching glyphs in same layer/font: don't change layers list
        if self._currentGlyph is not None and self._currentGlyph != glyph1.name:
            return

        # 2. switching fonts: update layers list (all layers)
        layers = list(self.font2.layerOrder)

        # 3. switching layer in same font: remove current layer
        # if self.font1 == self.font2:
        #     layers.remove(glyph1.layer.name)

        self.w.fontLayers.setItems(layers)

    def drawPreview(self, glyph1, glyph2, previewScale):

        window = CurrentGlyphWindow()
        x, y, w, h = window.getVisibleRect()

        isCompatible, report = glyph1.isCompatible(glyph2)

        g2 = glyph2.copy()
        if self.alignCenter:
            delta = -(g2.width - glyph1.width) * 0.5
            g2.moveBy((delta, 0))

        # ------------------------
        # draw errors and warnings
        # ------------------------

        if not isCompatible:
            ctx.save()
            ctx.font('Menlo-Bold')
            ctx.stroke(None)
            ctx.fill(*self.color2)
            ctx.fontSize(18 * previewScale)
            ctx.lineHeight(12 * previewScale)

            errors   = []
            warnings = []
            for L in str(report).split('\n'):
                if L.startswith('[Fatal]'):
                    L = L.replace('[Fatal] ', '')
                    errors.append(L)
                elif L.startswith('[Warning]'):
                    L = L.replace('[Warning] ', '')
                    warnings.append(L)

            if warnings:
                txt = "WARNINGS:\n"
                txt += '\n'.join(warnings)
                ctx.text(txt, (x, y))
                w, h = ctx.textSize(txt + '\n')
                y += h

            if errors:
                txt = "ERRORS:\n"
                txt += '\n'.join(errors)
                ctx.text(txt, (x, y))

            ctx.restore()

        # ------------------------
        # draw interpolation steps
        # ------------------------

        else:
            color3 = self.color2
            ctx.save()
            ctx.fill(None)

            if self.showSteps:
                for i in range(1, self.steps - 1):
                    factor = 1.0 - i * (1.0 / (self.steps - 1))
                    glyph3 = RGlyph()
                    glyph3.interpolate(factor, glyph1, glyph2)
                    ctx.save()

                    # move to center
                    if self.alignCenter:
                        delta = -(glyph3.width - glyph1.width) * 0.5
                        ctx.translate(delta, 0)

                    # draw glyph
                    ctx.fill(None)
                    ctx.stroke(*color3)
                    ctx.strokeWidth(1 * previewScale)
                    ctx.drawGlyph(glyph3)

                    ctx.restore()

            if self.showLines:
                ctx.stroke(*color3)
                ctx.lineCap('round')
                for c1, c2 in zip(glyph1.contours, g2.contours):
                    ctx.stroke(0, 0, 1)
                    for p1, p2 in zip(c1.bPoints, c2.bPoints):
                        # on-curve points
                        ctx.strokeWidth(2 * previewScale)
                        ctx.line(p1.anchor, p2.anchor)
                        # bezier handles
                        ctx.strokeWidth(1 * previewScale)
                        ctx.line(absoluteBCPIn(p1.anchor, p1.bcpIn), absoluteBCPIn(p2.anchor, p2.bcpIn))
                        ctx.line(absoluteBCPOut(p1.anchor, p1.bcpOut), absoluteBCPOut(p2.anchor, p2.bcpOut))
                        ctx.line(p1.anchor, absoluteBCPIn(p1.anchor, p1.bcpIn))
                        ctx.line(p1.anchor, absoluteBCPOut(p1.anchor, p1.bcpOut))
                        # ctx.line(p2.anchor, absoluteBCPIn(p2.anchor, p2.bcpIn))
                        # ctx.line(p2.anchor, absoluteBCPOut(p2.anchor, p2.bcpOut))
                    # off-curve points
                    ctx.stroke(*color3)
                    for p1, p2 in zip(c1.points, c2.points):
                        if p1.type == 'offcurve' and p2.type == 'offcurve':
                            ctx.strokeWidth(1 * previewScale)
                            ctx.lineDash(2 * previewScale, 4 * previewScale)
                        else:
                            ctx.strokeWidth(2 * previewScale)
                            ctx.lineDash(None)
                        ctx.line((p1.x, p1.y), (p2.x, p2.y))

            ctx.restore()

        # ------------
        # draw masters
        # ------------

        r = self.pointSize * previewScale

        ctx.save()
        ctx.fill(None)
        ctx.stroke(*self.color2)
        ctx.strokeWidth(2 * previewScale)
        ctx.drawGlyph(glyph1)
        ctx.drawGlyph(g2)
        # if self.showPoints:
        ctx.fill(None)
        ctx.stroke(*self.color2)
        for c in g2.contours:
            for pt in c.points:
                ctx.oval(pt.x - r, pt.y - r, r * 2, r * 2)
        ctx.restore()

# -------
# testing
# -------

if __name__ == '__main__':

    InterpolationPreviewDialog()
