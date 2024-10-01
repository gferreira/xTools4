from vanilla import SquareButton, List, CheckBox, ColorWell
from mojo.UI import PutFile, GetFile
from mojo.roboFont import CurrentFont
from hTools3.dialogs import hDialog
from hTools3.modules.color import rgb2nscolor, nscolor2rgb

class DuplicateRenameGlyphsDialog(hDialog):

    '''
    A dialog to duplicate glyphs under new names in the current font.

    '''

    title = 'duplicate glyphs'
    key = '%s.font.duplicateRename' % hDialog.key
    windowType = 1
    settings = {}

    def __init__(self):
        self.height  = self.buttonHeight * 6
        self.height += self.textHeight * 12
        self.height += self.padding * 10
        self.w = self.window((self.width * 3, self.height), self.title)

        x = y = p = self.padding
        self.w.addSelectionToList = SquareButton(
                (x, y, -p, self.buttonHeight),
                'add current font selection',
                callback=self.addSelectionToListCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.importGlyphNames = SquareButton(
                (x, y, -p, self.buttonHeight),
                'import glyph names from file…',
                callback=self.importGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        textBoxHeight = self.textHeight * 8
        self.w.glyphNames = List(
                (x, y, -p, textBoxHeight),
                [],
                enableDelete=True,
                drawFocusRing=False,
                columnDescriptions=[
                    dict(title='original',  editable=True, allowsSorting=True),
                    dict(title='duplicate', editable=True, allowsSorting=True),
                ],
            )

        y += textBoxHeight + p
        self.w.addEntry = SquareButton(
                (x, y, -p, self.buttonHeight),
                'add new entry',
                callback=self.addNewEntryCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.selectAllGlyphNames = CheckBox(
                (x, y, -p, self.textHeight),
                'select all',
                value=False,
                callback=self.selectAllGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.exportGlyphNames = SquareButton(
                (x, y, -p, self.buttonHeight),
                'export glyph names to file…',
                callback=self.exportGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.duplicateAndRename = SquareButton(
                (x, y, -p, self.buttonHeight),
                "duplicate glyphs",
                callback=self.duplicateAndRenameCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                'preflight',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.overwrite = CheckBox(
                (x, y, -p, self.textHeight),
                'overwrite existing glyphs',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.markGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                'mark duplicates',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        nsColor = rgb2nscolor((0, 0.5, 1, 0.5))
        self.w.markColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=nsColor)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def allGlyphNames(self):
        glyphNames = []
        for entry in self.w.glyphNames.get():
            glyphNames.append((entry['original'], entry['duplicate']))
        return glyphNames

    @property
    def selectedGlyphNames(self):
        selection = self.w.glyphNames.getSelection()
        glyphNames = []
        for i, glyphName in enumerate(self.allGlyphNames):
            if i in selection:
                glyphNames.append(glyphName)
        return glyphNames

    # ---------
    # callbacks
    # ---------

    def addSelectionToListCallback(self, sender):
        f = CurrentFont()
        if not f:
            print('no font open')
            return

        glyphNames = f.selectedGlyphNames
        if not len(glyphNames):
            print('no glyph selected')
            return

        entries = []
        for glyphName in glyphNames:
            entry = {'original': glyphName, 'duplicate': '...'}
            entries.append(entry)

        self.w.glyphNames.extend(entries)

    def selectAllGlyphNamesCallback(self, sender):
        if sender.get():
            selection = list(range(len(self.w.glyphNames)))
        else:
            selection = []
        self.w.glyphNames.setSelection(selection)

    def addNewEntryCallback(self, sender):
        print('adding new entry…\n')
        entry = {'original': '...', 'duplicate': '...'}
        self.w.glyphNames.append(entry)

    def importGlyphNamesCallback(self, sender):
        msg = 'import glyph names from .txt file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['txt'])
        if not filePath:
            print('no txt file selected.\n')
            return
        self.importGlyphNames(filePath)

    def exportGlyphNamesCallback(self, sender):
        msg = 'export glyph names to .txt file'
        filePath = PutFile(message=msg, fileName='duplicates.txt')
        if filePath:
            self.exportGlyphNames(filePath)

    def duplicateAndRenameCallback(self, sender):
        if self.w.preflight.get():
            self.preflight()
        else:
            self.duplicateAndRenameGlyphs()

    # -------
    # methods
    # -------

    def preflight(self):
        # get options
        overwrite  = self.w.overwrite.get()
        markGlyphs = self.w.markGlyphs.get()

        # print glyph names
        print('duplicate glyphs:')
        if len(self.selectedGlyphNames):
            for original, duplicate in self.selectedGlyphNames:
                print('- %s -> %s' % (original, duplicate))
        else:
            print('- [None]')
        print()

        # print options
        print('options:')
        if any([overwrite, markGlyphs]):
            if overwrite:
                print('- overwrite existing glyphs')
            if markGlyphs:
                print('- mark duplicates')
        else:
            print('- [None]')

        # done
        print()

    def importGlyphNames(self, filePath):
        print('importing glyph names from file…')

        # read glyph names from txt file
        with open(filePath, 'r') as inputFile:
            entries = []
            for L in inputFile.readlines():
                try:
                    original, duplicate = L.strip().split()
                except:
                    continue
                entry = {'original': original, 'duplicate': duplicate}
                entries.append(entry)

        # set glyph names in the UI
        self.w.glyphNames.set(entries)

        # done
        print('…done.\n')

    def exportGlyphNames(self, filePath):
        print('exporting glyph names to file…')
        txt = ''
        for original, duplicate in self.allGlyphNames:
            txt += '%s %s\n' % (original, duplicate)

        # save marks to txt file
        with open(filePath, 'w') as outputFile:
            outputFile.write(txt)

        # done
        print('…done.\n')

    def duplicateAndRenameGlyphs(self):

        # assert conditions

        f = CurrentFont()
        if not f:
            print('no font open')
            return

        if not len(self.selectedGlyphNames):
            print('no glyph selected')
            return

        # ----------------
        # duplicate glyphs
        # ----------------

        print('duplicating glyphs...\n')

        # get options
        overwrite  = self.w.overwrite.get()
        markGlyphs = self.w.markGlyphs.get()
        markColor  = nscolor2rgb(self.w.markColor.get())

        for original, duplicate in self.selectedGlyphNames:
            print("\tduplicating '%s' as '%s'..." % (original, duplicate))

            if overwrite or duplicate not in f:
                f.insertGlyph(f[original], name=duplicate)
                f[duplicate].unicodes = []

            else:
                f[duplicate].appendGlyph(f[original])

            if markGlyphs:
                f[duplicate].markColor = markColor

        print()
        print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    DuplicateRenameGlyphsDialog()
