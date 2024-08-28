import ezui
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, unregisterGlyphEditorSubscriber
from mojo.roboFont import OpenWindow, CurrentGlyph
from mojo.events import postEvent
from hTools3.modules.measureHandles import MeasureHandlesMaker, MeasureSegmentsMaker


DEFAULT_KEY = 'com.hipertipo.hTools4.dialogs.glyphs.measureHandles'


def measureHandlesFactory(glyph):

    glyph = glyph.asFontParts().copy()
    glyph.clearComponents()

    M = MeasureHandlesMaker()
    M.build(glyph)

    return M.positions, M.lengths, M.angles

def measureSegmentsFactory(glyph):

    glyph = glyph.asFontParts().copy()
    glyph.clearComponents()

    M = MeasureSegmentsMaker()
    M.build(glyph)

    return M.positions, M.lengths, M.angles


class MeasureHandlesController(ezui.WindowController):

    title   = 'measure'
    width   = 123
    margins = 10

    def build(self):
        content = """
        (X) length         @captionMode
        ( ) angle

        [X] handles        @handlesShow
        * ColorWell        @handlesColor

        [X] line segments  @linesShow
        * ColorWell        @linesColor

        caption size
        --X-----           @captionSize

        [X] show preview   @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            captionMode=dict(
                callback='settingsChangedCallback',
            ),
            handlesShow=dict(
                callback='settingsChangedCallback',
            ),
            handlesColor=dict(
                callback='settingsChangedCallback',
                color=(1, 0, 0.5, 1),
            ),
            linesShow=dict(
                callback='settingsChangedCallback',
            ),
            linesColor=dict(
                callback='settingsChangedCallback',
                color=(0, 0.5, 1, 1),
            ),
           captionSize=dict(
                callback='settingsChangedCallback',
                minValue=9,
                maxValue=13,
                value=11,
                tickMarks=5,
                stopOnTickMarks=True,
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
        registerRepresentationFactory(Glyph, f"{DEFAULT_KEY}.handles", measureHandlesFactory)
        registerRepresentationFactory(Glyph, f"{DEFAULT_KEY}.segments", measureSegmentsFactory)
        MeasureHandles.controller = self
        registerGlyphEditorSubscriber(MeasureHandles)

    def destroy(self):
        unregisterRepresentationFactory(Glyph, f"{DEFAULT_KEY}.handles")
        unregisterRepresentationFactory(Glyph, f"{DEFAULT_KEY}.segments")
        unregisterGlyphEditorSubscriber(MeasureHandles)
        MeasureHandles.controller = None

    def settingsChangedCallback(self, sender):
        postEvent(f"{DEFAULT_KEY}.changed")


class MeasureHandles(Subscriber):
    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=DEFAULT_KEY,
            location="foreground",
        )
        self.measureHandlesLayer = container.appendBaseSublayer()
        self.glyph = CurrentGlyph()
        self._drawMeasureHandles()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(DEFAULT_KEY)
        container.clearSublayers()

    def measureHandlesDidChange(self, info):
        self._drawMeasureHandles()

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self._drawMeasureHandles()

    def glyphEditorGlyphDidChangeOutline(self, info):
        self.glyph = info["glyph"]
        self._drawMeasureHandles()

    def _drawMeasureHandles(self):
        self.measureHandlesLayer.clearSublayers()

        showPreview = self.controller.w.getItem("preview").get()
        if not showPreview:
            return

        captionMode  = self.controller.w.getItem("captionMode").get()
        captionSize  = self.controller.w.getItem("captionSize").get()
        showHandles  = self.controller.w.getItem("handlesShow").get()
        showLines    = self.controller.w.getItem("linesShow").get()
        handlesColor = self.controller.w.getItem("handlesColor").get() 
        linesColor   = self.controller.w.getItem("linesColor").get() 
        ignoreZero   = False # does not work otherwise 

        if showHandles:
            measurements = self.glyph.getRepresentation(f"{DEFAULT_KEY}.handles")
            if measurements:
                positions, lengths, angles = measurements
                captions = lengths if captionMode == 0 else angles
                for i, pos in enumerate(positions):
                    for j, (x, y) in enumerate(pos):
                        caption  = captions[i][j]
                        if ignoreZero and int(float(caption)) == 0:
                            continue
                        self.measureHandlesLayer.appendTextLineSublayer(
                            position=(x, y),
                            text=caption,
                            font="system",
                            weight="bold",
                            pointSize=captionSize,
                            fillColor=handlesColor,
                            horizontalAlignment='center',
                            verticalAlignment='center',
                        )

        if showLines:
            measurements = self.glyph.getRepresentation(f"{DEFAULT_KEY}.segments")
            if measurements:
                positions, lengths, angles = measurements
                captions = lengths if captionMode == 0 else angles
                for i, pos in enumerate(positions):
                    for j, (x, y) in enumerate(pos):
                        caption  = captions[i][j]
                        if ignoreZero and int(float(caption)) == 0:
                            continue
                        self.measureHandlesLayer.appendTextLineSublayer(
                            position=(x, y),
                            text=caption,
                            font="system",
                            weight="bold",
                            pointSize=captionSize,
                            fillColor=linesColor,
                            horizontalAlignment='center',
                            verticalAlignment='center',
                        )


measureHandlesEvent = f"{DEFAULT_KEY}.changed"

if measureHandlesEvent not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=measureHandlesEvent,
        methodName="measureHandlesDidChange",
        lowLevelEventNames=[measureHandlesEvent],
        documentation="Send when the measure handles window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(MeasureHandlesController)
