from importlib import reload
import xTools4.modules.validation
reload(xTools4.modules.validation)

import ezui
from merz import MerzView
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from mojo import drawingTools as ctx
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.UI import GetFile, CurrentFontWindow
from mojo.roboFont import OpenFont, CurrentFont, CurrentGlyph, RGlyph, OpenWindow
from mojo.events import postEvent, addObserver, removeObserver
from mojo.smartSet import SmartSet
from xTools4.modules.validation import *
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


KEY = 'com.xTools4.glyphValidator'


def checkResultsFactory(glyph, defaultGlyph=None):
    if defaultGlyph is None:
        defaultGlyph = RGlyph()
    glyph = glyph.asFontParts()
    checkResults = {
        'compatibility' : checkCompatibility(glyph, defaultGlyph),
        'equality'      : checkEquality(glyph, defaultGlyph),
    }
    return checkResults

def validationGroupFactory(glyph, defaultGlyph=None):
    if defaultGlyph is None:
        defaultGlyph = RGlyph()
    glyph = glyph.asFontParts()

    checkResults = {
        'compatibility' : checkCompatibility(glyph, defaultGlyph),
        'equality'      : checkEquality(glyph, defaultGlyph),
    }

    validationGroup = None

    # glyphs with components
    if glyph.components:
        levels = getNestingLevels(glyph)
        # warning: nested components or mixed contour/components
        if levels > 1 or len(glyph.contours):
            validationGroup = 'warning'
        else:
            # components equal to default
            if all(checkResults['compatibility']) and checkResults['equality']['components']:
                validationGroup = 'componentsEqual'
            # components different from default
            else:
                validationGroup = 'componentsDifferent'
    else:
        # contours equal to default
        if checkResults['compatibility']['points'] and checkResults['equality']['points']:
            if glyph.font.path != defaultGlyph.font.path:
                validationGroup = 'contoursEqual'
            else:
                validationGroup = 'contoursDifferent'
        else:
            # empty glyphs
            if not len(defaultGlyph) and not len(glyph):
                # width equal to default
                if glyph.width == defaultGlyph.width:
                    validationGroup = 'contoursEqual'
                # width different from default
                else:
                    validationGroup = 'contoursDifferent'
            # contours different from default
            else:
                validationGroup = 'contoursDifferent'

    return validationGroup


