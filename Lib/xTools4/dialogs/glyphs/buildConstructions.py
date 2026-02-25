import ezui
from mojo import drawingTools as ctx
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.UI import GetFile, CurrentFontWindow
from mojo.roboFont import CurrentFont, CurrentGlyph
from mojo.events import postEvent, addObserver, removeObserver
from mojo.pens import DecomposePointPen
from mojo.smartSet import SmartSet
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.accents import buildGlyphConstruction
from xTools4.dialogs.old import hDialog
from xTools4.dialogs.variable.Measurements import colorCheckTrue, colorCheckFalse, colorCheckEqual


KEY = f'{hDialog.key}.glyphs.buildConstructions'


def compositeGlyphFactory(glyph, construction):
    constructionGlyph = GlyphConstructionBuilder(construction, glyph.font)
    return constructionGlyph


class BuildConstructionController(ezui.WindowController):

    title   = 'builder'
    width   = 123
    margins = 10
    verbose = True

    glyph = None

    constructionsTxt = None

    def build(self):
        content = """
        (constructions…)  @loadButton
        (reload ↺)        @reloadButton
        * ColorWell       @colorButton
        [X] preview       @preview
        [X] validate      @validate
        (build)           @buildButton
        (composites)      @filterButton
        """
        descriptionData = dict(
            content=dict(
                sizeStyle="small"
            ),
            loadButton=dict(
                width="fill",
            ),
            reloadButton=dict(
                width="fill",
            ),
            buildButton=dict(
                width="fill",
            ),
            filterButton=dict(
                width="fill",
            ),
            colorButton=dict(
                callback='settingsChangedCallback',
                color=(0, 1, 0.35, 0.8),
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
        BuildConstructionGlyphEditor.controller = self
        registerGlyphEditorSubscriber(BuildConstructionGlyphEditor)
        registerRepresentationFactory(Glyph, f"{KEY}.compositeGlyph", compositeGlyphFactory)
        addObserver(self, "drawLabelCell", "glyphCellDrawBackground")
        self.updateFontViewCallback(None)
        self.glyph = CurrentGlyph()

    def destroy(self):
        unregisterRepresentationFactory(Glyph, f"{KEY}.compositeGlyph")
        removeObserver(self, "glyphCellDrawBackground")
        unregisterGlyphEditorSubscriber(BuildConstructionGlyphEditor)
        BuildConstructionGlyphEditor.controller = None
        self.updateFontViewCallback(None)

    # dynamic attrs

    @property
    def constructions(self):
        if not self.constructionsTxt:
            return
        constructionsRaw  = ParseGlyphConstructionListFromString(self.constructionsTxt)
        constructionsDict = { c.split('=')[0].strip() : c for c in constructionsRaw }
        return constructionsDict

    # callbacks

    def loadButtonCallback(self, sender):
        self.glyphConstructionPath = GetFile(
            message='Get .glyphConstruction file...',
            title=self.title,
            allowsMultipleSelection=False,
            fileTypes=["glyphConstruction"]
        )

        if not self.glyphConstructionPath:
            return

        self._loadConstructions()
        self.updateFontViewCallback(None)
        self.settingsChangedCallback(None)

    def reloadButtonCallback(self, sender):
        self._loadConstructions()
        self.updateFontViewCallback(None)
        self.settingsChangedCallback(None)

    def buildButtonCallback(self, sender):

        font = CurrentFont()
        if not font:
            return

        glyphNames = getGlyphs2(font, glyphNames=True, template=False)
        if not glyphNames:
            return

        if not self.constructions:
            print('no glyph constructions available\n')
            return

        if self.verbose:
            print('building glyph constructions:\n')

        for glyphName in glyphNames:
            construction = self.constructions.get(glyphName)
            if construction is None:
                print(f'\tskipping {glyphName} (no construction)...')
            else:
                buildGlyphConstruction(font, construction, clear=True, verbose=True, autoUnicodes=False, indentLevel=1)

        font.changed()
        if self.verbose:
            print('\n...done.\n')

    def filterButtonCallback(self, sender):

        glyph = CurrentGlyph()
        if glyph is None:
            print('no glyph selected\n')
            return

        compositeGlyphs = [glyph.name]
        for g in glyph.font:
            componentNames = [c.baseGlyph for c in g.components]
            if glyph.name in componentNames:
                if g.name not in compositeGlyphs:
                    compositeGlyphs.append(g.name)

        query = SmartSet()
        query.glyphNames = compositeGlyphs
        queryObject = query.getQueryObject()

        w = CurrentFontWindow()
        w.getGlyphCollection().setQuery(queryObject)

    def updateFontViewCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        for g in font:
            g.changed()

    def settingsChangedCallback(self, sender):
        postEvent(f"{KEY}.changed")

    # methods

    def _loadConstructions(self):

        if self.verbose:
            print('loading glyph constructions from file...', end=' ')

        # read glyph constructions from file
        with open(self.glyphConstructionPath, 'r', encoding='utf-8') as f:
            self.constructionsTxt = f.read()

        if self.verbose:
            print('done.\n')

    def drawLabelCell(self, notification):

        glyph = notification['glyph']

        if not self.constructions:
            return

        construction = self.constructions.get(glyph.name)
        if not construction:
            return

        if not self.w.getItem('validate').get():
            return

        w = CurrentFontWindow()
        cellSize = w.fontOverview.views.sizeSlider.get()
        x, y = cellSize-12, cellSize * 0.35

        constructionGlyph = glyph.getRepresentation(f"{KEY}.compositeGlyph", construction=construction)

        components = [(c.baseGlyph, c.transformation) for c in glyph.components]

        # TO-DO: check if shapes are equal

        if constructionGlyph.components == components and glyph.width == constructionGlyph.width:
            color = colorCheckTrue
        else:
            color = colorCheckFalse

        ctx.save()
        ctx.font('LucidaGrande-Bold')
        ctx.fontSize(10)
        ctx.translate(x, y)
        ctx.fill(*color)
        ctx.text('C', (0, 0))
        ctx.restore()


class BuildConstructionGlyphEditor(Subscriber):

    controller = None

    def build(self):
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="background",
        )
        self.glyphConstructionPreview = container.appendBaseSublayer()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        glyphEditor = self.getGlyphEditor()
        container = glyphEditor.extensionContainer(
            identifier=KEY,
            location="background",
        )
        container.clearSublayers()

    def glyphEditorDidSetGlyph(self, info):
        self.controller.glyph = info["glyph"]
        self._drawGlyphConstruction()

    def glyphConstructionPreviewDidChange(self, info):
        self._drawGlyphConstruction()

    def _drawGlyphConstruction(self):

        preview = self.controller.w.getItem('preview').get()
        color   = self.controller.w.getItem('colorButton').get()

        self.glyphConstructionPreview.clearSublayers()

        if not preview:
            return

        if not self.controller.constructions:
            return

        construction = self.controller.constructions.get(self.controller.glyph.name)
        if not construction:
            return

        constructionGlyph = self.controller.glyph.getRepresentation(f"{KEY}.compositeGlyph", construction=construction)
        if not constructionGlyph:
            return

        previewGlyph = Glyph()
        previewGlyph.width = constructionGlyph.width
        previewPen = previewGlyph.getPointPen()

        font = CurrentFont()

        decomposePen = DecomposePointPen(font, previewPen)
        constructionGlyph.drawPoints(decomposePen)

        glyphPath = previewGlyph.getRepresentation("merz.CGPath")

        glyphConstructionLayerFill = self.glyphConstructionPreview.appendPathSublayer(
            fillColor=color,
            opacity=0.35,
            strokeColor=None,
        )
        glyphConstructionLayerFill.setPath(glyphPath)

        glyphConstructionLayerStroke = self.glyphConstructionPreview.appendPathSublayer(
            fillColor=None,
            strokeColor=color,
            strokeWidth=2,
        )
        glyphConstructionLayerStroke.setPath(glyphPath)


eventName = f"{KEY}.changed"

if eventName not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=eventName,
        methodName="glyphConstructionPreviewDidChange",
        lowLevelEventNames=[eventName],
        documentation="Send when the glyph construction preview changes.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    BuildConstructionController()
