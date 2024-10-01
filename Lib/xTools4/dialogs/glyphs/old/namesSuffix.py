from importlib import reload
import hTools3.modules.glyphutils
reload(hTools3.modules.glyphutils)

from vanilla import TextBox, EditText, CheckBox, Button, RadioGroup
from hTools3.dialogs import hDialog
from hTools3.modules.glyphutils import findReplaceGlyphName, addToGlyphName


class PrefixSuffixGlyphNamesDialog(hDialog):

    '''
    A dialog to replace or remove a suffix in the names of selected glyphs.

    ::

        from hTools3.dialogs.glyphs.namesSuffix import PrefixSuffixGlyphNamesDialog
        PrefixSuffixGlyphNamesDialog()

    '''

    title = 'suffix'
    key   = f'{hDialog.key}.glyphs.prefixSuffixGlyphNames'
    settings = {
        'overwrite' : True,
        'duplicate' : False,
    }

    def __init__(self):
        self.height  = self.textHeight * 6
        self.height += self.padding * 4 + 5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 3
        self.w.appendLabel = TextBox(
                (x, y, -p, self.textHeight),
                "add",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.addText = EditText(
                (x, y, -p, self.textHeight),
                text='',
                placeholder='add string',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.addMode = RadioGroup(
                (p*0.7, y, -p*0.3, self.textHeight),
                ['prefix', 'suffix'],
                isVertical=False,
                sizeStyle=self.sizeStyle)
        self.w.addMode.set(1)

        y += self.textHeight + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "apply",
                callback=self.addCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.overwrite = CheckBox(
                (x, y, -p, self.textHeight),
                "overwrite",
                value=self.settings['overwrite'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.duplicate = CheckBox(
                (x, y, -p, self.textHeight),
                "duplicate",
                value=self.settings['duplicate'],
                sizeStyle=self.sizeStyle)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def addText(self):
        return self.w.addText.get()

    @property
    def suffix(self):
        return bool(self.w.addMode.get())

    @property
    def overwrite(self):
        return bool(self.w.overwrite.get())

    @property
    def duplicate(self):
        return bool(self.w.duplicate.get())

    # ---------
    # callbacks
    # ---------

    def addCallback(self, sender):

        # assert conditions

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # print info

        if self.verbose:
            print('renaming glyphs...\n')
            print('\tadd string: %s (%s)' % (self.addText, ['prefix', 'suffix'][self.suffix]))
            print('\toverwrite: %s' % self.overwrite)
            print('\tduplicate: %s' % self.duplicate)
            print()

        # rename glyphs

        for glyphName in glyphNames:
            g = font[glyphName]
            g.prepareUndo('rename glyph')
            addToGlyphName(g, self.addText, suffix=self.suffix, overwrite=self.overwrite, duplicate=self.duplicate, verbose=self.verbose)
            g.performUndo()

        print('\n...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    PrefixSuffixGlyphNamesDialog()
