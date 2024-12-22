import ezui
from merz import MerzView
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.roboFont import OpenWindow, CurrentGlyph, CurrentFont, AllFonts, RGlyph
from mojo.events import postEvent
from mojo.UI import UpdateCurrentGlyphView


KEY = 'com.hipertipo.xTools4.dialogs.glyph.interpolationPreview'


class InterpolationPreviewController(ezui.WindowController):

    title    = 'interpolation'
    width    = 123
    margins  = 10

    font1    = None
    glyph1   = None

    allFonts = {}

    content = """
    (_ ...)           @font2
    (_ ...)           @layers2
    [__]              @glyph2

    --X-----          @steps

    * ColorWell       @color

    [X] align center  @alignCenter
    [X] show steps    @showSteps
    [X] show lines    @showLines
    [X] show report   @showReport
    [X] show preview  @showPreview

    --------------------------------

    starting point
    ((( ← | → )))     @startingPoint

    contour index
    ((( ← | → )))     @contourIndex
    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small"
        ),
        font2=dict(
            callback='settingsChangedCallback',
            width='fill'
        ),
        layers2=dict(
            callback='settingsChangedCallback',
            width='fill'
        ),
        glyph2=dict(
            callback='settingsChangedCallback',
        ),
        steps=dict(
            callback='settingsChangedCallback',
            value=3,
            minValue=1,
            maxValue=11,
            tickMarks=11,
            stopOnTickMarks=True,
        ),
        color=dict(
            color=(1, 0, 1, 0.65),
            callback='settingsChangedCallback',
        ),
        startingPoint=dict(
            sizeStyle="regular",
            width="fill",
        ),
        contourIndex=dict(
            sizeStyle="regular",
            width="fill",
        ),
    )

    def build(self):
        self.w = ezui.EZPanel(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            margins=self.margins,
            size=(self.width, 'auto'),
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    def started(self):
        InterpolationPreviewGlyphEditor.controller = self
        InterpolationPreviewRoboFont.controller = self
        registerGlyphEditorSubscriber(InterpolationPreviewGlyphEditor)
        registerRoboFontSubscriber(InterpolationPreviewRoboFont)
        self.font1 = CurrentFont()
        self.settingsChangedCallback(None)

    def destroy(self):
        unregisterGlyphEditorSubscriber(InterpolationPreviewGlyphEditor)
        unregisterRoboFontSubscriber(InterpolationPreviewRoboFont)
        InterpolationPreviewGlyphEditor.controller = None
        InterpolationPreviewRoboFont.controller = None

    # dynamic attrs

    @property
    def font2(self):
        fontName2 = self.w.getItem("font2").getItem()
        return self.allFonts.get(fontName2)

    @property
    def layer2(self):
        return self.w.getItem("layers2").getItem()

    @property
    def layer2(self):
        return self.w.getItem("layers2").getItem()

    @property
    def glyphName2(self):
        return self.w.getItem("glyph2").get().strip()

    # callbacks

    def alignCenterCallback(self, sender):
        self.settingsChangedCallback(None)

    def showLinesCallback(self, sender):
        self.settingsChangedCallback(None)

    def showStepsCallback(self, sender):
        self.settingsChangedCallback(None)

    def showReportCallback(self, sender):
        self.settingsChangedCallback(None)

    def showPreviewCallback(self, sender):
        self.settingsChangedCallback(None)

    def startingPointCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        direction = sender.get()
        g.prepareUndo('changed starting points')
        for contour in g.selectedContours:
            if direction: # next
                contour.setStartSegment(+1)
            else: # previous
                contour.setStartSegment(-1)
        g.performUndo()

    def contourIndexCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        direction = sender.get()

        # record contour selection
        selection = [ci for ci, c in enumerate(g) if c.selected]

        # make temp copy of contours to change order
        contours = list(g.copy().contours)
        for ci, contour in enumerate(g.contours):
            if ci in selection:
                # next
                if direction:
                    newIndex = (ci + 1) % len(contours)
                # previous
                else:
                    newIndex = (ci - 1) % len(contours)
                contours.insert(newIndex, contours.pop(ci))

        # update glyph contours
        g.prepareUndo('changed contour order')
        g.clearContours()
        for c in contours:
            g.appendContour(c)
        g.performUndo()

        # restore contour selection
        # DOES NOT WORK IF NEW INDEX WRAPS AROUND
        if direction:
            selection = [(i+1) % len(g) for i in selection]
        else:
            selection = [(i-1) % len(g) for i in selection]

        for ci, contour in enumerate(g.contours):
            contour.selected = ci in selection

    def settingsChangedCallback(self, sender):
        postEvent(f"{KEY}.changed")


class InterpolationPreviewGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        
        # create preview layer 
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="background",
        )
        self.interpolationPreviewLayer = container.appendBaseSublayer()

        # create report layer
        size = 10000
        self.merzView = MerzView((0, 0, size, size))
        merzContainer = self.merzView.getMerzContainer()
        color = self.controller.w.getItem('color').get()
        self.reportLayer = merzContainer.appendTextBoxSublayer(
            name=f'{KEY}.report',
            position=(0, 0),
            size=(size, size),
            padding=(10, 10),
            fillColor=color,
            font='Menlo-Bold',
            pointSize=13,
            lineHeight=18,
            horizontalAlignment="left",
        )
        glyphEditor.addGlyphEditorSubview(self.merzView)

        # initialize preview
        self.controller.glyph1 = CurrentGlyph()
        self._drawInterpolationPreview()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        # remove preview layer
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="background",
        )
        container.clearSublayers()
        # remove report layer
        glyphEditor.removeGlyphEditorSubview(self.merzView)

    def interpolationPreviewDidChange(self, info):
        self._drawInterpolationPreview()

    def glyphEditorDidSetGlyph(self, info):
        # print('glyphEditorDidSetGlyph')
        self.controller.glyph1 = info["glyph"]
        self._drawInterpolationPreview()

    def glyphEditorGlyphDidChangeOutline(self, info):
        # print('glyphEditorGlyphDidChangeOutline')
        self._drawInterpolationPreview()

    def _drawInterpolationPreview(self):
        showPreview = self.controller.w.getItem('showPreview').get()
        showReport  = self.controller.w.getItem('showReport').get()

        self.interpolationPreviewLayer.clearSublayers()
        self.reportLayer.setVisible(showPreview and showReport)
        if not showPreview:
            return

        glyph1 = self.controller.glyph1

        font2      = self.controller.font2
        layerName2 = self.controller.layer2
        glyphName2 = self.controller.glyphName2

        if not glyphName2:
            glyphName2 = glyph1.name

        if glyph1 is None:
            return

        if font2 is None:
            return

        if glyphName2 not in font2:
            return

        glyph2 = font2[glyphName2].getLayer(layerName2)
        isCompatible, report = glyph1.isCompatible(glyph2)

        steps       = int(self.controller.w.getItem('steps').get())
        color       = self.controller.w.getItem('color').get()
        alignCenter = self.controller.w.getItem('alignCenter').get() 
        showSteps   = self.controller.w.getItem('showSteps').get()
        showLines   = self.controller.w.getItem('showLines').get()

        g1, g2 = glyph1, glyph2.copy()
        if alignCenter:
            delta = -(g2.width - g1.width) * 0.5
            g2.moveBy((delta, 0))

        # draw interpolation steps
        if showSteps:
            steps += 2
            step = 1.0 / (steps - 1)
            with self.interpolationPreviewLayer.sublayerGroup():
                for i in range(0, steps):
                    factor = 1.0 - i * step
                    g = RGlyph()
                    g.interpolate(factor, g1, g2)
                    sw = 1 # 2 if (i == 0 or i == steps-1) else 1
                    glyphsLayer = self.interpolationPreviewLayer.appendPathSublayer(
                        fillColor=None,
                        strokeColor=color,
                        strokeWidth=sw,
                    )
                    glyphPath = g.getRepresentation("merz.CGPath")
                    glyphsLayer.setPath(glyphPath)

        # draw lines between points
        if showLines:
            with self.interpolationPreviewLayer.sublayerGroup():
                for c1, c2 in zip(g1.contours, g2.contours):
                    for p1, p2 in zip(c1.points, c2.points):
                        dash = (2, 2) if p1.type == 'offcurve' else None
                        linesLayer = self.interpolationPreviewLayer.appendLineSublayer(
                            startPoint=(p1.x, p1.y),
                            endPoint=(p2.x, p2.y),
                            strokeWidth=1,
                            strokeColor=color,
                            strokeDash=dash,
                        )
            # draw glyph2 points
            dotSize = 4
            with self.interpolationPreviewLayer.sublayerGroup():
                for c in g2:
                    for pt in c.points:
                        symbol = self.interpolationPreviewLayer.appendSymbolSublayer(
                            position=(pt.x, pt.y),
                        )
                        symbol.setImageSettings(
                            dict(
                                name="oval",
                                size=(dotSize, dotSize),
                                strokeWidth=None,
                                fillColor=color,
                            )
                        )

        # display report 
        captionSize = 13
        with self.reportLayer.propertyGroup():
            self.reportLayer.setText(report.report())
            self.reportLayer.setFillColor(color)
            self.reportLayer.setPointSize(captionSize)


class InterpolationPreviewRoboFont(Subscriber):

    def build(self):
        self._updateFonts()
        self._updateLayers()

    def _updateFonts(self):
        self.controller.font1 = CurrentFont()
        allFonts = AllFonts()
        # no fonts open
        if not len(allFonts):
            self.controller.allFonts = {}
            self.controller.w.getItem("font2").setItems([])
            return
        # update fonts list
        self.controller.allFonts = {f"{f.info.familyName} {f.info.styleName}" : f for f in allFonts}
        allFontNames = sorted(self.controller.allFonts.keys())
        self.controller.w.getItem("font2").setItems(allFontNames)

    def _updateLayers(self):
        # glyph1 = CurrentGlyph()

        if self.controller.font1 is None or self.controller.font2 is None: # or not glyph1:
            self.controller.w.getItem("layers2").setItems([])
            return

        # 1. switching glyphs in same layer/font: don't change layers list
        # if self.glyph is not None and self._currentGlyph != glyph1.name:
        #     return

        # 2. switching fonts: update layers list (all layers)
        layerNames = list(self.controller.font2.layerOrder)

        # 3. switching layer in same font: remove current layer
        # if self.font1 == self.font2:
        #     layers.remove(glyph1.layer.name)

        self.controller.w.getItem("layers2").setItems(layerNames)

    def fontDocumentDidBecomeCurrent(self, info):
        self.controller.font1 = CurrentFont()
        self._updateFonts()
        self._updateLayers()

    # def fontDocumentDidOpen(self, info):
    #     self.controller.font1 = CurrentFont()
    #     self._updateFonts()
    #     self._updateLayers()

    def fontDocumentDidClose(self, info):
        self.controller.font1 = CurrentFont()
        self._updateFonts()
        self._updateLayers()

    def roboFontDidSwitchCurrentGlyph(self, info):
        # self._updateFonts()
        # self._updateLayers()
        pass


interpolationPreviewEvent = f"{KEY}.changed"

if interpolationPreviewEvent not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=interpolationPreviewEvent,
        methodName="interpolationPreviewDidChange",
        lowLevelEventNames=[interpolationPreviewEvent],
        documentation="Send when the interpolation preview window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(InterpolationPreviewController)
