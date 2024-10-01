from importlib import reload
import hTools3.dialogs.batch.base
reload(hTools3.dialogs.batch.base)

import os
import json
import plistlib
from vanilla import Group, Button, List, CheckBox, EditText
from mojo.UI import AccordionView, PutFile, GetFile
from hTools3.modules.fontinfo import FontInfoAttributes, FontInfoAttributesIgnorePrefix
from hTools3.modules.fontutils import getFontID
from hTools3.modules.unicode import unicodeHexToInt, unicodeIntToHex, clearUnicodes, autoUnicode
from hTools3.dialogs.batch.base import BatchDialogBase


class BatchSetDialog(BatchDialogBase):

    '''
    A dialog to set several types of data in selected target fonts.

    ::

        from hTools3.dialogs.batch.set import BatchSetDialog
        BatchSetDialog()

    '''

    title = 'batch set'
    key = '%s.set' % BatchDialogBase.key

    fontInfo = dict(FontInfoAttributes)
    del fontInfo['WOFF']
    del fontInfo['Miscellaneous']

    attrsIgnorePrefix = FontInfoAttributesIgnorePrefix

    fontInfoData = {}
    unicodesData = {}

    def __init__(self):
        self.height = 480
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, 360))

        # build groups
        self.initFontSelectorGroup()
        self.initFontInfoSelectorGroup()
        self.initGlyphSetSelectorGroup()
        self.initUnicodesSelectorGroup()
        # self.initFindAndReplaceSelectorGroup()

        # build accordion
        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="font info",
                view=self.fontInfoSelector,
                size=self.fontInfoSelectorHeight,
                collapsed=True,
                canResize=True),
            dict(label="glyph set",
                view=self.glyphSetSelector,
                size=self.glyphSetSelectorHeight,
                collapsed=True,
                canResize=True),
            dict(label="unicodes",
                view=self.unicodesSelector,
                size=self.unicodesSelectorHeight,
                collapsed=True,
                canResize=True),
            # dict(label="find & replace",
            #     view=self.findAndReplaceSelector,
            #     size=self.findAndReplaceSelectorHeight,
            #     collapsed=True,
            #     canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
        # self.w.open()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initFontInfoSelectorGroup(self):
        '''
        Initialize fontInfo group.

        '''
        self.fontInfoSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.fontInfoSelector.importFontInfoFromFont = Button(
                (x, y, -p, self.textHeight),
                "import info from UFO…",
                callback=self.importFontInfoFromFontCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.fontInfoSelector.importFontInfoDict = Button(
                (x, y, -p, self.textHeight),
                "import info from json file…",
                callback=self.importFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        listHeight = -(self.textHeight + p) * 2 - (self.textHeight + p) * 2 - p
        self.fontInfoSelector.fontInfo = List(
                (x, y, -p, listHeight),
                [],
                enableDelete=True,
                drawFocusRing=False,
                editCallback=self.fontInfoDeletedCallback,
                columnDescriptions=[
                    dict(title="attribute"),
                    dict(title="value", editable=True, allowsSorting=True),
                ])

        y = -(self.textHeight + p) * 2 - (self.textHeight + p) * 2
        self.fontInfoSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                "select all attributes",
                callback=self.selectAllFontInfoAttributes,
                value=False,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2 - (self.textHeight + p)
        self.fontInfoSelector.exportFontInfoDict = Button(
                (x, y, -p, self.textHeight),
                "export info to json file…",
                callback=self.exportFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) - (self.textHeight + p)
        self.fontInfoSelector.applyFontInfoButton = Button(
                (x, y, -p, self.textHeight),
                "apply selected info",
                callback=self.applyFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.fontInfoSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        self.fontInfoSelectorHeight = 340

    def initGlyphSetSelectorGroup(self):
        '''
        Initialize glyphSet group.

        '''
        self.glyphSetSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.glyphSetSelector.importGlyphSet = Button(
                (x, y, -p, self.textHeight),
                "import glyph set…",
                callback=self.importGlyphSetCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        listHeight = -(self.textHeight + p) * 2 - (self.textHeight + p) * 3
        self.glyphSetSelector.glyphNames = EditText(
                (x, y, -p, listHeight),
                '')

        y = -(self.textHeight + p) * 2 - (self.textHeight + p) * 3 + p
        self.glyphSetSelector.exportGlyphSet = Button(
                (x, y, -p, self.textHeight),
                "export glyph set…",
                callback=self.exportGlyphSetCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) - (self.textHeight + p) * 3 + p
        self.glyphSetSelector.createMissingGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "create missing glyphs",
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) - (self.textHeight + p) * 2
        self.glyphSetSelector.deleteRemainingGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "delete remaining glyphs",
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) - (self.textHeight + p)
        self.glyphSetSelector.applyGlyphSet = Button(
                (x, y, -p, self.textHeight),
                "apply glyph set",
                callback=self.applyGlyphSetCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.glyphSetSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        self.glyphSetSelectorHeight = 320

    def initUnicodesSelectorGroup(self):
        '''
        Initialize unicodes group.

        '''
        self.unicodesSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.unicodesSelector.importExtraUnicodes = Button(
                (x, y, -p, self.textHeight),
                "import extra unicodes…",
                callback=self.importUnicodesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        listHeight = -(self.textHeight + p) * 4
        self.unicodesSelector.unicodes = List(
                (x, y, -p, listHeight),
                [],
                drawFocusRing=False,
                columnDescriptions=[
                    dict(title="glyph name",  editable=False, allowsSorting=True),
                    dict(title="unicode hex", editable=False, allowsSorting=True),
                    dict(title="unicode int", editable=False, allowsSorting=True),
                ])

        y = -(self.textHeight + p) * 4 + p
        self.unicodesSelector.selectAllUnicodes = CheckBox(
                (x, y, -p, self.textHeight),
                "select all unicodes",
                callback=self.selectAllUnicodesCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 3
        self.unicodesSelector.clearUnicodes = CheckBox(
                (x, y, -p, self.textHeight),
                "clear existing unicodes",
                value=True,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2
        self.unicodesSelector.applyUnicodesButton = Button(
                (x, y, -p, self.textHeight),
                "set unicodes…",
                callback=self.applyUnicodesCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.unicodesSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        self.unicodesSelectorHeight = 320

    def initFindAndReplaceSelectorGroup(self):
        '''
        Initialize findAndReplace group.

        '''
        self.findAndReplaceSelector = Group((0, 0, -0, -0))
        self.findAndReplaceSelectorHeight = 100

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedFontInfoSection(self):
        '''
        Get selected font info section.

        '''
        i = self.fontInfoSelector.sections.get()
        section = self.fontInfoSelector.sections.getItems()[i]
        return section

    @property
    def selectedFontInfoSubSection(self):
        '''
        Get selected font info subsection.

        '''
        i = self.fontInfoSelector.subSections.get()
        subsection = self.fontInfoSelector.subSections.getItems()[i]
        return subsection

    @property
    def selectedFontInfoAttribute(self):
        '''
        Get selected font info attribute.

        '''
        i = self.fontInfoSelector.subSectionAttributes.get()
        attribute = self.fontInfoSelector.subSectionAttributes.getItems()[i]
        return attribute

    @property
    def selectedFontInfoDataAsDict(self):
        '''
        Get selected font info attributes and data as a dict.

        '''
        fontInfoDict = {}
        for i in self.fontInfoSelector.fontInfo.getSelection():
            entry = self.fontInfoSelector.fontInfo.get()[i]
            attr = entry['attribute']
            fontInfoDict[attr] = self.fontInfoData[attr]
        return fontInfoDict

    @property
    def selectedUnicodes(self):
        '''
        Get selected unicodes.

        '''
        selection = self.unicodesSelector.unicodes.getSelection()
        unicodes  = self.unicodesSelector.unicodes.get()
        uniDict = {}
        for i, L in enumerate(unicodes):
            if i in selection:
                glyphName = L['glyph name']
                uniInt = int(L['unicode int'])
                uniDict[glyphName] = uniInt
        return uniDict

    # ---------
    # callbacks
    # ---------

    def importFontInfoCallback(self, sender):
        msg = 'import font info data from .json file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['json'])
        if not filePath:
            print('no json file selected.\n')
            return
        self.importFontInfo(filePath)

    def importFontInfoFromFontCallback(self, sender):
        msg = 'import font info data from .ufo file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['ufo'])
        if not filePath:
            print('no ufo file selected.\n')
            return
        self.importFontInfoFromFont(filePath)

    def selectAllFontInfoAttributes(self, sender):
        if sender.get():
            selection = list(range(len(self.fontInfoSelector.fontInfo)))
        else:
            selection = []
        self.fontInfoSelector.fontInfo.setSelection(selection)

    def exportFontInfoCallback(self, sender):
        msg = 'export font info data to json format'
        filePath = PutFile(message=msg, fileName='fontinfo.json')
        if filePath:
            self.exportFontInfo(filePath)

    def applyFontInfoCallback(self, sender):
        preflight = self.fontInfoSelector.preflight.get()
        if preflight:
            self.preflight(fontInfo=True)
        else:
            self.batchSetFontInfo()

    def importGlyphSetCallback(self, sender):
        msg = 'import glyph order from .enc file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['enc', 'txt'])
        if not filePath:
            print('no encoding file selected.\n')
            return
        self.importGlyphSet(filePath)

    def exportGlyphSetCallback(self, sender):
        msg = 'export glyph set to .enc file'
        filePath = PutFile(message=msg, fileName='encoding.enc')
        if filePath:
            self.exportGlyphSet(filePath)

    def applyGlyphSetCallback(self, sender):
        preflight = self.glyphSetSelector.preflight.get()
        if preflight:
            self.preflight(glyphOrder=True)
        else:
            self.batchSetGlyphOrder()

    def fontInfoDeletedCallback(self, sender):
        fontInfoAttrs   = set(self.fontInfoData.keys())
        fontInfoAttrsUI = set([entry['attribute'] for entry in self.fontInfoSelector.fontInfo.get()])
        deletedAttrs = fontInfoAttrs.difference(fontInfoAttrsUI)
        if len(deletedAttrs):
            print('deleting font info attributes...\n')
            for attr in deletedAttrs:
                print('\t- %s' % attr)
                del self.fontInfoData[attr]
            print('\n...done.\n')

    def importUnicodesCallback(self, sender):
        msg = 'import unicodes from .uni file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['uni'])
        if not filePath:
            print('no unicodes file selected.\n')
            return
        self.importUnicodes(filePath)

    def selectAllUnicodesCallback(self, sender):
        if sender.get():
            selection = list(range(len(self.unicodesSelector.unicodes)))
        else:
            selection = []
        self.unicodesSelector.unicodes.setSelection(selection)

    def applyUnicodesCallback(self, sender):
        preflight = self.unicodesSelector.preflight.get()
        if preflight:
            self.preflight(unicodes=True)
        else:
            self.batchSetUnicodes()

    # -------
    # methods
    # -------

    def loadFontInfoDict(self, fontInfoDict):
        '''
        Load font info data from dictionary into the UI.

        '''
        fontInfoDictItems = []
        for attr, value in fontInfoDict.items():
            D = { "attribute" : attr , "value" : str(value) }
            fontInfoDictItems.append(D)
        self.fontInfoSelector.fontInfo.set(fontInfoDictItems)

    def loadUnicodesDict(self, unicodesDict):
        '''
        Load unicode data from dictionary into the UI.

        '''
        unicodeDictItems = []
        for uniHex, glyphName in unicodesDict.items():
            uniInt = unicodeHexToInt(uniHex)
            D = {
                "glyph name"  : glyphName ,
                "unicode hex" : str(uniHex),
                "unicode int" : str(uniInt),
            }
            unicodeDictItems.append(D)
        self.unicodesSelector.unicodes.set(unicodeDictItems)

    def importFontInfo(self, jsonPath):
        '''
        Import font info data to from json file to internal dictionary.

        '''
        print('importing font info from file…')
        # read font info from json
        with open(jsonPath, 'r', encoding='utf-8') as inputFile:
            self.fontInfoData = json.load(inputFile)
        # load font info dict into UI
        self.loadFontInfoDict(self.fontInfoData)
        # done
        print('…done.\n')

    def exportFontInfo(self, filePath):
        '''
        Export font info data to from internal dictionary to json file.

        '''
        print('exporting font info to file…')
        # save font info to json
        with open(filePath, 'w', encoding='utf-8') as outputFile:
            json.dump(self.fontInfoData, outputFile, indent=2)
        # done
        print('…done.\n')

    def importFontInfoFromFont(self, ufoPath):
        '''
        Import font info data to from a UFO font file.

        '''
        # import data from fontinfo.plist
        infoPlistPath = os.path.join(ufoPath, 'fontinfo.plist')
        with open(infoPlistPath, 'rb') as f:
            fontInfo = plistlib.load(f)
        # ignore guidelines
        if 'guidelines' in fontInfo:
            del fontInfo['guidelines']
        # update UI
        self.fontInfoData = fontInfo
        self.loadFontInfoDict(self.fontInfoData)

    def importGlyphSet(self, filePath):
        '''
        Import glyph set from encoding file.

        '''
        print('importing glyph order from file…')
        # read glyph order from file
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            glyphSetRaw = inputFile.readlines()
        # ignore lines starting with %
        glyphOrder = [L.strip() for L in glyphSetRaw if not L.startswith('%')]
        # update UI
        self.glyphSetSelector.glyphNames.set(' '.join(glyphOrder))
        # done
        print('…done.\n')

    def exportGlyphSet(self, filePath):
        '''
        Export glyph set to encoding file.

        '''
        print('exporting glyph set to .enc file…')
        # save glyph set to file
        glyphSetRaw = self.glyphSetSelector.glyphNames.get()
        if not len(glyphSetRaw):
            print('glyph set is empty.\n')
            return
        glyphSet = glyphSetRaw.replace(' ', '\n')
        with open(filePath, 'w', encoding='utf-8') as outputFile:
            outputFile.write(glyphSet)
        # done
        print('…done.\n')

    def importUnicodes(self, filePath):
        '''
        Import glyph names and unicodes from text file.

        '''
        print('importing unicodes from file…')
        # read unicode from file
        unicodesData = {}
        with open(filePath, 'r', encoding='utf-8', errors='replace') as inputFile:
            for L in inputFile.readlines():
                if not len(L.split()) == 2:
                    continue
                glyphName, uni = L.split()
                unicodesData[glyphName] = uni
        # store unicodes dict
        self.unicodesData = unicodesData
        # update UI
        self.loadUnicodesDict(self.unicodesData)
        # done
        print('…done.\n')

    def preflightFontInfo(self):
        '''
        Preflight selected font info data.

        '''
        print('font info data:')
        if len(self.selectedFontInfoDataAsDict):
            for attr, value in self.selectedFontInfoDataAsDict.items():
                print('- %s: %s' % (attr, value))
        # no font info selected
        else:
            print('- [None]')
        print()

    def preflightGlyphSet(self):
        '''
        Preflight glyph set & order.

        '''
        createMissingGlyphs   = self.glyphSetSelector.createMissingGlyphs.get()
        deleteRemainingGlyphs = self.glyphSetSelector.deleteRemainingGlyphs.get()
        if createMissingGlyphs or deleteRemainingGlyphs:
            print('glyph set & order:')
            if createMissingGlyphs:
                print('- create missing glyphs')
            if deleteRemainingGlyphs:
                print('- delete remaining glyphs')
            print()

    def preflightUnicodes(self):
        '''
        Preflight unicodes.

        '''
        _clearUnicodes = self.unicodesSelector.clearUnicodes.get()
        if _clearUnicodes:
            print('unicode options:')
            print('- clear unicodes')
            print()

        print('custom unicodes:')
        selectedUnicodes = self.selectedUnicodes
        if len(selectedUnicodes):
            w = max([len(k) for k in selectedUnicodes.keys()])
            for glyphName, uniInt in selectedUnicodes.items():
                uniInt = int(uniInt)
                uniHex = unicodeIntToHex(uniInt)
                print('- %s: %s (%s)' % (glyphName.ljust(w+1), uniHex, uniInt))
        # no unicode selected
        else:
            print('- [None]')
        print()

    def preflight(self, fontInfo=False, glyphOrder=False, unicodes=False):
        '''
        Print information about the batch operation before actually executing it.

        '''
        self.preflightTargetFonts()

        if fontInfo:
            self.preflightFontInfo()

        if glyphOrder:
            self.preflightGlyphSet()

        if unicodes:
            self.preflightUnicodes()

    def batchSetFontInfo(self):
        '''
        Batch set font info in all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # no font info entries selected
        fontInfoDict = self.selectedFontInfoDataAsDict
        if not len(fontInfoDict):
            print('no font info attributes selected.\n')
            return

        # -------------------
        # batch set font info
        # -------------------

        print('batch setting font info...\n')
        for targetFontName, targetFont in targetFonts:
            print("\tsetting font info in font '%s'..." % targetFontName)
            for attr, value in fontInfoDict.items():
                setattr(targetFont.info, attr, value)

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

    def batchSetGlyphOrder(self):
        '''
        Batch set glyph order in all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # ---------------------
        # batch set glyph order
        # ---------------------

        # get options
        createMissingGlyphs   = self.glyphSetSelector.createMissingGlyphs.get()
        deleteRemainingGlyphs = self.glyphSetSelector.deleteRemainingGlyphs.get()

        print('batch setting glyph order...\n')
        for targetFontName, targetFont in targetFonts:
            glyphOrderSrc = self.glyphSetSelector.glyphNames.get()
            glyphOrder = glyphOrderSrc.split()
            print("\tsetting glyph order in font '%s'..." % targetFontName)

            # create missing glyphs
            if createMissingGlyphs:
                missingGlyphs = set(glyphOrder).difference(set(targetFont.keys()))
                print("\tcreating missing glyphs...")
                for glyphName in missingGlyphs:
                    targetFont.newGlyph(glyphName)

            # delete remaining glyphs
            if deleteRemainingGlyphs:
                print("\tdeleting remaining glyphs...")
                remainingGlyphs = set(targetFont.keys()).difference(set(glyphOrder))
                for glyphName in remainingGlyphs:
                    targetFont.removeGlyph(glyphName)

            # set glyph order
            targetFont.glyphOrder = glyphOrder

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

    def batchSetUnicodes(self):
        '''
        Batch set unicodes in all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # ------------------
        # batch set unicodes
        # ------------------

        # get options
        selectedUnicodes = self.selectedUnicodes
        _clearUnicodes = self.unicodesSelector.clearUnicodes.get()

        print('batch setting unicodes...\n')
        for targetFontName, targetFont in targetFonts:

            # clear unicodes
            if _clearUnicodes:
                print("\tremoving all unicodes in font '%s'..." % targetFontName)
                clearUnicodes(targetFont)
                print()

            # set unicodes
            print("\tsetting unicodes in font '%s'...\n" % targetFontName)
            for glyphName in targetFont.keys():
                g = targetFont[glyphName]
                autoUnicode(g, customUnicodes=selectedUnicodes, verbose=True, indent=2)

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

# -------
# testing
# -------

if __name__ == '__main__':

    BatchSetDialog()
