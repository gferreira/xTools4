from vanilla import *
from mojo.UI import AccordionView
from xTools4.dialogs.batch.base import BatchDialogBase


class BatchGenerateDialog(BatchDialogBase):

    title = 'batch generate'

    settings = {
        'suffix'        : '%Y%m%d-%H%M%S',
        'versionString' : '{openTypeOS2VendorID} : {familyName} {styleName} {versionMajor}.{versionMinor}',
    }

    optionsCFF = [
        'decompose',
        'remove overlaps',
        'autohint (PS)',
    ]

    optionsTTF = [
        'decompose',
        'remove overlaps',
        'autohint (TT)',
    ]

    ttfautohintOptions = {
        'hintSetRangeMin'        : 8,
        'hintSetRangeMax'        : 50,
        'hintingLimit'           : 200,
        'noHintingLimit'         : False,
        'xHeightIncreaseLimit'   : 14,
        'noXHeightIncreaseLimit' : False,
        'fallbackScriptLatin'    : False,
        'preHinted'              : False,
        'symbolFont'             : False,
        'ttfautohintInfo'        : False,
        'overrideLicense'        : False,
        'grayscale'              : False,
        'clearTypeGDI'           : False,
        'clearTypeDW'            : False,
    }

    formatsGenerate = ['OTF', 'TTF', 'WOFF', 'WOFF2']

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 2, self.height),
                self.title,
                minSize=(self.width * 2, self.height))

        # build groups

        self.initFontSelectorGroup()
        self.initCFFSelectorGroup()
        self.initTTFSelectorGroup()
        self.initWOFFSelectorGroup()
        self.initGenerateFontsGroup()

        # build accordion

        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="OTF",
                view=self.CFFSelector,
                size=self.CFFSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="TTF",
                view=self.TTFSelector,
                size=self.TTFSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="WOFF",
                view=self.WOFFSelector,
                size=self.WOFFSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="generate",
                view=self.generateFontsSelector,
                size=self.generateFontsSelectorHeight,
                collapsed=True,
                canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, 0), descriptions)

        # setup window

        self.initBatchWindowBehaviour()
        self.openWindow()
        # self.w.open()

    #--------------
    # initializers
    #--------------

    def initCFFSelectorGroup(self):

        self.CFFSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        for option in self.optionsCFF:
            attrName = option.replace('(', '').replace(')', '').replace(' ', '_')
            checkBox = CheckBox(
                (x, y, -p, self.textHeight),
                option,
                sizeStyle=self.sizeStyle)
            setattr(self.CFFSelector, attrName, checkBox)
            y += self.textHeight

        y += p
        self.CFFSelectorHeight = y

    def initTTFSelectorGroup(self):

        self.TTFSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        for option in self.optionsTTF:
            attrName = option.replace('(', '').replace(')', '').replace(' ', '_')
            checkBox = CheckBox(
                (x, y, -p, self.textHeight),
                option,
                sizeStyle=self.sizeStyle)
            setattr(self.TTFSelector, attrName, checkBox)
            y += self.textHeight

        y += p
        self.TTFSelectorHeight = y

    def initWOFFSelectorGroup(self):

        self.WOFFSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.WOFFSelector.format = RadioGroup(
                (x, y, -p, self.textHeight),
                ['OTF', 'TTF'],
                isVertical=False,
                sizeStyle=self.sizeStyle)
        self.WOFFSelector.format.set(0)

        y += self.textHeight + p
        self.WOFFSelector.obfuscateNames = CheckBox(
                (x, y, -p, self.textHeight),
                'obfuscate font names',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.WOFFSelector.subset = CheckBox(
                (x, y, -p, self.textHeight),
                'subset',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        textBoxHeight = self.textHeight * 4
        self.WOFFSelector.glyphNames = EditText(
                (x, y, -p, textBoxHeight),
                '',
                sizeStyle=self.sizeStyle)

        y += textBoxHeight + p
        self.WOFFSelector.importGlyphNames = SquareButton(
                (x, y, -p, self.buttonHeight),
                "import glyph names…",
                # callback=self.generateFontsCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.WOFFSelector.removeFeatures = CheckBox(
                (x, y, -p, self.textHeight),
                'remove features',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.WOFFSelector.removeKerning = CheckBox(
                (x, y, -p, self.textHeight),
                'remove kerning',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.WOFFSelector.removeHinting = CheckBox(
                (x, y, -p, self.textHeight),
                'remove hinting',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.WOFFSelectorHeight = y

    def initGenerateFontsGroup(self):

        self.generateFontsSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        listHeight = self.textHeight * len(self.formatsGenerate)
        self.generateFontsSelector.formats = List(
                (x, y, -p, listHeight),
                self.formatsGenerate,
                drawFocusRing=False)

        y += listHeight + p
        self.generateFontsSelector.releaseMode = CheckBox(
                (x, y, -p, self.textHeight),
                "release mode",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.generateFontsSelector.addDSIG = CheckBox(
                (x, y, -p, self.textHeight),
                "add DSIG table",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.generateFontsSelector.addSuffix = CheckBox(
                (x, y, -p, self.textHeight),
                "add suffix",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.generateFontsSelector.suffix = EditText(
                (x, y, -p, self.textHeight),
                self.settings['suffix'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.generateFontsSelector.setCustomVersion = CheckBox(
                (x, y, -p, self.textHeight),
                "custom version string",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.generateFontsSelector.customVersion = EditText(
                (x, y, -p, self.textHeight),
                self.settings['versionString'],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.generateFontsSelector.getDestinationFolder = SquareButton(
                (x, y, -p, self.buttonHeight),
                "get output folder…",
                # callback=self.getDestinationFolderCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.generateFontsSelector.createSubfolder = CheckBox(
                (x, y, -p, self.textHeight),
                "create subfolders",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.generateFontsSelector.overwriteExistingFiles = CheckBox(
                (x, y, -p, self.textHeight),
                "overwrite existing files",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.generateFontsSelector.applyButton = SquareButton(
                (x, y, -p, self.buttonHeight),
                "generate fonts",
                callback=self.generateFontsCallback,
                sizeStyle=self.sizeStyle)

        y += self.buttonHeight + p
        self.generateFontsSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.generateFontsSelectorHeight = y

    #-----------
    # callbacks
    #-----------

    def generateFontsCallback(self):
        pass

#---------
# testing
#---------

if __name__ == '__main__':

    BatchGenerateDialog()
