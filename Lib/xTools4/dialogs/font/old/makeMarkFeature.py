from vanilla import SquareButton, List, CheckBox
from mojo.UI import PutFile, GetFile
from mojo.roboFont import CurrentFont
from xTools4.dialogs.old import hDialog
from xTools4.modules.markFeature import markToBaseFeaBuilder

KEY = 'com.xTools4.makeMarksFeature'
def markToBaseList2Dict(marksList):
    marksDict = {}
    for baseGlyph, markGlyph, anchorName in marksList:
        if baseGlyph not in marksDict:
            marksDict[baseGlyph] = []
        marksDict[baseGlyph].append((markGlyph, anchorName))
    return marksDict


class MakeMarkFeatureDialog(hDialog):

    '''
    A dialog to generate mark feature code from a list of base glyphs, mark glyphs and anchor names.

    '''

    title = 'make mark'
    key = '%s.font.makeMark' % hDialog.key
    windowType = 0
    settings = {}

    def __init__(self):
        self.height  = self.buttonHeight * 4
        self.height += self.textHeight * 11
        self.height += self.padding * 8
        self.w = self.window((self.width * 3, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        self.w.importMarks = SquareButton(
                (x, y, -p, self.buttonHeight),
                'import list from file…',
                callback=self.importMarksCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        textBoxHeight = self.textHeight * 8
        self.w.marksList = List(
                (x, y, -p, textBoxHeight),
                [],
                enableDelete=True,
                drawFocusRing=False,
                columnDescriptions=[
                    dict(title='base', editable=True, allowsSorting=True),
                    dict(title='mark', editable=True, allowsSorting=True),
                    dict(title='anchor', editable=True, allowsSorting=True),
                ],
            )

        y += textBoxHeight + p
        self.w.addEntry = SquareButton(
                (x, y, -p, self.buttonHeight),
                'add new entry',
                callback=self.addNewEntryCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.selectAllMarks = CheckBox(
                (x, y, -p, self.textHeight),
                'select all',
                value=False,
                callback=self.selectAllMarksCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.exportMarks = SquareButton(
                (x, y, -p, self.buttonHeight),
                'export list to file…',
                callback=self.exportMarksCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.makeMarksFeature = SquareButton(
                (x, y, -p, self.buttonHeight),
                "make mark feature",
                callback=self.createMarkFeatureCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.w.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                'preflight',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.appendFeature = CheckBox(
                (x, y, -p, self.textHeight),
                'append feature',
                value=False,
                sizeStyle=self.sizeStyle)

        self.w.open()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def allMarks(self):
        marksList = []
        for entry in self.w.marksList.get():
            marksList.append((entry['base'], entry['mark'], entry['anchor']))
        return marksList

    @property
    def selectedMarks(self):
        selection = self.w.marksList.getSelection()
        marksList = []
        for i, mark in enumerate(self.allMarks):
            if i in selection:
                marksList.append(mark)
        return marksList

    # ---------
    # callbacks
    # ---------

    def selectAllMarksCallback(self, sender):
        if sender.get():
            selection = list(range(len(self.w.marksList)))
        else:
            selection = []
        self.w.marksList.setSelection(selection)

    def addNewEntryCallback(self, sender):
        print('adding new entry…\n')
        entry = {'base': '...', 'mark': '...', 'anchor': '...'}
        self.w.marksList.append(entry)

    def importMarksCallback(self, sener):
        msg = 'import marks from .txt file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['txt'])
        if not filePath:
            print('no txt file selected.\n')
            return
        self.importMarks(filePath)

    def exportMarksCallback(self, sender):
        msg = 'export marks to .txt file'
        filePath = PutFile(message=msg, fileName='marks.txt')
        if filePath:
            self.exportMarks(filePath)

    def createMarkFeatureCallback(self, sender):

        font = self.getCurrentFont()
        if not font:
            return

        preflight     = self.w.preflight.get()
        appendFeature = self.w.appendFeature.get()

        if not len(self.selectedMarks):
            print('no mark selected.\n')
            return

        markToBaseDict = markToBaseList2Dict(self.selectedMarks)
        M = markToBaseFeaBuilder(font, markToBaseDict)

        if preflight:
            M.verbose = True
            M.buildDicts()
            print()

        else:
            M.verbose = False
            fea = M.compile()
            print(fea)
            print()

            if appendFeature:
                if not font.features.text:
                    font.features.text = fea
                else:
                    font.features.text += '\n%s' % fea

    # -------
    # methods
    # -------

    def importMarks(self, filePath):
        print('importing marks from file…')
        # read marks data from txt file
        with open(filePath, 'r') as inputFile:
            entries = []
            for L in inputFile.readlines():
                try:
                    base, mark, anchor = L.strip().split()
                except:
                    continue
                entry = {'base': base, 'mark': mark, 'anchor': anchor}
                entries.append(entry)
        # set marks data in the UI
        self.w.marksList.set(entries)
        # done
        print('…done.\n')

    def exportMarks(self, filePath):
        print('exporting mark data to file…')
        txt = ''
        for base, mark, anchor in self.allMarks:
            txt += '%s %s %s\n' % (base, mark, anchor)
        # save marks to txt file
        with open(filePath, 'w') as outputFile:
            outputFile.write(txt)
        # done
        print('…done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    MakeMarkFeatureDialog()
