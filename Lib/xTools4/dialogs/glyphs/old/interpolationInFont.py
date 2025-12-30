from vanilla import TextBox, EditText, CheckBox, SquareButton, PopUpButton
from mojo.UI import EditStepper
from xTools4.dialogs.old import hDialog
from xTools4.dialogs.old.misc.spinner import Spinner
from xTools4.dialogs.old.misc.spinnerSlider import SpinnerSlider
from xTools4.modules.interpolation import interpolateStepsInFont


KEY = 'com.xTools4.dialogs.glyphs.interpolationInFont'


class InterpolateGlyphsInFontDialog(hDialog):

    '''
    A dialog to interpolate and extrapolate between two glyphs in the same font.

    ::

        from hTools3.dialogs.glyphs.interpolationInFont import InterpolateGlyphsInFontDialog
        InterpolateGlyphsInFontDialog()

    '''

    title = 'interpol'
    key   = KEY

    settings = {
        'interSteps' : 7,
        'extraSteps' : 3,
        'prefix'     : 'result',
    }
    # windowType = 1

    mode = ['linear', 'lucas'][0]

    def __init__(self):
        self.height  = self.textHeight * 5
        self.height += self.padding * 6
        self.height += self.buttonHeight - 2
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 2
        self.w.prefixLabel = TextBox(
                (x, y, -p, self.textHeight),
                "glyph name prefix",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.prefix = EditText(
                (x, y, -p, self.textHeight),
                'result',
                sizeStyle=self.sizeStyle)

        inputWidth = 35
        labelWidth = self.width - inputWidth - p * 2
        y += self.textHeight + p
        self.w.interLabel = TextBox(
                (x, y + 3, labelWidth, self.textHeight),
                'interpol',
                sizeStyle=self.sizeStyle)

        self.w.interSteps = EditText(
                (x + labelWidth, y, inputWidth, self.textHeight),
                self.settings['interSteps'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.extraLabel = TextBox(
                (x, y + 3, labelWidth, self.textHeight),
                'extrapol',
                sizeStyle=self.sizeStyle)

        self.w.extraSteps = EditText(
                (x + labelWidth, y, inputWidth, self.textHeight),
                self.settings['extraSteps'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.clearGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "clear glyphs",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "interpolate",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.w.workspaceWindowIdentifier = KEY

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def prefix(self):
        return self.w.prefix.get()

    @property
    def interSteps(self):
        return int(self.w.interSteps.get())

    @property
    def extraSteps(self):
        return int(self.w.extraSteps.get())

    @property
    def clearGlyphs(self):
        return bool(self.w.clearGlyphs.get())

    # ---------
    # callbacks
    # ---------

    def applyCallback(self, sender):

        # assert conditions
        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        if not len(glyphNames) == 2:
            print("please select two compatible glyphs in the same font\n")
            return

        # get master glyphs
        g1, g2 = glyphNames

        # remove glyphs with prefix
        if self.clearGlyphs:
            for glyphName in font.keys():
                if self.prefix in glyphName:
                    font.removeGlyph(glyphName)
            font.changed()

        # print info
        if self.verbose:
            print('interpolating glyphs:\n')
            print(f'\tglyph 1: {g1}')
            print(f'\tglyph 2: {g2}')
            print(f'\tinter steps: {self.interSteps}')
            print(f'\textra steps: {self.extraSteps}')
            print(f'\tclear: {self.clearGlyphs}')
            print()

        # interpolate glyphs
        interpolateStepsInFont(font, font[g1], font[g2], self.interSteps, self.extraSteps, prefix=self.prefix, mark=True, mode=self.mode)

        print('\n...done.\n')


# -------
# testing
# -------

if __name__ == "__main__":

    InterpolateGlyphsInFontDialog()