class GlyphValidatorController(ezui.WindowController):

    title   = 'validator'
    width   = 123
    margins = 10

    defaultPath = None
    defaultFont = None

    content = """
    ( get default… )         @getDefaultButton
    ( reload ↺ )             @reloadButton

    * Accordion: checks      @checksPanel
    > [X] width              @widthCheck
    > [ ] left               @leftCheck
    > [ ] right              @rightCheck
    > [X] points             @pointsCheck
    > [X] components         @componentsCheck
    > [X] anchors            @anchorsCheck
    > [X] unicodes           @unicodesCheck

    * Accordion: display     @displayPanel
    > [X] font overview      @displayFontOverview
    > [X] glyph window       @displayGlyphWindow

    * Accordion: validation  @filtersPanel
    > [ ] /= contours        @filterContoursEqual
    > [ ] ≠ contours         @filterContoursDifferent
    > [ ] /= components      @filterComponentsEqual
    > [ ] ≠ components       @filterComponentsDifferent
    > [ ] ‼ not allowed      @filterNestedMixed
    > ( mark glyphs )        @markGlyphsButton
    """

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        displayPanel=dict(
            closed=True
        ),
        filtersPanel=dict(
            closed=True
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
        registerRepresentationFactory(Glyph, f"{KEY}.validationGroup", validationGroupFactory)
        addObserver(self, "checkResultsGlyphCellDrawBackground", "glyphCellDrawBackground")
        registerGlyphEditorSubscriber(GlyphValidatorGlyphEditor)
        registerRoboFontSubscriber(GlyphValidatorRoboFont)

    def destroy(self):
        unregisterGlyphEditorSubscriber(GlyphValidatorGlyphEditor)
        unregisterRoboFontSubscriber(GlyphValidatorRoboFont)
        GlyphValidatorGlyphEditor.controller = None
        GlyphValidatorRoboFont.controller = None
        unregisterRepresentationFactory(Glyph, f"{KEY}.checkResults")
        unregisterRepresentationFactory(Glyph, f"{KEY}.validationGroup")
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

    def filterContoursEqualCallback(self, sender):
        self.updateFiltersCallback(sender)

    def filterContoursDifferentCallback(self, sender):
        self.updateFiltersCallback(sender)

    def filterComponentsEqualCallback(self, sender):
        self.updateFiltersCallback(sender)

    def filterComponentsDifferentCallback(self, sender):
        self.updateFiltersCallback(sender)

    def filterNestedMixedCallback(self, sender):
        self.updateFiltersCallback(sender)

    def updateFiltersCallback(self, sender):
        currentFont = CurrentFont()
        defaultFont = self.defaultFont
        if currentFont is None or defaultFont is None:
            return

        contoursEqual       = []
        contoursDifferent   = []
        componentsEqual     = []
        componentsDifferent = []
        nestedMixed         = []

        for glyphName in currentFont.glyphOrder:
            defaultGlyph = defaultFont[glyphName]
            group = currentFont[glyphName].getRepresentation(f"{KEY}.validationGroup", defaultGlyph=defaultGlyph)
            if group == 'componentsEqual':
                componentsEqual.append(glyphName)
            elif group == 'componentsDifferent':
                componentsDifferent.append(glyphName)
            elif group == 'contoursEqual':
                contoursEqual.append(glyphName)
            elif group == 'contoursDifferent':
                contoursDifferent.append(glyphName)
            elif group == 'warning':
                nestedMixed.append(glyphName)

        filters = {
            'contoursEqual'       : self.w.getItem('filterContoursEqual').get(),
            'contoursDifferent'   : self.w.getItem('filterContoursDifferent').get(),
            'componentsEqual'     : self.w.getItem('filterComponentsEqual').get(),
            'componentsDifferent' : self.w.getItem('filterComponentsDifferent').get(),
            'nestedMixed'         : self.w.getItem('filterNestedMixed').get(),
        }

        # don't update if filters state has not changed
        if filters == currentFont.tempLib.get(f'{KEY}.filters'):
            return

        if not any(filters.values()):
            glyphNames = None
        else:
            glyphNames = []
            if self.w.getItem('filterContoursEqual').get():
                glyphNames += contoursEqual
            if self.w.getItem('filterContoursDifferent').get():
                glyphNames += contoursDifferent
            if self.w.getItem('filterComponentsEqual').get():
                glyphNames += componentsEqual
            if self.w.getItem('filterComponentsDifferent').get():
                glyphNames += componentsDifferent
            if self.w.getItem('filterNestedMixed').get():
                glyphNames += nestedMixed

        query = SmartSet()
        if glyphNames is not None:
            query.glyphNames = glyphNames
            queryObject = query.getQueryObject()
        else:
            queryObject = None

        w = CurrentFontWindow()
        w.getGlyphCollection().setQuery(queryObject)

        # store filters state in temp lib
        currentFont.tempLib[f'{KEY}.filters'] = filters

    def displayFontOverviewCallback(self, sender):
        self.updateFontViewCallback(sender)

    def displayGlyphWindowCallback(self, sender):
        postEvent(f"{KEY}.changed")

    def settingsChangedCallback(self, sender):
        postEvent(f"{KEY}.changed")
        self.updateFontViewCallback(sender)

    def updateFontViewCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        for g in font:
            g.changed()

    def checkResultsGlyphCellDrawBackground(self, notification):
        if not self.w.getItem("displayFontOverview").get():
            return

        if self.defaultFont is None:
            return

        if CurrentFont() == self.defaultFont:
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
                ctx.fill(*colorCheckEqual)
            elif isCompatible or isEqual:
                ctx.fill(*colorCheckTrue)
            else:
                ctx.fill(*colorCheckFalse)
            # draw check label
            label = checkName[0].upper()
            ctx.text(label, (0, -3))
            w, h = ctx.textSize(label)
            ctx.translate(w + 2, 0)
        ctx.restore()


class GlyphValidatorRoboFont(Subscriber):

    controller = None

    def fontDocumentDidBecomeCurrent(self, info):
        currentFont = info['font']
        filters = currentFont.tempLib.get(f'{KEY}.filters')
        if filters:
            for key, value in filters.items():
                checkbox = self.controller.w.getItem(f'filter{key[0].upper()}{key[1:]}')
                checkbox.set(value)
        self.controller.updateFontViewCallback(None)
        self.controller.updateFiltersCallback(None)

    def fontDocumentDidOpen(self, info):
        self.controller.updateFontViewCallback(None)
        self.controller.updateFiltersCallback(None)

    def fontDocumentDidClose(self, info):
        self.controller.updateFontViewCallback(None)


class GlyphValidatorGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        sizeX, sizeY = 400, 40
        self.merzView = MerzView((0, -sizeY, sizeX, sizeY))
        container = self.merzView.getMerzContainer()
        color = 0, 0.5, 1, 1
        self.reportLayer = container.appendTextBoxSublayer(
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

        if self.controller.glyph is None:
            return

        glyphName = self.controller.glyph.name

        if self.controller.defaultFont is None or glyphName not in self.controller.defaultFont:
            return

        if not self.controller.w.getItem('displayGlyphWindow').get():
            self.reportLayer.setVisible(False)
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
                color = colorCheckEqual
            elif isCompatible or isEqual:
                color = colorCheckTrue
            else:
                color = colorCheckFalse
            txt.append(
                dict(
                    text=f'{checkName[0].upper()} ',
                    fillColor=color,
                )
            )

        with self.reportLayer.propertyGroup():
            self.reportLayer.setText(txt)
            self.reportLayer.setVisible(True)


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
