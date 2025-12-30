from vanilla import Group, CheckBox, Button
from mojo.UI import AccordionView
from xTools4.modules.fontinfo import FontInfoAttributes, FontInfoAttributesIgnorePrefix
from xTools4.modules.fontutils import clearMarkColors, clearUnicodes
from xTools4.dialogs.batch.base import BatchDialogBase


KEY = f'{BatchDialogBase.key}.clear'


class BatchClearDialog(BatchDialogBase):

    '''
    A dialog to delete font-level and glyph-level data in the selected fonts.

    ::

        from xTools4.dialogs.batch.actions import BatchClearDialog
        BatchClearDialog()

    '''

    title = 'batch clear'
    key   = KEY

    fontInfo = dict(FontInfoAttributes)
    del fontInfo['WOFF']
    del fontInfo['Miscellaneous']

    attrsIgnorePrefix = FontInfoAttributesIgnorePrefix

    clearFontData = [
        'groups',
        'features',
        'kerning',
        'mark colors',
        'anchors',
        'unicodes',
        # 'images',
        # 'components',
        # 'layers',
        'font guides',
        'glyph guides',
        'font lib',
        'glyph lib',
    ]

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, self.height))

        # build groups

        self.initFontSelectorGroup()
        self.initClearFontInfoGroup()
        self.initClearFontDataGroup()

        # build accordion

        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="font info",
                view=self.clearFontInfoSelector,
                size=self.clearFontInfoSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="font data",
                view=self.clearFontDataSelector,
                size=self.clearFontDataSelectorHeight,
                collapsed=True,
                canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initClearFontInfoGroup(self):
        '''
        Initialize clearFontInfo group.

        '''
        self.clearFontInfoSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.clearFontInfoSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                'select all',
                value=False,
                callback=self.selectAllFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        for k in self.fontInfo.keys():
            for kk in self.fontInfo[k].keys():
                sectionTitle = CheckBox(
                        (x, y, -p, self.textHeight),
                        '%s > %s' % (k, kk),
                        value=False,
                        callback=self.selectFontInfoSubSectionCallback,
                        sizeStyle=self.sizeStyle)
                setattr(self.clearFontInfoSelector, '%s%sGroup' % (k, kk), sectionTitle)
                y += self.textHeight
                for kkk in self.fontInfo[k][kk]:
                    attrTitle = kkk
                    if k in self.attrsIgnorePrefix:
                        if kk in self.attrsIgnorePrefix[k]:
                            ignore = self.attrsIgnorePrefix[k][kk]
                            attrTitle = attrTitle.replace(ignore, '')
                    checkBox = CheckBox(
                            (x + p * 1.6, y, -p, self.textHeight),
                            attrTitle,
                            value=False,
                            sizeStyle=self.sizeStyle)
                    attrName = '%s_%s_%s' % (k, kk, kkk)
                    setattr(self.clearFontInfoSelector, attrName, checkBox)
                    y += self.textHeight
                y += p

        self.clearFontInfoSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "clear font info",
                callback=self.batchClearFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.clearFontInfoSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.clearFontInfoSelectorHeight = y

    def initClearFontDataGroup(self):
        '''
        Initialize clearFontData group.

        '''
        self.clearFontDataSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.clearFontDataSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                'select all',
                value=False,
                callback=self.selectAllFontDataCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        for d in self.clearFontData:
            attrName = d.replace(' ', '_')
            checkBox = CheckBox(
                    (x, y, -p, self.textHeight),
                    d,
                    value=False,
                    sizeStyle=self.sizeStyle)
            setattr(self.clearFontDataSelector, attrName, checkBox)
            y += self.textHeight

        y += p
        self.clearFontDataSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "clear font data",
                callback=self.batchClearFontDataCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.clearFontDataSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.clearFontDataSelectorHeight = y

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedAttributes(self):
        '''
        A list of selected font info attributes.

        '''
        attrs = []
        for k in self.fontInfo.keys():
            for kk in self.fontInfo[k].keys():
                for kkk in self.fontInfo[k][kk]:
                    attrName = '%s_%s_%s' % (k, kk, kkk)
                    checkBox = getattr(self.clearFontInfoSelector, attrName)
                    value = checkBox.get()
                    if value:
                        attrs.append(kkk)
        return attrs

    @property
    def selectedFontData(self):
        '''
        A list of selected font data types.

        '''
        attrs = []
        for d in self.clearFontData:
            attrName = d.replace(' ', '_')
            checkBox = getattr(self.clearFontDataSelector, attrName)
            value = checkBox.get()
            if value:
                attrs.append(d)
        return attrs

    # ---------
    # callbacks
    # ---------

    def selectAllFontInfoCallback(self, sender):
        value = sender.get()
        for section in self.fontInfo.keys():
            for subsection in self.fontInfo[section].keys():
                attrName = '%s%sGroup' % (section, subsection)
                checkBox = getattr(self.clearFontInfoSelector, attrName)
                checkBox.set(value)
                for attribute in self.fontInfo[section][subsection]:
                    attrName = '%s_%s_%s' % (section, subsection, attribute)
                    checkBox = getattr(self.clearFontInfoSelector, attrName)
                    checkBox.set(value)

    def selectAllFontDataCallback(self, sender):
        value = sender.get()
        for d in self.clearFontData:
            attrName = d.replace(' ', '_')
            checkBox = getattr(self.clearFontDataSelector, attrName)
            checkBox.set(value)

    def selectFontInfoSubSectionCallback(self, sender):
        section, subsection = sender.getTitle().split('>')
        section = section.strip()
        subsection = subsection.strip()
        value = sender.get()
        for attribute in self.fontInfo[section][subsection]:
            attrName = '%s_%s_%s' % (section, subsection, attribute)
            checkBox = getattr(self.clearFontInfoSelector, attrName)
            checkBox.set(value)

    def batchClearFontInfoCallback(self, sender):
        preflight = self.clearFontInfoSelector.preflight.get()
        if preflight:
            self.preflight(fontInfo=True, fontData=False)
        else:
            self.batchClearFontInfo()

    def batchClearFontDataCallback(self, sender):
        preflight = self.clearFontDataSelector.preflight.get()
        if preflight:
            self.preflight(fontInfo=False, fontData=True)
        else:
            self.batchClearFontData()

    # -------
    # methods
    # -------

    def preflightFontInfo(self):
        '''
        Preflight selected font info attributes.

        '''
        print('font info attributes:')
        if len(self.selectedAttributes):
            for attr in self.selectedAttributes:
                print('- %s' % attr)
        else:
            print('- [None]')
        print()

    def preflightFontData(self):
        '''
        Preflight selected glyph data types.

        '''
        print('font data:')
        if len(self.selectedFontData):
            for d in self.selectedFontData:
                print('- %s' % d)
        else:
            print('- [None]')
        print()

    def preflight(self, fontInfo=True, fontData=True):
        '''
        Print information about the batch operation before actually executing it.

        '''

        self.preflightTargetFonts()

        if fontInfo:
            self.preflightFontInfo()

        if fontData:
            self.preflightFontData()

    def batchClearFontInfo(self):
        '''
        Clear font info attributes from all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        selectedAttributes = self.selectedAttributes
        if not len(selectedAttributes):
            print('no font info attributes selected.\n')
            return

        # ---------------------
        # batch clear font info
        # ---------------------

        print('batch clearing font info...\n')

        clearFontInfoExceptions = {
            'descender'  : -250,
            'xHeight'    : 500,
            'ascender'   : 750,
            'capHeight'  : 750,
            'unitsPerEm' : 1000,
        }

        for targetFontName, targetFont in targetFonts:
            print('\tclearing font info in %s...' % targetFontName)
            for attr in selectedAttributes:
                if attr in clearFontInfoExceptions.keys():
                    value = clearFontInfoExceptions[attr]
                else:
                    value = None
                print('\t\tclearing %s...' % attr)
                setattr(targetFont.info, attr, value)

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\t\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchClearFontData(self):
        '''
        Clear font data from all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # no font data selected
        selectedFontData = self.selectedFontData
        if not len(self.selectedFontData):
            print('no font data selected.\n')
            return

        # ---------------------
        # batch clear font data
        # ---------------------

        print('batch clearing font data...\n')

        # get target fonts
        for targetFontName, targetFont in targetFonts:
            print("\tclearing font data in font '%s'...\n" % targetFontName)
            for fontData in selectedFontData:

                # groups
                if fontData == 'groups':
                    print('\t\tclearing groups...')
                    targetFont.groups.clear()

                # features
                if fontData == 'features':
                    print('\t\tclearing features...')
                    targetFont.features.text = ''

                # kerning
                if fontData == 'kerning':
                    print('\t\tclearing kerning...')
                    targetFont.kerning.clear()

                # mark color
                if fontData == 'mark colors':
                    print('\t\tclearing mark colors...')
                    clearMarkColors(targetFont)

                # anchors
                if fontData == 'anchors':
                    print('\t\tclearing anchors...')
                    for g in targetFont:
                        g.clearAnchors()
                        if targetFont.hasInterface():
                            g.changed()

                # unicodes
                if fontData == 'unicodes':
                    print('\t\tclearing unicodes...')
                    clearUnicodes(targetFont)

                # font guides
                if fontData == 'font guides':
                    print('\t\tclearing font guides...')
                    targetFont.clearGuidelines()

                # glyph guides
                if fontData == 'glyph guides':
                    print('\t\tclearing glyph guides...')
                    for g in targetFont:
                        g.clearGuidelines()
                        if targetFont.hasInterface():
                            g.changed()

                # font lib
                if fontData == 'font lib':
                    print('\t\tclearing the font lib...')
                    targetFont.lib.clear()

                # glyph lib
                if fontData == 'glyph lib':
                    print('\t\tclearing glyph libs...')
                    for g in targetFont:
                        g.lib.clear()
                        if targetFont.hasInterface():
                            g.changed()

            # done with font
            print()

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\tsaving %s...' % targetFontName)
                targetFont.save()
                targetFont.close()
                print()
            else:
                targetFont.changed()

        # done
        print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    BatchClearDialog()
