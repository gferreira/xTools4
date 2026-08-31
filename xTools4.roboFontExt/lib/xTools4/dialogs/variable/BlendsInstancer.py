import os
import ezui
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from mojo.UI import GetFile
from mojo.roboFont import CurrentFont, RGlyph
from mojo.subscriber import Subscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerCurrentFontSubscriber, unregisterCurrentFontSubscriber
from mojo.events import postEvent
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.blendsPreview import getEffectiveLocation, instantiateGlyph
from xTools4.modules.glyphutils import getImplicitSelectedPoints
from xTools4.modules.fontutils import getGlyphs2
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


KEY = 'com.xTools4.dialogs.variable.blendsInstancer'


colorCheckTrueBG  = 0.7, 1.0, 0.7, 0.85
colorCheckFalseBG = 1.0, 0.7, 0.7, 0.85


def getStyleNameFromReferenceSourcePath(referenceSourcePath):
    fileName = os.path.splitext(os.path.split(referenceSourcePath)[-1])[0]
    styleName = ' '.join(fileName.split('_')[1:])
    return styleName

def blendedGlyphFactory(glyph, font, operator):

    if not (glyph and font and operator):
        return Glyph()

    styleName = getStyleNameFromReferenceSourcePath(font.path)

    # get blended location from style name
    blendedLocation = { p[:4] : int(p[4:]) for p in styleName.split(' ') }

    # get parametric location from blended location
    parametricLocation = getEffectiveLocation(operator.doc.path, blendedLocation)

    return instantiateGlyph(operator, glyph.name, parametricLocation)


