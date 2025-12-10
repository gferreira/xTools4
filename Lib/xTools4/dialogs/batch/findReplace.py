# from importlib import reload
# import xTools4.dialogs.batch.base
# reload(xTools4.dialogs.batch.base)

from vanilla import TextBox, EditText, CheckBox, Button, Group, List
from mojo.roboFont import CurrentFont
from mojo.UI import AccordionView
from xTools4.dialogs.batch.base import BatchDialogBase

KEY = 'com.xTools4.batchFindReplace'
def findFontInfo(font, txtFind, attributes):
    matches = []
    for attr in attributes:
        value = getattr(font.info, attr)
        if value is None:
            continue
        if value.find(txtFind) != -1:
            matches.append(attr)
    return matches

def replaceFontInfo(font, txtFind, txtReplace, attributes, preflight=False, indentLevel=0):
    for attr in attributes:
        value = getattr(font.info, attr)
        if value is None:
            continue
        if value.find(txtFind) != -1:
            newValue = value.replace(txtFind, txtReplace)
            if preflight:
                print('%s%s:'  % ('\t' * indentLevel, attr))
                print('%s- %s' % ('\t' * indentLevel, value))
                print('%s+ %s' % ('\t' * indentLevel, newValue))
                print()
            else:
                # print()
                setattr(font.info, attr, newValue)


class BatchFindReplaceDialog(BatchDialogBase):

    title = 'batch find & replace'
    settings = {}

    fontInfoAttributes = [
        'familyName',
        'styleName',
        'styleMapFamilyName',
        'styleMapStyleName',
        'copyright',
        'trademark',
        'openTypeNameLicense',
        'openTypeNameLicenseURL',
        'openTypeNameDesigner',
        'openTypeNameDesignerURL',
        'openTypeNameManufacturer',
        'openTypeNameManufacturerURL',
        'note',
        'openTypeNamePreferredFamilyName',
        'openTypeNamePreferredSubfamilyName',
        'openTypeNameCompatibleFullName',
        'openTypeNameWWSFamilyName',
        'openTypeNameWWSSubfamilyName',
        'openTypeNameVersion',
        'openTypeNameUniqueID',
        'openTypeNameDescription',
        'openTypeNameSampleText',
        'postscriptFontName',
        'postscriptFullName',
        'postscriptWeightName',
    ]

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 2, self.height),
                self.title,
                minSize=(self.width * 2, self.height))
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        self.w.findLabel = TextBox(
                (x, y, -p, self.textHeight),
                "find",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.findString = EditText(
                (x, y, -p, self.textHeight),
                '',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.replaceLabel = TextBox(
                (x, y, -p, self.textHeight),
                "replace",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.replaceString = EditText(
                (x, y, -p, self.textHeight),
                '',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        # build groups
        self.initFontSelectorGroup()
        self.initFontInfoGroup()

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
        ]
        self.w.accordionView = AccordionView((0, y, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initFontInfoGroup(self):

        self.fontInfoSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        listHeight = -(self.textHeight + p) * 3 - p
        self.fontInfoSelector.attributes = List(
                (x, y, -p, listHeight),
                self.fontInfoAttributes,
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                drawFocusRing=False)

        y = -(self.textHeight + p) * 3
        self.fontInfoSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                "select all",
                value=False,
                callback=self.selectAllAttributesCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2
        self.fontInfoSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "find & replace",
                callback=self.findReplaceFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.fontInfoSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                value=False,
                sizeStyle=self.sizeStyle)

        self.fontInfoSelectorHeight = 300

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedFontInfoAttributes(self):
        selection = self.fontInfoSelector.attributes.getSelection()
        attrs = []
        for i, attr in enumerate(self.fontInfoAttributes):
            if i in selection:
                attrs.append(attr)
        return attrs

    # ---------
    # callbacks
    # ---------

    def selectAllAttributesCallback(self, sender):
        if sender.get():
            selection = list(range(len(self.fontInfoSelector.attributes)))
        else:
            selection = []
        self.fontInfoSelector.attributes.setSelection(selection)

    def findReplaceFontInfoCallback(self, sender):
        preflight  = self.fontInfoSelector.preflight.get()
        if preflight:
            self.preflight()
        else:
            self.batchFindReplaceFontInfo()

    def preflightFindReplaceFontInfo(self):

        if not len(self.targetFonts):
            return

        txtFind    = self.w.findString.get()
        txtReplace = self.w.replaceString.get()
        attributes = self.selectedFontInfoAttributes

        for targetFontName, targetFont in self.targetFonts:
            matches = findFontInfo(targetFont, txtFind, attributes)
            if len(matches):
                print("matches found in '%s':\n" % targetFontName)
                replaceFontInfo(targetFont, txtFind, txtReplace, attributes, preflight=True, indentLevel=1)
            else:
                print("no matches found in '%s'.\n" % targetFontName)

    def preflight(self):
        self.preflightTargetFonts()
        self.preflightFindReplaceFontInfo()

    def batchFindReplaceFontInfo(self):
        '''
        Batch find & replace string in the selected font info attributes.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        txtFind = self.w.findString.get()
        if not len(txtFind):
            print('find string is empty\n')
            return

        txtReplace = self.w.replaceString.get()

        # --------------------
        # batch find & replace
        # --------------------

        print('batch finding & replacing font info data…\n')

        for targetFontName, targetFont in targetFonts:

            print('\treplacing font info in %s…' % targetFontName)
            replaceFontInfo(targetFont, txtFind, txtReplace, self.selectedFontInfoAttributes, preflight=False, indentLevel=3)

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        print('...done.\n')


# -------
# testing
# -------

if __name__ == '__main__':

    BatchFindReplaceDialog()
