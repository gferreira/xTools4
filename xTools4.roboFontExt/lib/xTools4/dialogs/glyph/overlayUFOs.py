import ezui
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.roboFont import OpenWindow, OpenFont, CurrentFont, CurrentGlyph
from mojo.events import postEvent
from xTools4.dialogs.old import hDialog


KEY = f'{hDialog.key}.glyph.overlayUFOs'


class OverlayUFOsController(ezui.WindowController):

    title       = 'overlay UFOs'
    width       = 123*3 
    margins     = 10

    rowHeight   = 17
    lineHeight  = 20
    
    content = """
    = HorizontalStack

    = VerticalStack @panel
    > * ColorWell   @color
    > [X] stroke    @strokeDraw
    > [ ] fill      @fillDraw
    > [X] points    @pointsDraw
    > [ ] anchors   @anchorsDraw

    > alignment
    > (X) left      @alignment
    > ( ) center
    > ( ) right
    
    = VerticalStack @main
    > |-fonts----|  @ufos
    # > (update ↺)  @updateButton
    
    """
    
    descriptionData = dict(
        ufos=dict(
            items=[],
            acceptedDropFileTypes=[".ufo"],
            columnDescriptions=[
                dict(
                    identifier="path",
                    title="path",
                    cellDescription=dict(
                        cellClassArguments=dict(
                            showFullPath=False
                        )
                    )
                ),
            ],
        ),
        color=dict(
            color=(1, 0.5, 0, 1),
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
            sizeStyle='small',
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem('ufos').getNSTableView().setRowHeight_(self.rowHeight)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    def started(self):
        OverlayUFOsGlyphEditor.controller = self
        registerGlyphEditorSubscriber(OverlayUFOsGlyphEditor)
        self.settingsChangedCallback(None)

    def destroy(self):
        unregisterGlyphEditorSubscriber(OverlayUFOsGlyphEditor)
        OverlayUFOsGlyphEditor.controller = None

    # callbacks

    def ufosSelectionCallback(self, sender):
        self.settingsChangedCallback(None)

    def colorCallback(self, sender):
        self.settingsChangedCallback(None)

    def strokeDrawCallback(self, sender):
        self.settingsChangedCallback(None)

    def fillDrawCallback(self, sender):
        self.settingsChangedCallback(None)

    def pointsDrawCallback(self, sender):
        self.settingsChangedCallback(None)

    def anchorsDrawCallback(self, sender):
        self.settingsChangedCallback(None)

    def alignmentCallback(self, sender):
        self.settingsChangedCallback(None)

    def ufosCreateItemsForDroppedPathsCallback(self, sender, paths):
        fonts = [OpenFont(path, showInterface=False) for path in paths]
        return fonts

    # callbacks

    def settingsChangedCallback(self, sender):
        postEvent(f"{KEY}.changed")


class OverlayUFOsGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="background",
        )
        self.overlayFontsLayer = container.appendBaseSublayer()

        self.glyph = CurrentGlyph()
        self._drawUFOs()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="background",
        )
        container.clearSublayers()

    def overlayUFOsDidChange(self, info):
        self.glyph = self.getGlyphEditor().getGlyph().asFontParts()
        self._drawUFOs()

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self._drawUFOs()

    def _drawUFOs(self):

        self.overlayFontsLayer.clearSublayers()

        strokeDraw  = self.controller.w.getItem('strokeDraw').get()
        fillDraw    = self.controller.w.getItem('fillDraw').get()
        pointsDraw  = self.controller.w.getItem('pointsDraw').get()
        anchorsDraw = self.controller.w.getItem('anchorsDraw').get()
        alignment   = self.controller.w.getItem('alignment').get()

        UFOs  = self.controller.w.getItem('ufos').getSelectedItems()
        color = self.controller.w.getItem('color').get()

        pointsSize = 5

        fillOpacity = 0.5 / (len(UFOs) + 1)

        for ufo in UFOs:
            if self.glyph.name not in ufo:
                continue
            ufoGlyph = ufo[self.glyph.name]

            colorFill   = color if fillDraw else None
            colorStroke = color if strokeDraw else None
            colorPoints = color if pointsDraw else None

            glyphFillLayer = self.overlayFontsLayer.appendPathSublayer(
                fillColor=colorFill,
                opacity=fillOpacity,
                strokeColor=None,
            )
            glyphPath = ufoGlyph.getRepresentation("merz.CGPath")
            glyphFillLayer.setPath(glyphPath)

            glyphStrokeLayer = self.overlayFontsLayer.appendPathSublayer(
                fillColor=None,
                strokeColor=colorStroke,
                strokeWidth=1,
            )
            glyphPath = ufoGlyph.getRepresentation("merz.CGPath")
            glyphStrokeLayer.setPath(glyphPath)

            if alignment == 1:
                deltaX = -(ufoGlyph.width - self.glyph.width) * 0.5
            elif alignment == 2:
                deltaX = -(ufoGlyph.width - self.glyph.width)
            else:
                deltaX = 0

            glyphFillLayer.addTranslationTransformation((deltaX, 0), name='translate')
            glyphStrokeLayer.addTranslationTransformation((deltaX, 0), name='translate')

            if pointsDraw:
                with self.overlayFontsLayer.sublayerGroup():
                    for c in ufoGlyph:
                        for pt in c.points:
                            symbol = self.overlayFontsLayer.appendSymbolSublayer(
                                position=(pt.x + deltaX, pt.y),
                            )
                            symbol.setImageSettings(
                                dict(
                                    name="oval",
                                    size=(pointsSize, pointsSize),
                                    strokeWidth=None,
                                    fillColor=colorPoints,
                                )
                            )

            if anchorsDraw:
                with self.overlayFontsLayer.sublayerGroup():
                    for a in ufoGlyph.anchors:
                        symbol = self.overlayFontsLayer.appendSymbolSublayer(
                            position=(a.x + deltaX, a.y),
                        )
                        symbol.setImageSettings(
                            dict(
                                name="oval",
                                size=(pointsSize, pointsSize),
                                strokeWidth=None,
                                fillColor=colorPoints,
                            )
                        )


eventName = f"{KEY}.changed"

if eventName not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        eventName,
        methodName="overlayUFOsDidChange",
        lowLevelEventNames=[eventName],
        documentation="Send when the OverlayUFOs window changes its settings.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(OverlayUFOsController)

