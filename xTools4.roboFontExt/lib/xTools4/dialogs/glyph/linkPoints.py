import ezui
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, unregisterGlyphEditorSubscriber
from mojo.roboFont import OpenWindow, CurrentGlyph
from mojo.events import postEvent
from xTools4.modules.linkPoints import *
from xTools4.modules.measureHandles import getVector


KEY = '{hDialog.key}.glyph.linkPoints'


class LinkPointsController(ezui.WindowController):

    title   = "links"
    width   = 123
    margins = 10

    def build(self):
        content = """
        (X) length        @captionMode
        ( ) angle

        (link)            @linkButton
        (unlink)          @unlinkButton

        * ColorWell       @colorButton

        caption size
        --X-----          @captionSize

        [ ] projections   @projections

        (clear all)       @clearButton

        [X] show preview  @preview
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            captionMode=dict(
                callback='settingsChangedCallback',
            ),
            linkButton=dict(
                width="fill",
            ),
            unlinkButton=dict(
                width="fill",
            ),
            colorButton=dict(
                callback='settingsChangedCallback',
                color=(1, 0.2, 0, 0.8),
            ),
            captionSize=dict(
                callback='settingsChangedCallback',
                minValue=9,
                maxValue=13,
                value=11,
                tickMarks=5,
                stopOnTickMarks=True,
            ),
            projections=dict(
                callback='settingsChangedCallback',
            ),
            clearButton=dict(
                width="fill",
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
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    def started(self):
        LinkPoints.controller = self
        registerGlyphEditorSubscriber(LinkPoints)

    def destroy(self):
        unregisterGlyphEditorSubscriber(LinkPoints)
        LinkPoints.controller = None

    # callbacks

    def linkButtonCallback(self, sender):
        glyph = CurrentGlyph()
        if not glyph:
            return
        linkPoints(glyph, key=KEY)
        postEvent(f"{KEY}.changed")

    def unlinkButtonCallback(self, sender):
        glyph = CurrentGlyph()
        if not glyph:
            return
        deleteSelectedLinks(glyph, key=KEY)
        postEvent(f"{KEY}.changed")

    def clearButtonCallback(self, sender):
        glyph = CurrentGlyph()
        if not glyph:
            return
        deleteAllLinks(glyph, key=KEY)
        postEvent(f"{KEY}.changed")

    def settingsChangedCallback(self, sender):
        captionMode = self.w.getItem("captionMode").get()
        self.w.getItem("projections").enable(not captionMode)
        postEvent(f"{KEY}.changed")


class LinkPoints(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="foreground",
        )
        self.linksLayer = container.appendBaseSublayer()
        self.glyph = CurrentGlyph()
        self._drawLinks()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(KEY)
        container.clearSublayers()

    def linksDidChange(self, info):
        self.glyph = self.getGlyphEditor().getGlyph().asFontParts()
        self._drawLinks()

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self._drawLinks()

    def glyphEditorGlyphDidChangeOutline(self, info):
        self.glyph = info["glyph"]
        self._drawLinks()

    def _drawLinks(self):
        self.linksLayer.clearSublayers()

        showPreview = self.controller.w.getItem("preview").get()
        if not showPreview:
            return

        links = getLinks(self.glyph, key=KEY)

        linkColor   = self.controller.w.getItem("colorButton").get()
        captionMode = self.controller.w.getItem("captionMode").get()
        captionSize = self.controller.w.getItem("captionSize").get()
        projections = self.controller.w.getItem("projections").get()

        def _drawMeasurement(p1, p2, captionMode):
            # draw line
            self.linksLayer.appendLineSublayer(
                startPoint=p1,
                endPoint=p2,
                strokeColor=linkColor,
                strokeWidth=3,
                strokeCap='round',
            )
            # draw caption
            distance, angle = getVector((p1[0], p1[1]), (p2[0], p2[1]))
            value = angle if captionMode else distance
            txt = f'{int(value)}' if (projections and not captionMode) else f'{value:.2f}'
            if captionMode:
                txt += '°'
            x = p1[0] + (p2[0] - p1[0]) * 0.5
            y = p1[1] + (p2[1] - p1[1]) * 0.5
            self.linksLayer.appendTextLineSublayer(
                position=(x, y),
                backgroundColor=linkColor,
                text=txt,
                font="system",
                weight="bold",
                pointSize=captionSize,
                padding=(4, 0),
                cornerRadius=4,
                fillColor=(1, 1, 1, 1),
                horizontalAlignment='center',
                verticalAlignment='center',
            )

        with self.linksLayer.sublayerGroup():
            for ID1, ID2 in links:
                pt1 = getPoint(self.glyph, ID1)
                pt2 = getPoint(self.glyph, ID2)
                if captionMode == 0 and projections:
                    _drawMeasurement((pt1.x, pt1.y), (pt2.x, pt1.y), captionMode)
                    _drawMeasurement((pt2.x, pt1.y), (pt2.x, pt2.y), captionMode)
                else:
                    _drawMeasurement((pt1.x, pt1.y), (pt2.x, pt2.y), captionMode)


linkPointsEvent = f"{KEY}.changed"

if linkPointsEvent not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=linkPointsEvent,
        methodName="linksDidChange",
        lowLevelEventNames=[linkPointsEvent],
        documentation="Send when the links window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(LinkPointsController)
