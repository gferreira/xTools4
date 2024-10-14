from vanilla import RadioGroup, Button, CheckBox
from xTools4.dialogs.old import hDialog
from xTools4.modules.encoding import psname2char


class PrintGlyphNamesDialog(hDialog):

    '''
    A dialog to print the names of selected glyphs in multiple output formats.

    ::

        from hTools3.dialogs.glyphs.namesPrint import PrintGlyphNamesDialog
        PrintGlyphNamesDialog()

    '''

    title = 'print'
    key   = f'{hDialog.key}.glyphs.glyphNamesPrint'
    settings = {
        'printMode' : 0,
        'glyphMode' : 0,
        'sortNames' : False,
    }

    def __init__(self):
        self.height  = self.textHeight * 8
        self.height += self.padding * 5 - 2
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.glyphMode = RadioGroup(
                (x, y, -p, self.textHeight * 2),
                ['glyph names', 'unicode chars'],
                sizeStyle=self.sizeStyle,
                isVertical=True)
        self.w.glyphMode.set(self.settings['glyphMode'])

        y += self.textHeight * 2 + p
        self.w.printMode = RadioGroup(
                (x, y, -p, self.textHeight * 4),
                ['plain string', 'plain list', 'Python string', 'Python list'],
                sizeStyle=self.sizeStyle,
                isVertical=True)
        self.w.printMode.set(self.settings['printMode'])

        y += self.textHeight * 4 + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "print",
                callback=self.applyCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + self.padding
        self.w.sortGlyphNames = CheckBox(
                (x, y, -p, self.textHeight),
                "sorted list",
                value=self.settings['sortNames'],
                sizeStyle=self.sizeStyle)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def printMode(self):
        '''
        The selected output mode.

        '''
        return self.w.printMode.get()

    @property
    def glyphMode(self):
        '''
        The selected glyph mode.

        '''
        return self.w.glyphMode.get()

    @property
    def sortGlyphNames(self):
        '''
        A boolean indicating if the glyph names should be sorted.

        '''
        return self.w.sortGlyphNames.get()

    # ---------
    # callbacks
    # ---------

    def applyCallback(self, sender):
        '''
        Print the names of selected glyphs in the chosen output format.

        '''

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # -----------
        # print names
        # -----------

        if self.glyphMode:
            glyphNames = [psname2char(g) for g in glyphNames]

        

        if self.sortGlyphNames:
            glyphNames.sort()
        else:
            # sort using font.glyphorder
            glyphNames = [gName for gName in font.glyphOrder if gName in glyphNames]

        # plain string
        if self.printMode == 0:
            print(' '.join(glyphNames))

        # plain list
        elif self.printMode == 1:
            print('\n'.join(glyphNames))

        # python string
        elif self.printMode == 2:
            print('"%s"' % ' '.join(glyphNames))

        # python list
        else:
            txt = '['
            for i, glyphName in enumerate(glyphNames):
                txt += '"%s"' % glyphName
                if i < len(glyphNames) - 1:
                    txt += ', '
            txt += ']'
            print(txt)

        # done
        print()

# -------
# testing
# -------

if __name__ == '__main__':

    PrintGlyphNamesDialog()
