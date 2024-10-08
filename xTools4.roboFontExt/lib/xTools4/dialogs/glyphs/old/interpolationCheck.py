from vanilla import *
from hTools3.dialogs import hDialog


class CheckCompatibilityDialog(hDialog):

    '''
    A dialog to check the interpolation compatibility between glyphs of two open fonts.

    ::

        from hTools3.dialogs.glyphs.interpolationCheck import CheckCompatibilityDialog
        CheckCompatibilityDialog()

    '''

    title = 'check'
    key   = f'{hDialog.key}.glyphs.interpolationCheck'
    fonts = {}

    def __init__(self):
        self.height = self.textHeight * 4 + self.padding * 4 + self.buttonHeight + 3
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.f1Label = TextBox(
                (x, y, -p, self.textHeight),
                "font 1",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.f1Font = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.f2Label = TextBox(
                (x, y, -p, self.textHeight),
                "font 2",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.f2Font = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 3
        self.w.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                'apply',
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        self.openWindow()

    def applyCallback(self, sender):
        pass

if __name__ == "__main__":
    CheckCompatibilityDialog()
