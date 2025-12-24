import ezui
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont
from mojo.subscriber import Subscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.events import postEvent
from xTools4.modules.linkPoints2 import getDistance
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


tempEditModeKey = 'com.xTools4.tempEdit.mode'


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
    key     = 'com.xTools4.varGlyphViewer'
    width   = 123
    margins = 10

    glyph       = None
    defaultPath = None
    defaultFont = None

    content = """
    ( get default… )  @getDefaultButton
    ( reload ↺ )      @reloadDefaultButton

    # * ColorWell       @color

    [X] show equal    @showEqual
    [X] show deltas   @showDeltas
    [X] show values   @showValues
    [ ] show default  @showDefault
    [ ] selection     @selectionOnly

    ((( – | + )))     @addSubtractButton

    [X] display       @preview
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
            color=(0.9860473871231079, 0.008333318866789341, 0.5019234418869019, 1.0),
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

    @property
    def defaultGlyph(self):

        if self.glyph is None or self.defaultFont is None:
            return

        currentFont = self.glyph.font
        if not currentFont:
            return

        isTempFont = currentFont.lib.get(tempEditModeKey) == 'glyphs'

        if isTempFont:
            defaultGlyphName = self.glyph.name[:self.glyph.name.rfind('.')]
        else:
            defaultGlyphName = self.glyph.name

        if defaultGlyphName not in self.defaultFont:
            return

        return self.defaultFont[defaultGlyphName]

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

    def showValuesCallback(self, sender):
        self.settingsChangedCallback(None)

    def showDefaultCallback(self, sender):
        self.settingsChangedCallback(None)

    def previewCallback(self, sender):
        postEvent(f"{self.key}.changed")

    def settingsChangedCallback(self, sender):
        postEvent(f"{self.key}.changed")

    def addSubtractButtonCallback(self, sender):
        mode = ['subtract', 'add'][sender.get()]
        if self.glyph is None or self.defaultGlyph is None:
            return
        if mode == 'subtract':
            self.glyph.prepareUndo('subtract default glyph')
            diffGlyph = self.glyph - self.defaultGlyph
        else:
            self.glyph.prepareUndo('add default glyph')
            diffGlyph = self.glyph + self.defaultGlyph
        self.glyph.clearContours()
        self.glyph.clearAnchors()
        self.glyph.appendGlyph(diffGlyph)
        self.glyph.performUndo()


class VarGlyphViewerSubscriberGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=f"{self.controller.key}.foreground",
            location="foreground",
        )
        self.displayLayer = container.appendBaseSublayer()

    def destroy(self):
        self.displayLayer.clearSublayers()

    def glyphEditorDidSetGlyph(self, info):
        self.controller.glyph = info["glyph"]
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

        # if self.controller.glyph.name not in self.controller.defaultFont:
        #     return

        defaultGlyph  = self.controller.defaultGlyph

        if not defaultGlyph:
            return

        selectionOnly = self.controller.w.getItem('selectionOnly').get()
        showEqual     = self.controller.w.getItem('showEqual').get()
        showDeltas    = self.controller.w.getItem('showDeltas').get()
        showValues    = self.controller.w.getItem('showValues').get()
        showDefault   = self.controller.w.getItem('showDefault').get()
        preview       = self.controller.w.getItem("preview").get()

        color1 = (0, 0.85, 0, 1)
        color2 = (1, 0.5, 0, 1)

        if not preview:
            return

        if showDefault:
            defaultLayer = self.displayLayer.appendPathSublayer(
                fillColor=None,
                strokeColor=(0.5, 0.5, 0.5, 1),
                strokeWidth=2,
                opacity=0.2,
            )
            glyphPath = defaultGlyph.getRepresentation("merz.CGPath")
            defaultLayer.setPath(glyphPath)

        dash = 2, 2
        dotSize = 4

        selectedPoints = getImplicitSelectedPoints(self.controller.glyph)

        with self.displayLayer.sublayerGroup():
            
            # draw points
            for ci, c in enumerate(self.controller.glyph):
                for pi, p in enumerate(c.points):
                    if selectionOnly and p not in selectedPoints:
                        continue
                    p2 = defaultGlyph.contours[ci].points[pi]

                    isOrthogonal = p.x == p2.x or  p.y == p2.y
                    isEqual      = p.x == p2.x and p.y == p2.y
                    color = colorCheckTrue if isOrthogonal else colorCheckFalse

                    if isEqual:
                        if showEqual:
                            pointEqual = self.displayLayer.appendSymbolSublayer(
                                position=(p2.x, p2.y),
                            )
                            pointEqual.setImageSettings(
                                dict(
                                    name="oval",
                                    size=(dotSize*4, dotSize*4),
                                    strokeColor=colorCheckEqual,
                                    strokeWidth=2,
                                    fillColor=None,
                                )
                            )
                    else:
                        if showDeltas:
                            line = self.displayLayer.appendLineSublayer(
                                startPoint=(p.x, p.y),
                                endPoint=(p2.x, p2.y),
                                strokeWidth=1,
                                strokeColor=color,
                            )
                            ovalSymbol = dict(
                                name="oval",
                                size=(dotSize, dotSize),
                                fillColor=color,
                            )
                            line.setEndSymbol(ovalSymbol)

                            if showValues:
                                cx = p.x + (p2.x - p.x) * 0.5
                                cy = p.y + (p2.y - p.y) * 0.5
                                caption = ''
                                if p2.x != p.x:
                                    if not isOrthogonal:
                                        caption += 'x:'
                                    caption += f'{p.x - p2.x} '
                                if p2.y != p.y:
                                    if not isOrthogonal:
                                        caption += 'y:'
                                    caption += f'{p.y - p2.y}'

                                self.displayLayer.appendTextLineSublayer(
                                    position=(cx, cy),
                                    backgroundColor=color,
                                    text=caption,
                                    font="system",
                                    weight="bold",
                                    pointSize=9,
                                    padding=(4, 0),
                                    cornerRadius=4,
                                    fillColor=(1, 1, 1, 1),
                                    horizontalAlignment='center',
                                    verticalAlignment='center',
                                )


            # draw anchors
            for ai, a in enumerate(self.controller.glyph.anchors):
                if selectionOnly and not a.selected:
                    continue
                a2 = defaultGlyph.anchors[ai]

                isOrthogonal = a.x == a2.x or  a.y == a2.y
                isEqual      = a.x == a2.x and a.y == a2.y
                color = colorCheckTrue if isOrthogonal else colorCheckFalse

                if a.x == a2.x and a.y == a2.y:
                    if showEqual:
                        pointEqual = self.displayLayer.appendSymbolSublayer(
                            position=(a2.x, a2.y),
                        )
                        pointEqual.setImageSettings(
                            dict(
                                name="oval",
                                size=(dotSize*4, dotSize*4),
                                strokeColor=colorCheckEqual,
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
                        line = self.displayLayer.appendLineSublayer(
                            startPoint=(a.x, a.y),
                            endPoint=(a2.x, a2.y),
                            strokeWidth=1,
                            strokeColor=color,
                            strokeDash=dash,
                        )

                        if showValues:
                            cx = a.x + (a2.x - a.x) * 0.5
                            cy = a.y + (a2.y - a.y) * 0.5
                            caption = ''
                            if a2.x != a.x:
                                if not isOrthogonal:
                                    caption += 'x:'
                                caption += f'{a.x - a2.x} '
                            if a2.y != a.y:
                                if not isOrthogonal:
                                    caption += 'y:'
                                caption += f'{a.y - a2.y}'

                            self.displayLayer.appendTextLineSublayer(
                                position=(cx, cy),
                                backgroundColor=color,
                                text=caption,
                                font="system",
                                weight="bold",
                                pointSize=9,
                                padding=(4, 0),
                                cornerRadius=4,
                                fillColor=(1, 1, 1, 1),
                                horizontalAlignment='center',
                                verticalAlignment='center',
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
