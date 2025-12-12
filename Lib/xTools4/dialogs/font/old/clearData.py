from vanilla import Button, CheckBox
from mojo.roboFont import CurrentFont
from xTools4.dialogs.old import hDialog
from xTools4.modules.messages import noFontOpen, showMessage
from xTools4.modules.fontutils import markGlyphs

KEY = 'com.xTools4.dialogs.font.clearData'
class ClearFontDataDialog(hDialog):

    '''
    A dialog to clear different kinds of font-level data.

    '''

    title = 'clear'
    key = '%s.font.clearData' % hDialog.key
    settings = {}

    options = [
        "guidelines",
        "groups",
        "kerning",
        "features",
        "stems",
        "blue values",
        "layers",
        "template glyphs",
        "mark colors",
    ]

    def __init__(self):
        self.height  = self.textHeight * (len(self.options) + 1)
        self.height += self.padding * 3 - 2
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        y -= 3

        for option in self.options:
            checkBox = CheckBox(
                (x, y, -p, self.textHeight),
                option, value=False,
                sizeStyle=self.sizeStyle)
            attrName = option.replace(' ', '_')
            setattr(self.w, attrName, checkBox)
            y += self.textHeight

        y += p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "clear",
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        self.openWindow()

    # ---------
    # callbacks
    # ---------

    def applyCallback(self, sender):

        font = CurrentFont()
        if font is None:
            if self.verbose:
                showMessage(noFontOpen, messageMode)
            return

        if self.verbose:
            print(f'clearing font data in {font.info.familyName} {font.info.styleName}...\n')

        for option in self.options:
            attrName = option.replace(' ', '_')
            checkBox = getattr(self.w, attrName)
            if not checkBox.get():
                continue

            if option == 'kerning':
                if self.verbose:
                    print('\tdeleting kerning...')
                font.kerning.clear()

            elif option == 'groups':
                if self.verbose:
                    print('\tdeleting groups...')
                font.groups.clear()

            elif option == 'guidelines':
                if self.verbose:
                    print('\tdeleting font guidelines...')
                font.clearGuidelines()

            elif option == 'layers':
                if self.verbose:
                    print('\tdeleting layers...')
                for layerName in font.layerOrder:
                    if layerName == font.defaultLayer.name:
                        continue
                    font.removeLayer(layerName)
                # reset name of default layer
                font.defaultLayer.name = 'foreground'

            elif option == 'template glyphs':
                if self.verbose:
                    print('\tdeleting template glyphs...')
                templateGlyphOrder = []
                for glyphName in font.templateGlyphOrder:
                    if glyphName not in font:
                        continue
                    templateGlyphOrder.append(glyphName)
                font.templateGlyphOrder = templateGlyphOrder

            elif option == 'mark colors':
                if self.verbose:
                    print('\tdeleting mark colors...')
                markGlyphs(font, font.keys(), None, verbose=False)

            elif option == 'blue values':
                if self.verbose:
                    print('\tdeleting blue values...')
                font.info.postscriptBlueValues = []
                font.info.postscriptOtherBlues = []
                font.info.postscriptFamilyBlues = []
                font.info.postscriptFamilyOtherBlues = []

            elif option == 'stems':
                if self.verbose:
                    print('\tdeleting stems...')
                font.info.postscriptStemSnapV = []
                font.info.postscriptStemSnapH = []

            elif option == 'features':
                if self.verbose:
                    print('\tdeleting features...')
                font.features.text = ''
        
        # done
        font.changed()

        if self.verbose:
            print('\n...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    ClearFontDataDialog()
