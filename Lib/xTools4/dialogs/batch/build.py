from importlib import reload
import xTools4.dialogs.batch.base
reload(xTools4.dialogs.batch.base)

from vanilla import Group, EditText, CheckBox, ColorWell, Button, List
from mojo.UI import AccordionView, PutFile, GetFile, CodeEditor
from mojo.roboFont import CurrentFont
from glyphConstruction import ParseGlyphConstructionListFromString
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.accents import buildGlyphConstructions
from xTools4.modules.messages import *
from xTools4.dialogs.batch.base import BatchDialogBase


KEY = f'{BatchDialogBase.key}.buildGlyphs'


class BatchBuildGlyphsDialog(BatchDialogBase):

    '''
    A dialog to build new glyphs in batch in selected fonts.

    ::

        from xTools4.dialogs.batch.build import BatchBuildDialog
        BatchBuildDialog()

    '''

    title = 'batch build glyphs'
    key   = KEY

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, self.height))

        # build groups
        self.initFontSelectorGroup()
        self.initNewGlyphsGroup()
        self.initGlyphConstructionGroup()
        self.initDuplicateRenameGroup()

        # build accordion
        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="new",
                view=self.newGlyphs,
                size=self.newGlyphsHeight,
                collapsed=True,
                canResize=True),
            dict(label="constructions",
                view=self.glyphConstructions,
                size=self.glyphConstructionsHeight,
                collapsed=True,
                canResize=True),
            dict(label="duplicates",
                view=self.duplicateRenameSelector,
                size=self.duplicateRenameSelectorHeight,
                collapsed=True,
                canResize=True),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initNewGlyphsGroup(self):
        '''
        Initialize newGlyphs group.

        '''
        self.newGlyphs = Group((0, 0, -0, -0))

        x = y = p = self.padding
        textBoxHeight = -(self.textHeight + p) * 2 - p
        self.newGlyphs.glyphNames = EditText(
                (x, y, -p, textBoxHeight),
                '')

        y = -(self.textHeight + p) * 2
        self.newGlyphs.applyButton = Button(
                (x, y, -p, self.textHeight),
                "batch make glyphs",
                callback=self.batchMakeNewGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.newGlyphs.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        self.newGlyphsHeight = self.textHeight * 6 + p * 4

    def initGlyphConstructionGroup(self):
        '''
        Initialize glyphConstructions group.

        '''
        self.glyphConstructions = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.glyphConstructions.importGlyphConstructions = Button(
                (x, y, -p, self.textHeight),
                "import constructions…",
                callback=self.importGlyphConstructionsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        textBoxHeight = -(self.textHeight + p)*6
        self.glyphConstructions.glyphConstructions = CodeEditor(
                (x, y, -p, textBoxHeight),
                '',
                showLineNumbers=False)

        y = -(self.textHeight + p) * 6 + p
        self.glyphConstructions.exportGlyphConstructions = Button(
                (x, y, -p, self.textHeight),
                "export constructions…",
                callback=self.exportGlyphConstructionsCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 5 + p
        self.glyphConstructions.selectGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "select glyphs",
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2 - (self.textHeight + p) * 2
        self.glyphConstructions.markGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "mark glyphs",
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 3
        nsColor = rgb2nscolor((1, 0, 0, 0.5))
        self.glyphConstructions.markColor = ColorWell(
                (x, y, -self.padding, self.textHeight),
                color=nsColor)

        y = -(self.textHeight + p) * 2
        self.glyphConstructions.applyButton = Button(
                (x, y, -p, self.textHeight),
                "batch build constructions",
                callback=self.batchBuildGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.glyphConstructions.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        self.glyphConstructionsHeight = 320

    def initDuplicateRenameGroup(self):

        self.duplicateRenameSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.duplicateRenameSelector.addSelectionToList = Button(
                (x, y, -p, self.textHeight),
                'add current font selection',
                callback=self.addSelectionToListCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.duplicateRenameSelector.importGlyphNames = Button(
                (x, y, -p, self.textHeight),
                'import glyph names from file…',
                callback=self.importGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        textBoxHeight = self.textHeight * 8
        self.duplicateRenameSelector.glyphNames = List(
                (x, y, -p, textBoxHeight),
                [],
                enableDelete=True,
                drawFocusRing=False,
                columnDescriptions=[
                    dict(title='source',  editable=True, allowsSorting=True),
                    dict(title='target',  editable=True, allowsSorting=True),
                ],
            )

        y += textBoxHeight + p
        self.duplicateRenameSelector.addEntry = Button(
                (x, y, -p, self.textHeight),
                'add new entry',
                callback=self.addNewEntryCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.duplicateRenameSelector.selectAllGlyphNames = CheckBox(
                (x, y, -p, self.textHeight),
                'select all',
                value=False,
                callback=self.selectAllGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.duplicateRenameSelector.exportGlyphNames = Button(
                (x, y, -p, self.textHeight),
                'export glyph names to file…',
                callback=self.exportGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.duplicateRenameSelector.overwrite = CheckBox(
                (x, y, -p, self.textHeight),
                'overwrite existing glyphs',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.duplicateRenameSelector.markGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                'mark duplicates',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        nsColor = rgb2nscolor((0, 0.5, 1, 0.5))
        self.duplicateRenameSelector.markColor = ColorWell(
                (x, y, -p, self.textHeight),
                color=nsColor)

        y += self.textHeight + p
        self.duplicateRenameSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "batch build duplicates",
                callback=self.duplicateRenameCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.duplicateRenameSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                'preflight',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.duplicateRenameSelectorHeight = y

    # -------------
    # dynamic attrs
    # -------------

    # duplicate rename

    @property
    def allGlyphNames(self):
        glyphNames = []
        for entry in self.duplicateRenameSelector.glyphNames.get():
            glyphNames.append((entry['source'], entry['target']))
        return glyphNames

    @property
    def selectedGlyphNames(self):
        selection = self.duplicateRenameSelector.glyphNames.getSelection()
        glyphNames = []
        for i, glyphName in enumerate(self.allGlyphNames):
            if i in selection:
                glyphNames.append(glyphName)
        return glyphNames

    @property
    def overwrite(self):
        return bool(self.duplicateRenameSelector.overwrite.get())

    @property
    def markGlyphs(self):
        return bool(self.duplicateRenameSelector.markGlyphs.get())

    @property
    def markColor(self):
        return nscolor2rgb(self.duplicateRenameSelector.markColor.get())

    # ---------
    # callbacks
    # ---------

    # new glyphs

    def batchMakeNewGlyphsCallback(self, sender):
        preflight = self.newGlyphs.preflight.get()
        if preflight:
            self.preflight(newGlyphs=True)
        else:
            self.batchMakeNewGlyphs()

    # glyph construction

    def importGlyphConstructionsCallback(self, sender):
        msg = 'import glyph constructions from file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['glyphConstruction', 'txt'])
        if not filePath:
            print('no glyph construction file selected.\n')
            return
        self.importGlyphConstructions(filePath)

    def exportGlyphConstructionsCallback(self, sender):
        msg = 'export glyph constructions to file'
        filePath = PutFile(message=msg, fileName='constructions.glyphConstruction')
        if filePath:
            self.exportGlyphConstructions(filePath)

    def batchBuildGlyphsCallback(self, sender):
        preflight = self.glyphConstructions.preflight.get()
        if preflight:
            self.preflight(buildGlyphs=True)
        else:
            self.batchBuildGlyphs()

    # duplicate rename

    def addSelectionToListCallback(self, sender):
        f = CurrentFont()
        if not f:
            print(noFontOpen)
            return

        glyphNames = f.selectedGlyphNames
        if not len(glyphNames):
            print(noGlyphSelected)
            return

        entries = []
        for glyphName in glyphNames:
            entry = {'source': glyphName, 'target': '...'}
            entries.append(entry)

        self.duplicateRenameSelector.glyphNames.extend(entries)

    def selectAllGlyphNamesCallback(self, sender):
        if sender.get():
            selection = list(range(len(self.duplicateRenameSelector.glyphNames)))
        else:
            selection = []
        self.duplicateRenameSelector.glyphNames.setSelection(selection)

    def addNewEntryCallback(self, sender):
        print('adding new entry…\n')
        entry = {
            'source' : '...',
            'target' : '...',
        }
        self.duplicateRenameSelector.glyphNames.append(entry)

    def importGlyphNamesCallback(self, sender):
        msg = 'import glyph names from .txt file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['txt'])
        if not filePath:
            print('no .txt file selected.\n')
            return
        self.importGlyphNames(filePath)

    def exportGlyphNamesCallback(self, sender):
        msg = 'export glyph names to .txt file'
        filePath = PutFile(message=msg, fileName='duplicates.txt')
        if filePath:
            self.exportGlyphNames(filePath)

    def duplicateRenameCallback(self, sender):
        if self.duplicateRenameSelector.preflight.get():
            self.preflight(duplicateRename=True)
        else:
            self.batchDuplicateRenameGlyphs()

    # -------
    # methods
    # -------

    # glyph construction

    def importGlyphConstructions(self, filePath):
        '''
        Import glyph constructions from a .glyphConstruction file.

        '''
        print('importing glyph constructions from file…')

        # read glyph constructions from file
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            constructions = inputFile.read()

        # update UI
        self.glyphConstructions.glyphConstructions.set(constructions)

        # done
        print('…done.\n')

    def exportGlyphConstructions(self, filePath):
        '''
        Export glyph constructions to a .glyphConstruction file.

        '''
        print('exporting glyph constructions to file…')

        # save glyph constructions to file
        constructions = self.glyphConstructions.glyphConstructions.get()
        if not len(constructions):
            print('glyph constructions are empty.\n')
            return

        with open(filePath, 'w', encoding='utf-8') as outputFile:
            outputFile.write(constructions)

        # done
        print('…done.\n')

    # duplicate rename

    def importGlyphNames(self, filePath):
        print('importing glyph names from file…')
        # read glyph names from txt file
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            entries = []
            for L in inputFile.readlines():
                try:
                    source, target = L.strip().split()
                except:
                    continue
                entry = {
                    'source' : source,
                    'target' : target,
                }
                entries.append(entry)
        # set glyph names in the UI
        self.duplicateRenameSelector.glyphNames.set(entries)
        # done
        print('…done.\n')

    def exportGlyphNames(self, filePath):
        print('exporting glyph names to file…')
        # collect source/target glyph names
        txt = ''
        for source, target in self.allGlyphNames:
            txt += '%s %s\n' % (source, target)
        # save glyph names to txt file
        with open(filePath, 'w', encoding='utf-8') as outputFile:
            outputFile.write(txt)
        # done
        print('…done.\n')

    # preflight

    def preflightNewGlyphs(self):
        '''
        Preflight settings for new glyphs.

        '''
        print('new glyphs:')
        glyphNames = self.newGlyphs.glyphNames.get().strip()
        glyphNames = glyphNames.split(' ')
        print('- %s' % ' '.join(glyphNames))
        print()

    def preflightGlyphConstructions(self):
        '''
        Preflight glyph constructions settings.

        '''
        # print constructions data
        print('constructions:')
        constructionsRaw = self.glyphConstructions.glyphConstructions.get()
        constructions = ParseGlyphConstructionListFromString(constructionsRaw)
        if len(constructions):
            for construction in constructions:
                try:
                    glyphName = construction.split('=')[0].strip()
                    print('- %s' % glyphName)
                except:
                    continue
        else:
            print('- [None]')
        print()

        # print options
        selectGlyphs = self.glyphConstructions.selectGlyphs.get()
        markGlyphs   = self.glyphConstructions.markGlyphs.get()
        print('options:')
        if not selectGlyphs and not markGlyphs:
            print('- [None]')
        if selectGlyphs:
            print('- select glyphs')
        if markGlyphs:
            print('- mark glyphs')
        print()

    def preflightDuplicateRename(self):
        # print glyph names
        print('duplicate glyphs:')
        if len(self.selectedGlyphNames):
            for source, target in self.selectedGlyphNames:
                print('- %s -> %s' % (source, target))
        else:
            print('- [None]')
        print()

        # print options
        print('options:')
        if any([self.overwrite, self.markGlyphs]):
            if self.overwrite:
                print('- overwrite existing glyphs')
            if self.markGlyphs:
                print('- mark duplicates')
        else:
            print('- [None]')

        # done
        print()

    def preflight(self, newGlyphs=False, buildGlyphs=False, duplicateRename=False):
        '''
        Print information about the batch operation before actually executing it.

        '''
        self.preflightTargetFonts()

        if newGlyphs:
            self.preflightNewGlyphs()

        if buildGlyphs:
            self.preflightGlyphConstructions()

        if duplicateRename:
            self.preflightDuplicateRename()

    # batch process

    def batchMakeNewGlyphs(self):
        '''
        Build new empty glyphs in all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # get glyph names
        glyphNames = self.newGlyphs.glyphNames.get().strip()
        if not len(glyphNames):
            print('no glyph names.\n')
            return

        # -----------------
        # batch make glyphs
        # -----------------

        glyphNames = glyphNames.split(' ')

        print('batch creating new empty glyphs...\n')

        for targetFontName, targetFont in targetFonts:

            # make glyphs
            print('\tcreating empty glyphs in %s...' % targetFontName)

            for glyphName in glyphNames:
                targetFont.newGlyph(glyphName)

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\tsaving %s...' % targetFontName)
                targetFont.save()
                targetFont.close()
            else:
                targetFont.changed()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchBuildGlyphs(self):
        '''
        Build glyphs from glyph constructions in all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # get glyph constructions
        constructions = self.glyphConstructions.glyphConstructions.get()
        if not len(constructions):
            print('no glyph constructions.\n')
            return

        # ------------------
        # batch build glyphs
        # ------------------

        selectGlyphs = self.glyphConstructions.selectGlyphs.get()

        # get color
        markColor = None
        if self.glyphConstructions.markGlyphs.get():
            nsColor = self.glyphConstructions.markColor.get()
            markColor = nscolor2rgb(nsColor)

        print('batch building glyphs...\n')

        for targetFontName, targetFont in targetFonts:

            # build glyphs
            print('\tbuilding glyphs in %s...\n' % targetFontName)
            builtGlyphs = buildGlyphConstructions(targetFont, constructions, verbose=True, indentLevel=2, markColor=markColor)

            # select glyphs
            if selectGlyphs:
                targetFont.selectedGlyphNames = builtGlyphs

            # save fonts without UI
            if not targetFont.hasInterface():
                print()
                print('\tsaving %s...' % targetFontName)
                targetFont.save()
                targetFont.close()
            else:
                targetFont.changed()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchDuplicateRenameGlyphs(self):
        '''
        Batch duplicate & rename glyphs.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # get src/dst glyph names
        glyphNames = self.selectedGlyphNames
        if not len(glyphNames):
            print('no glyph names selected.\n')
            return

        # -------------------------------
        # batch duplicate & rename glyphs
        # -------------------------------

        print('batch duplicating glyphs...\n')

        # get target fonts
        for fontName, font in targetFonts:
            print("\tduplicating glyphs in '%s'...\n" % fontName)

            # get source & target glyph names
            for srcName, dstName in glyphNames:
                print("\t\tduplicating '%s' as '%s'..." % (srcName, dstName))
                # create target glyph
                if dstName not in font:
                    font.newGlyph(dstName)

                if self.overwrite:
                    font[dstName] = font[srcName]
                else:
                    # copy duplicate into existing glyph
                    font[dstName].appendGlyph(font[srcName])

                font[dstName].unicodes = []

                # mark target glyph
                if self.markGlyphs:
                    font[dstName].markColor = self.markColor

            # save fonts without UI
            if not font.hasInterface():
                print('\n\t\tsaving font...')
                font.save()
                font.close()

            # done with font
            print()

        # done
        print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    BatchBuildGlyphsDialog()
