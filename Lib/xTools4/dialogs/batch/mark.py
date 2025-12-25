from vanilla import CheckBox, TextBox, EditText, Button, ColorWell, Group, List
from mojo.roboFont import CurrentFont
from mojo.UI import AccordionView
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.fontutils import *
from xTools4.dialogs.batch.base import BatchDialogBase

KEY = 'com.xTools4.dialogs.batch.MarkGlyphs'
class BatchMarkGlyphsDialog(BatchDialogBase):

    '''
    A dialog to apply mark colors and sort target fonts based on different types of search patterns.

    ::

        from xTools4.dialogs.batch.mark import BatchMarkGlyphsDialog
        BatchMarkGlyphsDialog()

    '''

    title = 'batch mark'
    key = '%s.mark' % BatchDialogBase.key

    settings = {
        'color'        : (1, 0.5, 0, 0.5),
        'shortSegment' : 10,
    }

    options = [
        'contours only',
        'components only',
        'contours & components',
        'no contours or components',
        'open contours',
        'short segments',
        # 'overlapping points',
    ]

    sorting = {
        'width'        : 'width',
        'left margin'  : 'leftMargin',
        'right margin' : 'rightMargin',
    }

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 2, self.height),
                self.title,
                minSize=(self.width * 2, self.height))
        self.w.workspaceWindowIdentifier = KEY

        # build groups
        self.initFontSelectorGroup()
        self.initGlyphFiltersGroup()
        self.initGlyphSortingGroup()
        self.initGlyphNamingGroup()

        # build accordion
        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="contents",
                view=self.glyphFiltersSelector,
                size=self.glyphFiltersSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="attributes",
                view=self.glyphSortingSelector,
                size=self.glyphSortingSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="naming",
                view=self.glyphNamingSelector,
                size=self.glyphNamingSelectorHeight,
                collapsed=True,
                canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
        # self.w.open()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initGlyphFiltersGroup(self):
        '''
        Initialize glyphFilters group.

        '''
        self.glyphFiltersSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        listHeight = self.textHeight * len(self.options)
        self.glyphFiltersSelector.glyphFilters = List(
                (x, y, -p, listHeight),
                self.options,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                drawFocusRing=False)

        y += listHeight + p
        self.glyphFiltersSelector.color = ColorWell(
                (x, y, -p, self.textHeight),
                color=rgb2nscolor(self.settings['color']))

        y += self.textHeight + p
        self.glyphFiltersSelector.clearColors = CheckBox(
                (x, y, -p, self.textHeight),
                "clear colors",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.glyphFiltersSelector.selectGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "select glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphFiltersSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "mark glyphs",
                callback=self.markGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphFiltersSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphFiltersSelectorHeight = y

    def initGlyphSortingGroup(self):
        '''
        Initialize glyphSorting group.

        '''
        self.glyphSortingSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        listHeight = self.textHeight * len(self.sorting)
        self.glyphSortingSelector.glyphSorting = List(
                (x, y, -p, listHeight),
                self.sorting.keys(),
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                drawFocusRing=False)

        y += listHeight + p
        self.glyphSortingSelector.markGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "mark glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.glyphSortingSelector.orderGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "sort glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphSortingSelector.sortGlyphsButton = Button(
                (x, y, -p, self.textHeight),
                "get grouped values",
                callback=self.sortGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphSortingSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphSortingSelectorHeight = y

    def initGlyphNamingGroup(self):
        '''
        Initialize glyphNaming group.

        '''
        self.glyphNamingSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding

        self.glyphNamingSelector.glyphStringLabel = TextBox(
                (x, y, -p, self.textHeight),
                "glyph name contains:",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.3
        self.glyphNamingSelector.glyphString = EditText(
                (x, y, -p, self.textHeight),
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphNamingSelector.selectGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "select glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.glyphNamingSelector.markGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "mark glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphNamingSelector.markColor = ColorWell(
                (x, y, -p, self.textHeight),
                color=rgb2nscolor((1, 0, 1, 0.5)))

        y += self.textHeight + p
        self.glyphNamingSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "find glyphs",
                callback=self.searchGlyphNamesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphNamingSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphNamingSelectorHeight = y

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedGlyphFilter(self):
        '''
        Selected glyph contents option.

        '''
        i = self.glyphFiltersSelector.glyphFilters.getSelection()[0]
        return self.glyphFiltersSelector.glyphFilters.get()[i]

    @property
    def selectedGlyphSorting(self):
        '''
        Selected glyph sorting option.

        '''
        i = self.glyphSortingSelector.glyphSorting.getSelection()[0]
        return self.glyphSortingSelector.glyphSorting.get()[i]

    # ---------
    # callbacks
    # ---------

    def markGlyphsCallback(self, sender):
        preflight = self.glyphFiltersSelector.preflight.get()
        if preflight:
            self.preflight(mark=True)
        else:
            self.batchMarkGlyphs()

    def sortGlyphsCallback(self, sender):
        preflight = self.glyphSortingSelector.preflight.get()
        if preflight:
            self.preflight(sort=True)
        else:
            self.batchSortGlyphs()

    def searchGlyphNamesCallback(self, sender):
        preflight = self.glyphNamingSelector.preflight.get()
        if preflight:
            self.preflight(names=True)
        else:
            self.batchSearchGlyphNames()

    # -------
    # methods
    # -------

    def preflightMarkGlyphs(self):
        '''
        Preflight mark color settings.

        '''
        clearColors  = self.glyphFiltersSelector.clearColors.get()
        selectGlyphs = self.glyphFiltersSelector.selectGlyphs.get()
        print('options:')
        print('- %s' % self.selectedGlyphFilter)
        if clearColors:
            print('- clear colors')
        if selectGlyphs:
            print('- select glyphs')
        print()

    def preflightSortGlyphs(self):
        '''
        Preflight settings for sorting glyphs.

        '''
        markGlyphs  = self.glyphSortingSelector.markGlyphs.get()
        orderGlyphs = self.glyphSortingSelector.orderGlyphs.get()
        print('options:')
        print('- %s' % self.selectedGlyphSorting)
        if markGlyphs:
            print('- mark glyphs')
        if orderGlyphs:
            print('- order glyphs')
        print()

    def preflightGlyphNames(self):
        '''
        Preflight settings for glyph names.

        '''
        selectGlyphs = self.glyphNamingSelector.selectGlyphs.get()
        markGlyphs   = self.glyphNamingSelector.markGlyphs.get()
        findString   = self.glyphNamingSelector.glyphString.get().strip()

        # search options
        print('glyph names containing:')
        print('- %s' % findString)
        print()

        # options
        print('options:')
        if not selectGlyphs and not markGlyphs:
            print('- [None]')
        else:
            if selectGlyphs:
                print('- select glyphs')
            if markGlyphs:
                print('- mark glyphs')
        print()

    def preflight(self, mark=False, sort=False, names=False):
        '''
        Print information about the batch operation before actually executing it.

        '''
        self.preflightTargetFonts()
        if mark:
            self.preflightMarkGlyphs()
        if sort:
            self.preflightSortGlyphs()
        if names:
            self.preflightGlyphNames()

    def batchMarkGlyphs(self):
        '''
        Batch mark glyphs based on the selected filter.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # -----------------
        # batch mark glyphs
        # -----------------

        print('batch marking glyphs...\n')

        # get settings
        color          = nscolor2rgb(self.glyphFiltersSelector.color.get())
        clearColors    = self.glyphFiltersSelector.clearColors.get()
        selectedFilter = self.selectedGlyphFilter
        selectGlyphs   = self.glyphFiltersSelector.selectGlyphs.get()

        # get target fonts
        for targetFontName, targetFont in targetFonts:

            # find glyphs by filter
            if selectedFilter == 'contours only':
                glyphNames = findContoursOnly(targetFont)

            if selectedFilter == 'components only':
                glyphNames = findComponentsOnly(targetFont)

            if selectedFilter == 'contours & components':
                glyphNames = findContoursAndComponents(targetFont)

            if selectedFilter == 'no contours or components':
                glyphNames = findEmptyGlyphs(targetFont)

            if selectedFilter == 'open contours':
                glyphNames = findOpenContours(targetFont)

            if selectedFilter == 'short segments':
                glyphNames = findShortSegments(targetFont, threshold=10)

            if selectedFilter == 'overlapping points':
                glyphNames = findClosePoints(targetFont, threshold=0)

            # mark glyphs
            print('\tmarking glyphs in font %s %s...\n' % (targetFont.info.familyName, targetFont.info.styleName))

            if clearColors:
                print('\t\tremoving mark colors in all glyphs...\n')
                clearMarkColors(targetFont)

            for glyphName in glyphNames:
                print('\t\t- %s' % glyphName)
                g = targetFont[glyphName]
                g.markColor = color

            # select glyphs
            if selectGlyphs:
                targetFont.selectedGlyphNames = glyphNames

            # save fonts without UI
            if not targetFont.hasInterface():
                print()
                print('\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchSortGlyphs(self):
        '''
        Batch sort glyphs based on the selected attribute.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # -----------------
        # batch sort glyphs
        # -----------------

        print('batch processing glyphs...\n')

        # get settings
        markGlyphs      = self.glyphSortingSelector.markGlyphs.get()
        orderGlyphs     = self.glyphSortingSelector.orderGlyphs.get()
        selectedSorting = self.selectedGlyphSorting
        attribute       = self.sorting[selectedSorting]
        sortFont        = True

        # get target fonts
        for targetFontName, targetFont in targetFonts:

            print('\tprocessing glyphs in font %s...\n' % targetFontName)

            values = findAttribute(targetFont, attribute, mark=markGlyphs, sort=orderGlyphs)
            for value, glyphNames in values.items():
                print('\t\t%s : %s' % (value, ' '.join(glyphNames)))

            # save fonts without UI
            if not targetFont.hasInterface():
                print()
                print('\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchSearchGlyphNames(self):
        '''
        Batch apply mark colors to glyphs with names with a given string.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # -------------------
        # batch search glyphs
        # -------------------

        print('batch searching glyph names...\n')

        # get settings
        searchString = self.glyphNamingSelector.glyphString.get().strip()
        selectGlyphs = self.glyphNamingSelector.selectGlyphs.get()
        markGlyphs   = self.glyphNamingSelector.markGlyphs.get()
        markColor    = nscolor2rgb(self.glyphNamingSelector.markColor.get())

        # get target fonts
        for targetFontName, targetFont in targetFonts:

            print('\tsearching glyph names in font %s...\n' % targetFontName)

            matches = []
            for glyphName in targetFont.glyphOrder:
                if searchString in glyphName:
                    matches.append(glyphName)
                    # mark glyph
                    if markGlyphs:
                        targetFont[glyphName].markColor = markColor

            # print matches
            if len(matches):
                print('\t\t%s' % ' '.join(matches))
            else:
                print('\t\t[no matches found]')
            print()

            # select glyphs
            if selectGlyphs:
                targetFont.selectedGlyphNames = matches

            # save fonts without UI
            if not targetFont.hasInterface():
                print()
                print('\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    BatchMarkGlyphsDialog()
