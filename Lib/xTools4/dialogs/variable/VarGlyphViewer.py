import ezui
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont
from mojo.subscriber import Subscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.events import postEvent


def getImplicitSelectedPoints(glyph):
    '''
    http://forum.robofont.com/topic/742/easier-way-of-getting-all-selected-contour-points

    '''
    pts = []
    for contour in glyph.contours:
        for i, segment in enumerate(contour.segments):
            for pt in segment:
                if not pt.selected:
                    continue
                pts.append(pt)
                # implicit == include BCPs in selection
                if pt.type != 'offcurve':
                    # bcpIn
                    if len(segment) == 3:
                        bcpIn = segment[-2]
                        pts.append(bcpIn)
                    # bcpOut
                    nextSegment = contour[(i + 1) % len(contour.segments)]
                    if len(nextSegment) == 3:
                        bcpOut = nextSegment[0]
                        pts.append(bcpOut)
    return pts


class VarGlyphViewer(ezui.WindowController):

    title   = 'varglyph'
    key     = 'com.fontBureau.varGlyphViewer'
    width   = 123
    margins = 10

    defaultPath = None
    defaultFont = None

    content = """
    ( get default… )  @getDefaultButton
    ( reload ↺ )      @reloadDefaultButton

    * ColorWell       @color

    [X] show equal    @showEqual
    [X] show deltas   @showDeltas
    [ ] show default  @showDefault
    [ ] selection     @selectionOnly

    ((( – | + )))     @addSubtractButton
    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        getDefaultButton=dict(
            width='fill',
        ),
        reloadDefaultButton=dict(
            width='fill',
        ),
        color=dict(
            color=(0, 0.5, 1, 0.85),
            callback='settingsChangedCallback',
        ),
        addSubtractButton=dict(
            sizeStyle="regular",
            width='fill',
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
        VarGlyphViewerSubscriberGlyphEditor.controller = self
        registerGlyphEditorSubscriber(VarGlyphViewerSubscriberGlyphEditor)
        self.settingsChangedCallback(None)

    def destroy(self):
        unregisterGlyphEditorSubscriber(VarGlyphViewerSubscriberGlyphEditor)
        VarGlyphViewerSubscriberGlyphEditor.controller = None

    # callbacks

    def getDefaultButtonCallback(self, sender):
        self.defaultPath = GetFile(message='Get default source…', title=self.title)
        self.defaultFont = OpenFont(self.defaultPath, showInterface=False)
        self.settingsChangedCallback(None)

    def reloadButtonCallback(self, sender):
        if self.defaultFont is None:
            return
        self.defaultFont = OpenFont(self.defaultPath, showInterface=False)
        self.settingsChangedCallback(None)

    def selectionOnlyCallback(self, sender):
        self.settingsChangedCallback(None)

    def showEqualCallback(self, sender):
        self.settingsChangedCallback(None)

    def showDeltasCallback(self, sender):
        self.settingsChangedCallback(None)

    def showDefaultCallback(self, sender):
        self.settingsChangedCallback(None)

    def settingsChangedCallback(self, sender):
        postEvent(f"{self.key}.changed")

    def addSubtractButtonCallback(self, sender):
        mode = ['subtract', 'add'][sender.get()]
        print(f'{mode} the default')


class VarGlyphViewerSubscriberGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=f"{self.controller.key}.background",
            location="background",
        )
        self.displayLayer = container.appendBaseSublayer()

    def destroy(self):
        self.displayLayer.clearSublayers()

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self._drawVarGlyphViewer()

    def glyphEditorGlyphDidChange(self, info):
        self._drawVarGlyphViewer()

    def glyphDidChangeSelection(self, info):
        self._drawVarGlyphViewer()

    def varGlyphViewerDidChange(self, info):
        self._drawVarGlyphViewer()

    def _drawVarGlyphViewer(self):
        self.displayLayer.clearSublayers()

        if self.controller.defaultFont is None:
            return

        if self.glyph.name not in self.controller.defaultFont:
            return

        defaultGlyph  = self.controller.defaultFont[self.glyph.name]
        selectionOnly = self.controller.w.getItem('selectionOnly').get()
        showEqual     = self.controller.w.getItem('showEqual').get()
        showDeltas    = self.controller.w.getItem('showDeltas').get()
        showDefault   = self.controller.w.getItem('showDefault').get()
        color         = self.controller.w.getItem('color').get()

        if showDefault:
            defaultLayer = self.displayLayer.appendPathSublayer(
                fillColor=color,
                strokeColor=None,
                opacity=0.2,
            )
            glyphPath = defaultGlyph.getRepresentation("merz.CGPath")
            defaultLayer.setPath(glyphPath)

        dash = 2, 2
        dotSize = 4

        selectedPoints = getImplicitSelectedPoints(self.glyph)

        with self.displayLayer.sublayerGroup():
            
            # draw points
            for ci, c in enumerate(self.glyph):
                for pi, p in enumerate(c.points):
                    if selectionOnly and p not in selectedPoints:
                        continue
                    p2 = defaultGlyph.contours[ci].points[pi]
                    if p.x == p2.x and p.y == p2.y:
                        if showEqual:
                            pointEqual = self.displayLayer.appendSymbolSublayer(
                                position=(p2.x, p2.y),
                            )
                            pointEqual.setImageSettings(
                                dict(
                                    name="oval",
                                    size=(dotSize*4, dotSize*4),
                                    strokeColor=color,
                                    strokeWidth=2,
                                    fillColor=None,
                                )
                            )
                    else:
                        if showDeltas:
                            pointDelta = self.displayLayer.appendSymbolSublayer(
                                position=(p2.x, p2.y),
                            )
                            pointDelta.setImageSettings(
                                dict(
                                    name="oval",
                                    size=(dotSize, dotSize),
                                    strokeWidth=None,
                                    fillColor=color,
                                )
                            )
                            line = self.displayLayer.appendLineSublayer(
                                startPoint=(p.x, p.y),
                                endPoint=(p2.x, p2.y),
                                strokeWidth=1,
                                strokeColor=color,
                                strokeDash=dash if p.type == 'offcurve' else None,
                            )

            # draw anchors
            for ai, a in enumerate(self.glyph.anchors):
                if selectionOnly and not a.selected:
                    continue
                a2 = defaultGlyph.anchors[ai]
                if a.x == a2.x and a.y == a2.y:
                    if showEqual:
                        pointEqual = self.displayLayer.appendSymbolSublayer(
                            position=(a2.x, a2.y),
                        )
                        pointEqual.setImageSettings(
                            dict(
                                name="oval",
                                size=(dotSize*4, dotSize*4),
                                strokeColor=color,
                                strokeWidth=2,
                                fillColor=None,
                            )
                        )
                else:
                    if showDeltas:
                        pointDelta = self.displayLayer.appendSymbolSublayer(
                            position=(a2.x, a2.y),
                        )
                        pointDelta.setImageSettings(
                            dict(
                                name="oval",
                                size=(dotSize, dotSize),
                                strokeWidth=None,
                                fillColor=color,
                            )
                        )
                        lineDash = (2, 2)
                        line = self.displayLayer.appendLineSublayer(
                            startPoint=(a.x, a.y),
                            endPoint=(a2.x, a2.y),
                            strokeWidth=1,
                            strokeColor=color,
                            strokeDash=lineDash,
                        )


eventName = f"{VarGlyphViewer.key}.changed"

if eventName not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=eventName,
        methodName="varGlyphViewerDidChange",
        lowLevelEventNames=[eventName],
        documentation="Send when the VarGlyphViewer window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(VarGlyphViewer)
