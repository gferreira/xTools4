from vanilla import Button, CheckBox
from mojo import drawingTools as ctx
from mojo.UI import GetFile, CodeEditor, getDefault
from mojo.events import removeObserver
from mojo.roboFont import RGlyph, CurrentFont
from mojo.pens import DecomposePointPen
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase
from xTools4.modules.accents import buildGlyphConstruction


class BuildConstructionDialog(GlyphsDialogBase):

    '''
    A dialog to preview and build new glyphs using Glyph Construction syntax.

    ::

        from xTools4.dialogs.glyphs.old.buildConstructions import BuildConstructionDialog
        BuildConstructionDialog()

    '''

    title = 'constructions'
    key   = f'{GlyphsDialogBase.key}.constructions'
    settings = {}
    glyphConstructionPath = None

    def __init__(self):
        self.height = 300 # self.textHeight * 3 + self.padding * 4
        self.w = self.window(
            (self.width, self.height),
            self.title,
            minSize=(self.width, self.height))

        x = y = p = self.padding
        self.w.importButton = Button(
            (x, y, -p, self.textHeight),
            'import...',
            sizeStyle=self.sizeStyle,
            callback=self.importConstructionsCallback)

        y += self.textHeight + p
        textBoxHeight = -(self.textHeight + p) * 3 - p
        self.w.glyphConstructions = CodeEditor(
                (x, y, -p, textBoxHeight),
                '',
                showLineNumbers=False)

        y = -(self.textHeight + p) * 3
        self.w.exportButton = Button(
            (x, y, -p, self.textHeight),
            'export',
            sizeStyle=self.sizeStyle,
            callback=self.exportConstructionsCallback)

        y = -(self.textHeight + p) * 2
        self.w.buildConstructions = Button(
            (x, y, -p, self.textHeight),
            'build',
            sizeStyle=self.sizeStyle,
            callback=self.applyCallback)

        y = -(self.textHeight + p)
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def constructions(self):
        constructionsTxt  = self.w.glyphConstructions.get()
        constructionsRaw  = ParseGlyphConstructionListFromString(constructionsTxt)
        constructionsDict = { c.split('=')[0].strip() : c for c in constructionsRaw }
        return constructionsDict

    # ---------
    # callbacks
    # ---------

    def importConstructionsCallback(self, sender):

        self.glyphConstructionPath = GetFile(message='Get .glyphConstruction file…', title=self.title)

        if not self.glyphConstructionPath:
            return

        if self.verbose:
            print('importing glyph constructions from file…')

        # read glyph constructions from file
        with open(self.glyphConstructionPath, 'r', encoding='utf-8') as f:
            constructions = f.read()

        self.w.glyphConstructions.set(constructions)

        if self.verbose:
            print('…done.\n')

    def exportConstructionsCallback(self, sender):
        constructionsTxt = self.w.glyphConstructions.get()

        if self.verbose:
            print('exporting glyph constructions back to file…')

        with open(self.glyphConstructionPath, 'w', encoding='utf-8') as f:
            constructions = f.write(constructionsTxt)

        if self.verbose:
            print('…done.\n')

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if g is None:
            return

        font = g.font
        construction = self.constructions.get(g.name)

        if not construction:
            return

        # make preview

        constructionGlyph = GlyphConstructionBuilder(construction, font)

        previewGlyph = RGlyph()
        previewGlyph.width = constructionGlyph.width
        previewPen = previewGlyph.getPointPen()

        decomposePen = DecomposePointPen(font, previewPen)
        constructionGlyph.drawPoints(decomposePen)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale, plain=False):

        ctx.save()

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = getDefault("glyphViewDefaultWidth")
            h = getDefault("glyphViewDefaultHeight")
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        ctx.restore()

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames(template=True)
        if not glyphNames:
            return

        if not self.constructions:
            print('no .glyphConstruction file\n')
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('building glyph constructions:\n')
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # ------------
        # build glyphs
        # ------------

        for glyphName in glyphNames:
            construction = self.constructions.get(glyphName)
            if construction is None:
                continue
            buildGlyphConstruction(font, construction, clear=True, verbose=False, autoUnicodes=False)

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')

# --------
# testing
# -------

if __name__ == "__main__":

    BuildConstructionDialog()
