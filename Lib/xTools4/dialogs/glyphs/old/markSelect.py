from random import random
from vanilla import SquareButton, Button, ColorWell
from xTools4.dialogs.old import hDialog
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.fontutils import markGlyphs, findMarkColor


class MarkGlyphsDialog(hDialog):

    '''
    A dialog to apply, clear and select mark colors in selected glyphs.

    ::

        from hTools3.dialogs.glyphs.markSelect import MarkGlyphsDialog
        MarkGlyphsDialog()

    '''

    title = 'mark'
    key   = f'{hDialog.key}.glyphs.mark'
    settings = {
        'markColor' : (1, 0, 0, 0.5),
    }

    def __init__(self):
        self.height  = self.textHeight * 5
        self.height += self.buttonHeight
        self.height += self.padding * 7
        self.w = self.window((self.width, self.height), self.title)

        x = y = self.padding
        self.w.getColorButton = Button(
                (x, y, -self.padding, self.textHeight),
                "get",
                callback=self.getColorCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + self.padding
        self.w.randomColorButton = Button(
                (x, y, -self.padding, self.textHeight),
                "random",
                callback=self.randomColorCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + self.padding
        self.w.markColor = ColorWell(
                (x, y, -self.padding, self.buttonHeight),
                color=rgb2nscolor(self.settings['markColor']))

        y += self.buttonHeight + self.padding
        self.w.setColorButton = Button(
                (x, y, -self.padding, self.textHeight),
                "set",
                callback=self.setColorCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + self.padding
        self.w.selectButton = Button(
                (x, y, -self.padding, self.textHeight),
                "select",
                callback=self.selectCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + self.padding
        self.w.clearButton = Button(
                (x, y, -self.padding, self.textHeight),
                "clear",
                callback=self.clearCallback,
                sizeStyle=self.sizeStyle)

        self.openWindow()

    # ---------
    # callbacks
    # ---------

    def getColorCallback(self, sender):

        if not self.assertConditions():
            return

        # get 1st glyph
        glyph = self.getCurrentFont()[self.getGlyphNames()[0]]

        # get color
        color = glyph.markColor
        print('%s: %s\n' % (glyph.name, color))

        # HACK: use transparent white for None
        if not color:
            color = 1, 1, 1, 0

        # convert rgba to NSColor
        nsColor = rgb2nscolor(color)

        # update color swatch
        self.w.markColor.set(nsColor)

    def randomColorCallback(self, sender):

        # if not self.assertConditions():
        #     return

        # make a random RGB color
        color = random(), random(), random(), 0.35

        # convert rgba to NSColor
        nsColor = rgb2nscolor(color)

        # update color swatch
        self.w.markColor.set(nsColor)

    def setColorCallback(self, sender):

        if not self.assertConditions():
            return

        font = self.getCurrentFont()
        glyphNames = self.getGlyphNames()

        # get swatch color
        nsColor = self.w.markColor.get()
        color = nscolor2rgb(nsColor)

        # mark glyphs
        print('marking glyphs:\n')
        print('\t', end='')
        print(' '.join(glyphNames), end='\n')

        markGlyphs(font, glyphNames, color, verbose=False)

        font.changed()
        print('\n...done.\n')

    def selectCallback(self, sender):

        if not self.assertConditions():
            return

        font = self.getCurrentFont()
        glyphNames = self.getGlyphNames()

        # get 1st glyph
        glyphName = glyphNames[0]

        # get glyph color
        color = font[glyphName].markColor

        # select all glyphs with the same color
        print('selecting glyphs:\n')
        print('\t', end='')
        glyphNames = findMarkColor(font, color)
        print(' '.join(glyphNames), end='\n')

        font.selectedGlyphNames = glyphNames

        font.changed()
        print('\n...done.\n')

    def clearCallback(self, sender):
        if not self.assertConditions():
            return

        font = self.getCurrentFont()
        glyphNames = self.getGlyphNames()

        markGlyphs(font, glyphNames, None, verbose=False)

        print('removing mark color:\n')
        print('\t', end='')
        print(' '.join(glyphNames), end='\n')

        font.changed()
        print('\n...done.\n')

    # -------
    # methods
    # -------

    def assertConditions(self):
        if not self.getCurrentFont():
            return
        if not self.getGlyphNames():
            return
        return True

# -------
# testing
# -------

if __name__ == "__main__":

    MarkGlyphsDialog()
