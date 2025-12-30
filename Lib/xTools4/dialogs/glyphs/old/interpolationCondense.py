from vanilla import TextBox, PopUpButton, CheckBox, Button
from mojo import drawingTools as ctx
from mojo.roboFont import AllFonts
from mojo.events import addObserver, removeObserver
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase
from xTools4.modules.interpolation import condenseGlyph
from xTools4.dialogs.old.misc.numberEditText001 import NumberEditText_001


KEY = f'{GlyphsDialogBase.key}.interpolationCondense'


class CondenseGlyphsDialog(GlyphsDialogBase):

    '''
    A dialog to generate condensed glyphs from a regular and a bold font.

    ::

        from xTools4.dialogs.glyphs.old.interpolationCondense import CondenseGlyphsDialog
        CondenseGlyphsDialog()

    '''

    title = 'condense'
    key   = KEY
    settings = {
        'regularStem' : 70,
        'boldStem'    : 170,
        'factor'      : 0.2,
    }
    allFonts = {}

    def __init__(self):
        self.height  = self.textHeight * 7
        self.height += self.padding * 6
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        col = (self.width - p*2) / 2
        y -= 2
        self.w.regularLabel = TextBox(
                (x, y, -p, self.textHeight),
                "regular",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.regularFont = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.boldLabel = TextBox(
                (x, y, -p, self.textHeight),
                "bold",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.boldFont = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 3
        self.w.factorLabel = TextBox(
                (x, y, col, self.textHeight),
                'factor',
                sizeStyle=self.sizeStyle)
        self.w.factorValue = NumberEditText_001(
                (x+col, y, -p, self.textHeight),
                text=self.settings['factor'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                continuous=False)

        y += self.textHeight + p
        self.w.buttonApply = Button(
                (x, y, -p, self.textHeight),
                "apply",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.updateFonts()
        self.updateFontLists()
        
        self.initGlyphsWindowBehaviour()

        addObserver(self, "updateFontsCallback", "newFontDidOpen")
        addObserver(self, "updateFontsCallback", "fontDidOpen")
        addObserver(self, "updateFontsCallback", "fontDidClose")

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def regularFontName(self):
        selection = self.w.regularFont.get()
        items = self.w.regularFont.getItems()
        return items[selection]

    @property
    def boldFontName(self):
        selection = self.w.boldFont.get()
        items = self.w.boldFont.getItems()
        return items[selection]

    @property
    def regularFont(self):
        return self.allFonts[self.regularFontName]

    @property
    def boldFont(self):
        return self.allFonts[self.boldFontName]

    @property
    def regularStem(self):
        if not len(self.regularFont.info.postscriptStemSnapV):
            return self.settings['regularStem']
        else:
            return self.regularFont.info.postscriptStemSnapV[0]

    @property
    def boldStem(self):
        if not len(self.boldFont.info.postscriptStemSnapV):
            return self.settings['boldStem']
        else:
            return self.boldFont.info.postscriptStemSnapV[0]

    @property
    def factor(self):
        return self.w.factorValue.get()

    # ---------
    # callbacks
    # ---------

    def updateFontsCallback(self, sender):
        self.updateFonts()
        self.updateFontLists()

    def windowCloseCallback(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontWillClose")
        removeObserver(self, "drawBackground")
        super().windowCloseCallback(sender)

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

        # make preview
        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def updateFonts(self):
        allFonts = {}
        for font in AllFonts():
            fontName = '%s %s' % (font.info.familyName, font.info.styleName)
            allFonts[fontName] = font
        # update fonts list
        self.allFonts = allFonts

    def updateFontLists(self):
        allFontsNames = sorted(self.allFonts.keys())
        self.w.regularFont.setItems(allFontsNames)
        self.w.boldFont.setItems(allFontsNames)

    def drawPreview(self, glyph, previewScale, plain=False):
        x1, x2 = 0, glyph.width
        y1, y2 = -10000, 10000

        ctx.save()

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = 10000
            h = 10000
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        # draw margins
        if not plain:
            ctx.lineDash(self.previewStrokeWidth * previewScale, self.previewStrokeWidth * previewScale)
            ctx.line((x1, y1), (x1, y2))
            ctx.line((x2, y1), (x2, y2))

        ctx.restore()

    def makeGlyph(self, glyph, preview=False):

        if preview:
            glyph = glyph.copy()

        regularGlyph = self.regularFont[glyph.name]
        boldGlyph = self.boldFont[glyph.name]

        condenseGlyph(regularGlyph, boldGlyph, glyph, self.regularStem, self.boldStem, self.factor)

        return glyph

    def apply(self):

        # assert conditions

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # print info

        if self.verbose:
            print('condensing glyphs:\n')
            print('\tregular font: %s (%s)' % (self.regularFontName, self.regularStem))
            print('\tbold font: %s (%s)' % (self.boldFontName, self.boldStem))
            print()
            print('\t', end='')
            print(' '.join(glyphNames), end='\n')

        # transform glyphs

        for glyphName in glyphNames:
            g = font[glyphName]
            g.prepareUndo('condense')
            self.makeGlyph(g)
            g.performUndo()
            g.changed()

        # done
        font.changed()
        if self.verbose:
            print('\n...done.\n')


# -------
# testing
# -------

if __name__ == "__main__":

    CondenseGlyphsDialog()
