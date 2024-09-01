import ezui
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, unregisterGlyphEditorSubscriber
from mojo.roboFont import OpenWindow, CurrentGlyph
from mojo.events import postEvent
from hTools3.modules.curvatureVisualizer import *


DEFAULT_KEY = 'com.hipertipo.hTools4.dialogs.glyph.curvatureVisualizer'


def curvatureCombFactory(glyph, steps, scale):
    glyph = glyph.asFontParts().copy()
    glyph.clearComponents()
    return makeCurvatureCombGlyph(glyph, steps, scale)


class CurvatureVisualizerController(ezui.WindowController):

    title   = 'curvature'
    width   = 123
    margins = 10

    def build(self):
        content = """
        * ColorWell       @colorButton

        scale
        --X-----          @scale

        steps
        --X-----          @steps

        [X] show preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            colorButton=dict(
                callback='settingsChangedCallback',
                color=(0, 1, 0, 0.5),
            ),
            scale=dict(
                callback='settingsChangedCallback',
                value=1000,
                minValue=500,
                maxValue=5000,
            ),
            steps=dict(
                callback='settingsChangedCallback',
                value=20,
                minValue=10,
                maxValue=40,
            ),
            preview=dict(
                callback='settingsChangedCallback',
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
        registerRepresentationFactory(Glyph, f"{DEFAULT_KEY}.preview", curvatureCombFactory)
        CurvatureVisualizer.controller = self
        registerGlyphEditorSubscriber(CurvatureVisualizer)

    def destroy(self):
        unregisterRepresentationFactory(Glyph, f"{DEFAULT_KEY}.preview")
        unregisterGlyphEditorSubscriber(CurvatureVisualizer)
        CurvatureVisualizer.controller = None

    # callbacks

    def settingsChangedCallback(self, sender):
        postEvent(f"{DEFAULT_KEY}.changed")


class CurvatureVisualizer(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=DEFAULT_KEY,
            location="foreground",
        )
        self.curvatureVisualizerLayer = container.appendBaseSublayer()
        self.glyph = CurrentGlyph()
        self._drawCurvature()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(DEFAULT_KEY)
        container.clearSublayers()

    def curvatureVisualizerDidChange(self, info):
        self.glyph = self.getGlyphEditor().getGlyph().asFontParts()
        self._drawCurvature()

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self._drawCurvature()

    def glyphEditorGlyphDidChangeOutline(self, info):
        self.glyph = info["glyph"]
        self._drawCurvature()

    def _drawCurvature(self):
        self.curvatureVisualizerLayer.clearSublayers()

        showPreview = self.controller.w.getItem("preview").get()
        if not showPreview:
            return

        curvatureCombSteps = self.controller.w.getItem("steps").get()
        curvatureCombScale = self.controller.w.getItem("scale").get()
        # curvatureCombScale *= self.glyph.font.info.unitsPerEm / 1000
        curvatureCombColor = self.controller.w.getItem("colorButton").get()

        lines, shapes = self.glyph.getRepresentation(
                f"{DEFAULT_KEY}.preview",
                steps=int(curvatureCombSteps),
                scale=curvatureCombScale
            )

        visualizer = SegmentCurvatureVisualizer_Merz(self.curvatureVisualizerLayer)
        visualizer.curvatureCombColor = curvatureCombColor
        visualizer.curvatureCombStrokeWidth  = 1
        visualizer.curvatureCombStrokeWidth2 = 2

        for ci, contour in enumerate(self.glyph.contours):
            for si, segment in enumerate(contour.segments):
                if not si < len(lines[ci]):
                    continue
                if not si < len(shapes[ci]):
                    continue
                segmentLines  = lines[ci][si]
                segmentShapes = shapes[ci][si]
                visualizer._drawCurvatureComb(segmentLines, segmentShapes)


curvatureVisualizerEvent = f"{DEFAULT_KEY}.changed"

if curvatureVisualizerEvent not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=curvatureVisualizerEvent,
        methodName="curvatureVisualizerDidChange",
        lowLevelEventNames=[curvatureVisualizerEvent],
        documentation="Send when the links window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )



if __name__ == '__main__':

    CurvatureVisualizerController()