class BlendsInstancerController(ezui.WindowController):

    title   = 'instancer'
    key     = KEY
    margins = 10
    verbose = True

    designspacePath = None
    font     = None
    glyph    = None
    operator = None

    content = """
    ( designspace…  )   @getDesignspaceButton
    ( reload ↺ )        @reloadButton

    [X] show deltas     @showDeltas
    [ ] show distance   @showValues
    [ ] selection only  @selectionOnly

    ( instantiate )     @instantiateButton
    (( ...))            @targetLayer

    [X] preview         @showPreview

    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        targetLayer=dict(
            width='fill',
        ),
        instantiateButton=dict(
            width='fill',
        ),
        getDesignspaceButton=dict(
            width='fill',
        ),
        reloadButton=dict(
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
            size=(123, 'auto')
        )
        self.w.workspaceWindowIdentifier = KEY
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    def started(self):
        registerRepresentationFactory(Glyph, f"{KEY}.preview", blendedGlyphFactory)

        BlendsInstancerSubscriberRoboFont.controller = self
        registerRoboFontSubscriber(BlendsInstancerSubscriberRoboFont)

        BlendsInstancerSubscriberCurrentFont.controller = self
        registerCurrentFontSubscriber(BlendsInstancerSubscriberCurrentFont)

        BlendsInstancerSubscriberGlyphEditor.controller = self
        registerGlyphEditorSubscriber(BlendsInstancerSubscriberGlyphEditor)

        self.showPreviewCallback(None)
        self.font = CurrentFont()
        self._updateFontLayers()

    def destroy(self):
        unregisterRepresentationFactory(Glyph, f"{KEY}.preview")

        unregisterRoboFontSubscriber(BlendsInstancerSubscriberRoboFont)
        BlendsInstancerSubscriberRoboFont.controller = None

        unregisterCurrentFontSubscriber(BlendsInstancerSubscriberCurrentFont)
        BlendsInstancerSubscriberCurrentFont.controller = None

        unregisterGlyphEditorSubscriber(BlendsInstancerSubscriberGlyphEditor)
        BlendsInstancerSubscriberGlyphEditor.controller = None

    def getDesignspaceButtonCallback(self, sender):
        designspacePath = GetFile(
            message='Select designspace file:',
            title=self.title, 
            allowsMultipleSelection=False,
            fileTypes=["designspace"]
        )
        if designspacePath is None:
            return
        self.designspacePath = designspacePath
        self._loadDesignspace()

    def reloadButtonCallback(self, sender):
        self._loadDesignspace()

    def showDeltasCallback(self, sender):
        self.settingsChangedCallback(None)

    def showValuesCallback(self, sender):
        self.settingsChangedCallback(None)

    def selectionOnlyCallback(self, sender):
        self.settingsChangedCallback(None)

    def showPreviewCallback(self, sender):
        self.settingsChangedCallback(None)

    def settingsChangedCallback(self, sender):
        postEvent(f"{self.key}.changed")

    def instantiateButtonCallback(self, sender):

        if not self.font:
            return

        if not self.operator:
            return

        glyphNames = getGlyphs2(self.font)

        targetLayer = self.w.getItem("targetLayer").getItem()

        styleName = getStyleNameFromReferenceSourcePath(self.font.path)

        if self.verbose:
            print(f'instantiating glyphs in {styleName}...\n')

        for glyphName in glyphNames:
            glyph = self.font[glyphName]

            if self.verbose:
                print(f'\tinstantiating {glyphName}...')

            instanceGlyph = glyph.getRepresentation(f"{KEY}.preview", font=self.font, operator=self.operator)
            if instanceGlyph is None:
                continue

            instanceGlyph = RGlyph(instanceGlyph)

            targetGlyph = glyph.getLayer(targetLayer)
            targetGlyph.prepareUndo('instantiate blended glyph')
            targetGlyph.clear()
            targetGlyph.appendGlyph(instanceGlyph)
            targetGlyph.width = instanceGlyph.width
            targetGlyph.performUndo()

        if self.verbose:
            print()
            print('...done.\n')

    def _loadDesignspace(self):
        if self.verbose:
            print(f'loading designspace from {os.path.split(self.designspacePath)[-1]}... ', end='')

        self.operator = UFOOperator()
        self.operator.read(self.designspacePath)
        self.operator.loadFonts()

        if self.verbose:
            print('done.\n')

    def _updateFontLayers(self):
        layerNames = list(self.font.layerOrder) if self.font else []
        self.w.getItem("targetLayer").setItems(layerNames)


class BlendsInstancerSubscriberRoboFont(Subscriber):

    controller = None

    def fontDocumentDidBecomeCurrent(self, info):
        self.controller.font = info['font']
        self.controller._updateFontLayers()

    def fontDocumentDidOpen(self, info):
        self.controller.font = info['font']
        self.controller._updateFontLayers()

    def fontDocumentDidClose(self, info):
        self.controller.font = None
        self.controller._updateFontLayers()

    def roboFontDidSwitchCurrentGlyph(self, info):
        glyph = info["glyph"]
        if self.controller.glyph is not None and glyph is not None:
            if glyph.name == self.controller.glyph.name:
                return
        self.controller.glyph = info["glyph"]


class BlendsInstancerSubscriberCurrentFont(Subscriber):

    controller = None

    def build(self):
        self.controller._updateFontLayers()

    def currentFontLayersDidChangeLayer(self, info):
        self.controller._updateFontLayers()


class BlendsInstancerSubscriberGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=f"{self.controller.key}.foreground",
            location="foreground",
        )
        self.displayLayer = container.appendBaseSublayer()

    def started(self):
        self._drawBlendsInstance()

    def destroy(self):
        self.displayLayer.clearSublayers()

    def glyphEditorDidSetGlyph(self, info):
        self.controller.glyph = info["glyph"]
        self._drawBlendsInstance()

    def glyphEditorGlyphDidChange(self, info):
        self._drawBlendsInstance()

    def glyphDidChangeSelection(self, info):
        self._drawBlendsInstance()

    def blendsInstancerDidChange(self, info):
        self._drawBlendsInstance()

    def _drawBlendsInstance(self):
        self.displayLayer.clearSublayers()

        preview = self.controller.w.getItem("showPreview").get()
        if not preview:
            return

        glyph = self.controller.glyph
        if glyph is None:
            return

        instanceGlyph = glyph.getRepresentation(f"{KEY}.preview", font=self.controller.font, operator=self.controller.operator)
        if not instanceGlyph:
            return

        instanceGlyphPath = instanceGlyph.getRepresentation("merz.CGPath")
        previewLayer = self.displayLayer.appendPathSublayer(
            fillColor=None,
            strokeColor=(0.5, 0.5, 0.5, 1),
            strokeWidth=2,
            opacity=0.2,
        )
        previewLayer.setPath(instanceGlyphPath)

        showDeltas    = self.controller.w.getItem('showDeltas').get()
        selectionOnly = self.controller.w.getItem('selectionOnly').get()
        showValues    = self.controller.w.getItem('showValues').get()

        if not showDeltas:
            return

        instanceGlyph = RGlyph(instanceGlyph)

        instanceGlyph.round()

        dash = 2, 2
        dotSize = 4

        selectedPoints = getImplicitSelectedPoints(self.controller.glyph)

        italicAngle = self.controller.glyph.font.info.italicAngle

        if italicAngle:
            g1_ = instanceGlyph.copy()
            g1_.skewBy((italicAngle, 0))
            g1_.round()
            g2_ = self.controller.glyph.copy()
            g2_.skewBy((italicAngle, 0))
            g2_.round()

        with self.displayLayer.sublayerGroup():

            # draw points

            for ci, c in enumerate(self.controller.glyph):
                for pi, p in enumerate(c.points):
                    p2 = instanceGlyph.contours[ci].points[pi]
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


eventName = f"{BlendsInstancerController.key}.changed"

if eventName not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=eventName,
        methodName="blendsInstancerDidChange",
        lowLevelEventNames=[eventName],
        documentation="Send when the BlendsInstancerController window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(BlendsInstancerController)

