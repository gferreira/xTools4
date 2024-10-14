from vanilla import TextBox, EditText, CheckBox, Button, RadioGroup
from xTools4.dialogs.old import hDialog
from xTools4.modules.glyphutils import findReplaceGlyphName, addToGlyphName


class FindReplaceGlyphNamesDialog(hDialog):

    '''
    A dialog to find and replace a string of characters in the names of selected glyphs.

    ::

        from hTools3.dialogs.glyphs.namesFindReplace import FindReplaceGlyphNamesDialog
        FindReplaceGlyphNamesDialog()

    '''

    title = 'replace'
    key   = f'{hDialog.key}.glyphs.findReplaceGlyphNames'
    settings = {
        'overwrite' : True,
        'duplicate' : False,
    }

    def __init__(self):
        self.height  = self.textHeight * 7
        self.height += self.padding * 5 # - 5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        y -= 3
        self.w.findLabel = TextBox(
                (x, y, -p, self.textHeight),
                "find",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.findText = EditText(
                (x, y, -p, self.textHeight),
                '',
                placeholder='find string',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.replaceLabel = TextBox(
                (x, y, -p, self.textHeight),
                "replace",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.replaceText = EditText(
                (x, y, -p, self.textHeight),
                text='',
                placeholder='replace string',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p + 5
        self.w.findReplaceButton = Button(
                (x, y, -p, self.textHeight),
                "apply",
                callback=self.findReplaceCallback,
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
    def findText(self):
        return self.w.findText.get()

    @property
    def replaceText(self):
        return self.w.replaceText.get()

    @property
    def overwrite(self):
        return bool(self.w.overwrite.get())

    @property
    def duplicate(self):
        return bool(self.w.duplicate.get())

    # ---------
    # callbacks
    # ---------

    def findReplaceCallback(self, sender):

        # assert conditions

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames(template=True)
        if not glyphNames:
            return

        layerNames = self.getLayerNames()
        if not layerNames:
            layerNames = [font.defaultLayer.name]

        # print info

        if self.verbose:
            print('renaming glyphs...\n')
            print(f'\tfind string: {self.findText}')
            print(f'\treplace by: {self.replaceText}')
            print(f'\toverwrite: {self.overwrite}')
            print(f'\tduplicate: {self.duplicate}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print()

        # rename glyphs

        for glyphName in glyphNames:
            for layerName in layerNames:
                layer = font.getLayer(layerName)
                if glyphName not in layer:
                    continue
                g = layer[glyphName]
                g.prepareUndo('rename glyph')
                findReplaceGlyphName(g,
                        self.findText, self.replaceText,
                        overwrite=self.overwrite,
                        duplicate=self.duplicate,
                        verbose=self.verbose)
                g.performUndo()

        print('\n...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    FindReplaceGlyphNamesDialog()
