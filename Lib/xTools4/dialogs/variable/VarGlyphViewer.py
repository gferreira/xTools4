import ezui
from math import atan, degrees
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont
from mojo.subscriber import Subscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.events import postEvent
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


KEY = 'com.xTools4.dialogs.variable.varGlyphViewer'


tempEditModeKey = 'com.xTools4.tempEdit.mode'

colorCheckTrueBG  = 0.7, 1.0, 0.7, 0.85
colorCheckFalseBG = 1.0, 0.7, 0.7, 0.85


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

def getAngle(p1, p2):
    a = p2.x - p1.x
    b = p2.y - p1.y
    if a != 0:
        angleRadians = atan(float(b) / a)
        angleDegrees = degrees(angleRadians)
    else:
        angleDegrees = 0
    return angleDegrees


class VarGlyphViewer(ezui.WindowController):

    title   = 'varglyph'
    key     = KEY
    width   = 123
    margins = 10

    glyph       = None
    defaultPath = None
    designspacePath = None
    defaultFont     = None

    content = """
    ( get default… )  @getDefaultButton
    ( reload ↺ )      @reloadDefaultButton

    [X] show default    @showDefault
    [X] show distance   @showValues
    [ ] selection only  @selectionOnly

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
        self.w.workspaceWindowIdentifier = KEY
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

    # def showEqualCallback(self, sender):
    #     self.settingsChangedCallback(None)

    # def showDeltasCallback(self, sender):
    #     self.settingsChangedCallback(None)

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
        showEqual     = True
        showDeltas    = True
        showValues    = self.controller.w.getItem('showValues').get()
        showDefault   = self.controller.w.getItem('showDefault').get()
        preview       = self.controller.w.getItem("preview").get()

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

        italicAngle = self.controller.glyph.font.info.italicAngle

        if italicAngle:
            g1_ = defaultGlyph.copy()
            g1_.skewBy((italicAngle, 0))
            g1_.round()
            g2_ = self.controller.glyph.copy()
            g2_.skewBy((italicAngle, 0))
            g2_.round()

        with self.displayLayer.sublayerGroup():

            #-------------
            # draw points
            #-------------

            for ci, c in enumerate(self.controller.glyph):
                for pi, p in enumerate(c.points):
                    p2 = defaultGlyph.contours[ci].points[pi]
                    isEqual = p2.x == p.x and p2.y == p.y

                    if italicAngle:
                        p1_ = g1_.contours[ci].points[pi]
                        p2_ = g2_.contours[ci].points[pi]
                        isOrthogonal = p2_.x == p1_.x or p2_.y == p1_.y
                    else:
                        isOrthogonal = p2.x == p.x or p2.y == p.y

                    color   = colorCheckTrue   if isOrthogonal else colorCheckFalse
                    colorBG = colorCheckTrueBG if isOrthogonal else colorCheckFalseBG

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
                                strokeDash=dash,
                            )
                            ovalSymbol = dict(
                                name="oval",
                                size=(dotSize, dotSize),
                                fillColor=color,
                            )
                            line.setEndSymbol(ovalSymbol)

                            if showValues:
                                if selectionOnly and p not in selectedPoints:
                                    continue

                                cx = p.x + (p2.x - p.x) * 0.5
                                cy = p.y + (p2.y - p.y) * 0.5

                                if italicAngle:
                                    deltaX = p2_.x - p1_.x
                                    deltaY = p2_.y - p1_.y
                                else:
                                    deltaX = p2.x - p.x
                                    deltaY = p2.y - p.y

                                caption = ''

                                if deltaX:
                                    caption += f'{int(deltaX)} '
                                if deltaY:
                                    caption += f'{int(deltaY)}'

                                self.displayLayer.appendTextLineSublayer(
                                    position=(cx, cy),
                                    backgroundColor=colorBG,
                                    text=caption,
                                    font="system",
                                    weight="bold",
                                    pointSize=9,
                                    padding=(4, 0),
                                    cornerRadius=4,
                                    fillColor=color,
                                    horizontalAlignment='center',
                                    verticalAlignment='center',
                                )

            #--------------
            # draw anchors
            #--------------

            for ai, a in enumerate(self.controller.glyph.anchors):
                if selectionOnly and not a.selected:
                    continue

                a2 = defaultGlyph.anchors[ai]
                isEqual = a.x == a2.x and a.y == a2.y

                if italicAngle:
                    a1_ = g1_.anchors[ai]
                    a2_ = g2_.anchors[ai]
                    isOrthogonal = a2_.x == a1_.x or a2_.y == a1_.y
                else:
                    isOrthogonal = a2.x == a.x or a2.y == a.y

                color = colorCheckTrue if isOrthogonal else colorCheckFalse
                colorBG = colorCheckTrueBG if isOrthogonal else colorCheckFalseBG

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

                            if italicAngle:
                                deltaX = a2_.x - a1_.x
                                deltaY = a2_.y - a1_.y
                            else:
                                deltaX = a2.x - a.x
                                deltaY = a2.y - a.y

                            caption = ''

                            if deltaX:
                                caption += f'{int(deltaX)} '
                            if deltaY:
                                caption += f'{int(deltaY)}'

                            self.displayLayer.appendTextLineSublayer(
                                position=(cx, cy),
                                backgroundColor=colorBG,
                                text=caption,
                                font="system",
                                weight="bold",
                                pointSize=9,
                                padding=(4, 0),
                                cornerRadius=4,
                                fillColor=color,
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
