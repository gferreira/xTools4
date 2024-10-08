import ezui
from merz import MerzView
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from mojo import drawingTools as ctx
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.UI import UpdateCurrentGlyphView, GetFile
from mojo.roboFont import OpenFont, CurrentFont, CurrentGlyph, RGlyph, OpenWindow
from mojo.events import postEvent, addObserver, removeObserver
from variableValues.validation import *


KEY = 'com.fontBureau.glyphValidator'


def checkResultsFactory(glyph, defaultGlyph=None):
    if defaultGlyph is None:
        defaultGlyph = RGlyph()
    glyph = glyph.asFontParts()
    checkResults = {
        'compatibility' : checkCompatibility(glyph, defaultGlyph),
        'equality'      : checkEquality(glyph, defaultGlyph),
    }
    return checkResults


class GlyphValidatorController(ezui.WindowController):

    title   = 'validator'
    width   = 123
    margins = 10

    defaultPath = None
    defaultFont = None

    colorCheckTrue  = 0.00, 0.85, 0.00, 1.00
    colorCheckFalse = 1.00, 0.00, 0.00, 1.00
    colorCheckEqual = 0.00, 0.33, 1.00, 1.00

    content = """
    ( get default… )   @getDefaultButton
    ( reload ↺ )       @reloadButton

    checks
    [X] width          @widthCheck
    [ ] left           @leftCheck
    [ ] right          @rightCheck
    [X] points         @pointsCheck
    [X] components     @componentsCheck
    [X] anchors        @anchorsCheck
    [X] unicodes       @unicodesCheck

    display
    [X] font overview  @displayFontOverview
    [X] glyph window   @displayGlyphWindow

    ( mark glyphs )    @markGlyphsButton
    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        getDefaultButton=dict(
            width='fill',
        ),
        reloadButton=dict(
            width='fill',
        ),
        markGlyphsButton=dict(
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
        GlyphValidatorGlyphEditor.controller = self
        GlyphValidatorRoboFont.controller = self
        registerRepresentationFactory(Glyph, f"{KEY}.checkResults", checkResultsFactory)
        addObserver(self, "checkResultsGlyphCellDrawBackground", "glyphCellDrawBackground")
        registerGlyphEditorSubscriber(GlyphValidatorGlyphEditor)
        registerRoboFontSubscriber(GlyphValidatorRoboFont)

    def destroy(self):
        unregisterGlyphEditorSubscriber(GlyphValidatorGlyphEditor)
        unregisterRoboFontSubscriber(GlyphValidatorRoboFont)
        GlyphValidatorGlyphEditor.controller = None
        GlyphValidatorRoboFont.controller = None
        unregisterRepresentationFactory(Glyph, f"{KEY}.checkResults")
        removeObserver(self, "glyphCellDrawBackground")
        self.updateFontViewCallback(None)

    # dynamic attrs

    @property
    def checks(self):
        checkNames = ['width', 'left', 'right', 'points', 'components', 'anchors', 'unicodes']
        checksDisplay = {}
        for checkName in checkNames:
            checkBoxName = f'{checkName}Check' 
            checkBox = self.w.getItem(checkBoxName)
            checksDisplay[checkName] = checkBox.get()
        return checksDisplay

    # callbacks

    def getDefaultButtonCallback(self, sender):
        self.defaultPath = GetFile(message='Get default source…', title=self.title)
        self.defaultFont = OpenFont(self.defaultPath, showInterface=False)
        postEvent(f"{KEY}.changed")
        self.updateFontViewCallback(sender)

    def reloadButtonCallback(self, sender):
        if self.defaultFont is None:
            return
        self.defaultFont = OpenFont(self.defaultPath, showInterface=False)
        postEvent(f"{KEY}.changed")
        self.updateFontViewCallback(sender)

    def widthCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def leftCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def rightCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def pointsCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def componentsCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def anchorsCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def unicodesCheckCallback(self, sender):
        self.settingsChangedCallback(None)

    def markGlyphsButtonCallback(self, sender):
        currentFont = CurrentFont()
        defaultFont = self.defaultFont
        if currentFont is None or defaultFont is None:
            return
        applyValidationColors(currentFont, defaultFont)

    def settingsChangedCallback(self, sender):
        postEvent(f"{KEY}.changed")
        self.updateFontViewCallback(sender)

    def updateFontViewCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        for g in font:
            g.changed()

    # drawing

    def checkResultsGlyphCellDrawBackground(self, notification):
        if not self.w.getItem("displayFontOverview"):
            return

        if self.defaultFont is None:
            return

        glyph = notification['glyph']

        if glyph.name not in self.defaultFont:
            return

        defaultGlyph = self.defaultFont[glyph.name]
        checkResults = glyph.getRepresentation(f"{KEY}.checkResults", defaultGlyph=defaultGlyph)

        if not len(self.checks) or not checkResults['compatibility'] or not checkResults['equality']:
            return

        ctx.save()
        ctx.font('LucidaGrande-Bold')
        ctx.fontSize(10)
        ctx.translate(3, 5)
        for checkName, checkDisplay in self.checks.items():
            # check is hidden
            if not checkDisplay:
                continue
            isCompatible = checkResults['compatibility'].get(checkName)
            isEqual      = checkResults['equality'].get(checkName)
            if isCompatible and isEqual:
                ctx.fill(*self.colorCheckEqual)
            elif isCompatible or isEqual:
                ctx.fill(*self.colorCheckTrue)
            else:
                ctx.fill(*self.colorCheckFalse)
            # draw check label
            label = checkName[0].upper()
            ctx.text(label, (0, -3))
            w, h = ctx.textSize(label)
            ctx.translate(w + 2, 0)
        ctx.restore()


class GlyphValidatorRoboFont(Subscriber):

    controller = None

    def fontDocumentDidBecomeCurrent(self, info):
        self.controller.updateFontViewCallback(None)

    def fontDocumentDidOpen(self, info):
        self.controller.updateFontViewCallback(None)

    def fontDocumentDidClose(self, info):
        self.controller.updateFontViewCallback(None)


class GlyphValidatorGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        sizeX, sizeY = 400, 40
        self.merzView = MerzView((0, -sizeY, sizeX, sizeY))
        merzContainer = self.merzView.getMerzContainer()
        color = 0, 0.5, 1, 1
        self.reportLayer = merzContainer.appendTextBoxSublayer(
            name=f'{KEY}.report',
            position=(0, 0),
            size=(sizeX, sizeY),
            padding=(10, 10),
            font='LucidaGrande-Bold',
            fillColor=color,
            pointSize=15,
            horizontalAlignment="left",
            verticalAlignment="bottom",
        )
        glyphEditor.addGlyphEditorSubview(self.merzView)

        # initialize preview
        self.controller.glyph = CurrentGlyph()
        self._drawCheckResults()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        glyphEditor.removeGlyphEditorSubview(self.merzView)

    def glyphValidatorDidChange(self, info):
        self._drawCheckResults()

    def glyphEditorDidSetGlyph(self, info):
        self.controller.glyph = info["glyph"]
        self._drawCheckResults()

    def glyphEditorGlyphDidChange(self, info):
        self.controller.glyph = info["glyph"]
        self._drawCheckResults()

    def _drawCheckResults(self):

        glyphName = self.controller.glyph.name

        if self.controller.defaultFont is None or glyphName not in self.controller.defaultFont:
            return

        defaultGlyph = self.controller.defaultFont[glyphName]
        checkResults = self.controller.glyph.getRepresentation(f"{KEY}.checkResults", defaultGlyph=defaultGlyph)

        isEqualResults      = checkResults['equality']
        isCompatibleResults = checkResults['compatibility']

        txt = []
        for checkName, isEqual in isEqualResults.items():
            if not self.controller.checks.get(checkName):
                continue
            isCompatible = isCompatibleResults.get(checkName)
            if isCompatible and isEqual:
                color = self.controller.colorCheckEqual
            elif isCompatible or isEqual:
                color = self.controller.colorCheckTrue
            else:
                color = self.controller.colorCheckFalse
            txt.append(
                dict(
                    text=f'{checkName[0].upper()} ',
                    fillColor=color,
                )
            )

        with self.reportLayer.propertyGroup():
            self.reportLayer.setText(txt)


glyphValidatorEvent = f"{KEY}.changed"

if glyphValidatorEvent not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=glyphValidatorEvent,
        methodName="glyphValidatorDidChange",
        lowLevelEventNames=[glyphValidatorEvent],
        documentation="Send when the GlyphValidator window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(GlyphValidatorController)
