import ezui
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.roboFont import OpenWindow, CurrentGlyph, CurrentFont, AllFonts, RGlyph
from mojo.events import postEvent


DEFAULT_KEY = 'com.hipertipo.hTools4.dialogs.glyph.interpolationPreview'
DEBUG = False


class InterpolationPreviewController(ezui.WindowController):

    title    = 'interpolation'
    width    = 123
    margins  = 10
    debug    = DEBUG

    font1    = None
    glyph1   = None

    allFonts = {}

    def build(self):
        content = """
        (_ ...)           @font2
        (_ ...)           @fontLayers
        [__]              @otherGlyph

        --X-----          @steps

        * ColorWell       @color

        [X] show lines    @showLines
        [X] show steps    @showSteps
        [X] align center  @alignCenter
        [X] show preview  @showPreview

        ----------------------------------

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
            fontLayers=dict(
                callback='settingsChangedCallback',
                width='fill'
            ),
            otherGlyph=dict(
                callback='settingsChangedCallback',
            ),
            steps=dict(
                callback='settingsChangedCallback',
                value=7,
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
        self.w = ezui.EZPanel(
            title=self.title,
            content=content,
            descriptionData=descriptionData,
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
        self.font1  = CurrentFont()
        # self.glyph1 = CurrentGlyph()

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

    # callbacks

    def showLinesCallback(self, sender):
        self.settingsChangedCallback(None)

    def showStepsCallback(self, sender):
        self.settingsChangedCallback(None)

    def alignCenterCallback(self, sender):
        self.settingsChangedCallback(None)

    def showPreviewCallback(self, sender):
        self.settingsChangedCallback(None)

    def startingPointCallback(self, sender):
        g = CurrentGlyph()
        if not g:
            return
        direction = sender.get()
        for contour in g.selectedContours:
            if direction: # next
                contour.setStartSegment(+1)
            else: # previous
                contour.setStartSegment(-1)

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
        g.clearContours()
        for c in contours:
            g.appendContour(c)

        # restore contour selection
        # DOES NOT WORK IF NEW INDEX WRAPS AROUND
        if direction:
            selection = [(i+1) % len(g) for i in selection]
        else:
            selection = [(i-1) % len(g) for i in selection]

        for ci, contour in enumerate(g.contours):
            contour.selected = ci in selection

    def settingsChangedCallback(self, sender):
        if self.debug:
            print('settingsChangedCallback')
        postEvent(f"{DEFAULT_KEY}.changed")


class InterpolationPreviewGlyphEditor(Subscriber):

    controller = None
    debug = DEBUG

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=DEFAULT_KEY,
            location="foreground",
        )
        self.interpolationPreviewLayer = container.appendBaseSublayer()
        self.controller.glyph1 = CurrentGlyph()
        self._drawInterpolationPreview()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(DEFAULT_KEY)
        container.clearSublayers()

    def interpolationPreviewDidChange(self, info):
        if self.debug:
            print('interpolationPreviewDidChange')
        self._drawInterpolationPreview()

    def glyphEditorDidSetGlyph(self, info):
        self.controller.glyph1 = info["glyph"]
        self._drawInterpolationPreview()

    def glyphEditorGlyphDidChangeOutline(self, info):
        self.controller.glyph1 = info["glyph"]
        self._drawInterpolationPreview()

    def _drawInterpolationPreview(self):
        self.interpolationPreviewLayer.clearSublayers()

        showPreview = self.controller.w.getItem('showPreview').get()
        if not showPreview:
            return

        glyph1 = self.controller.glyph1
        if glyph1 is None:
            return

        font2 = self.controller.font2
        if font2 is None:
            return

        glyphName2 = glyph1.name
        if glyphName2 not in font2:
            return

        glyph2 = font2[glyphName2]

        isCompatible, report = glyph1.isCompatible(glyph2)

        steps       = int(self.controller.w.getItem('steps').get())
        color       = self.controller.w.getItem('color').get()
        showSteps   = self.controller.w.getItem('showSteps').get()
        showLines   = self.controller.w.getItem('showLines').get()
        alignCenter = self.controller.w.getItem('alignCenter').get() 

        g1, g2 = glyph1, glyph2.copy()
        if alignCenter:
            delta = -(g2.width - g1.width) * 0.5
            g2.moveBy((delta, 0))

        if isCompatible:
            # draw interpolation steps
            if showSteps:
                steps += 2
                step = 1.0 / (steps - 1)
                with self.interpolationPreviewLayer.sublayerGroup():
                    for i in range(0, steps):
                        factor = 1.0 - i * step
                        g = RGlyph()
                        g.interpolate(factor, g1, g2)

                        sw = 2 if (i == 0 or i == steps-1) else 1

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
                with self.interpolationPreviewLayer.sublayerGroup():
                    r = 5 # get bezier point size from RF preferences?
                    for c in g2:
                        for pt in c.points:
                            self.interpolationPreviewLayer.appendOvalSublayer(
                                position=(pt.x-r, pt.y-r),
                                size=(r*2, r*2),
                                strokeWidth=1,
                                strokeColor=color,
                                fillColor=None,
                            )

        else:
            # display interpolation errors
            reportLayer = self.interpolationPreviewLayer.appendTextLineSublayer(
                position=(0, g1.font.info.xHeight),
                fillColor=color,
                text=report.report(),
                font='Menlo-Bold',
                pointSize=13,
                lineHeight=18,
                horizontalAlignment="left",
            )

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
            self.controller.w.getItem("fontLayers").setItems([])
            return

        # 1. switching glyphs in same layer/font: don't change layers list
        # if self.glyph is not None and self._currentGlyph != glyph1.name:
        #     return

        # 2. switching fonts: update layers list (all layers)
        layerNames = list(self.controller.font2.layerOrder)

        # 3. switching layer in same font: remove current layer
        # if self.font1 == self.font2:
        #     layers.remove(glyph1.layer.name)

        self.controller.w.getItem("fontLayers").setItems(layerNames)

    def fontDocumentDidBecomeCurrent(self, info):
        if self.debug:
            print('InterpolationPreviewRoboFont.fontDocumentDidBecomeCurrent')
        self.controller.font1 = CurrentFont()
        self._updateFonts()
        self._updateLayers()

    def fontDocumentDidOpen(self, info):
        if self.debug:
            print('InterpolationPreviewRoboFont.fontDocumentDidOpen')
        self.controller.font1 = CurrentFont()
        self._updateFonts()
        self._updateLayers()

    def fontDocumentDidClose(self, info):
        if self.debug:
            print('InterpolationPreviewRoboFont.fontDocumentDidClose')
        self.controller.font1 = CurrentFont()
        self._updateFonts()
        self._updateLayers()

    def roboFontDidSwitchCurrentGlyph(self, info):
        if self.debug:
            print('InterpolationPreviewRoboFont.roboFontDidSwitchCurrentGlyph')
        self._updateFonts()
        self._updateLayers()

    # def interpolationPreviewDidChange(self, info):
    #     print('InterpolationPreviewRoboFont.interpolationPreviewDidChange')


interpolationPreviewEvent = f"{DEFAULT_KEY}.changed"

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
