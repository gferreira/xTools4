import AppKit
from vanilla import Group, CheckBox, Button, List, RadioGroup, EditText, ColorWell
from mojo.UI import AccordionView
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.dialogs.batch.base import BatchDialogBase


# TODO: add a new section with transformations (scale, move, rotate, skew)


KEY = f'{BatchDialogBase.key}.actions'


class BatchActionsDialog(BatchDialogBase):

    '''
    A dialog to apply glyph actions in batch to selected fonts.

    ::

        from xTools4.dialogs.batch.actions import BatchActionsDialog
        BatchActionsDialog()

    '''

    title = 'batch glyph actions'
    key   = KEY

    #: A list of available glyph actions.
    actions = [
        'decompose',
        'remove overlaps',
        'add extreme points',
        'auto starting points',
        'correct contour direction',
        'round to integer',
    ]

    ##: A list of available glyph transformations.
    # transformations = [
    #     'skew',
    #     'rotate',
    #     'scale',
    #     'move',
    # ]

    glyphSelectionOptions = [
        "all glyphs in font",
        "font selection",
        "glyph names list",
    ]

    def __init__(self):
        self.height = 360
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, 280))

        # build groups
        self.initFontSelectorGroup()
        self.initGlyphSelectorGroup()
        self.initActionsSelectorGroup()

        # build accordion
        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="glyphs",
                view=self.glyphSelector,
                size=self.glyphSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="actions",
                view=self.actionsSelector,
                size=self.actionsSelectorHeight,
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

    def initActionsSelectorGroup(self):
        '''
        Initialize actionsSelector group.

        '''
        self.actionsSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.actionsSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                'select all',
                value=False,
                callback=self.selectAllActionsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        listHeight = self.textHeight * len(self.actions)
        self.actionsSelector.actions = List(
                (x, y, -p, listHeight),
                self.actions,
                drawFocusRing=False,
                selfDropSettings=dict(type="genericListPboardType",
                        operation=AppKit.NSDragOperationMove,
                        callback=self.genericDropSelfCallback),
                dragSettings=dict(type="genericListPboardType",
                        callback=self.genericDragCallback))

        y += listHeight + p
        self.actionsSelector.contourType = RadioGroup(
                (x, y, -p, self.textHeight),
                ["PostScript", "TrueType"],
                isVertical=False,
                sizeStyle=self.sizeStyle)
        self.actionsSelector.contourType.set(0)

        y += self.textHeight + p
        self.actionsSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "apply selected actions",
                callback=self.batchApplyActionsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.actionsSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.actionsSelectorHeight = y

    def initGlyphSelectorGroup(self):
        '''
        Initialize glyphSelector group.

        '''
        self.glyphSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        radioGroupHeight = self.textHeight * 3
        self.glyphSelector.glyphNamesMode = RadioGroup(
                (x, y, -p, radioGroupHeight),
                self.glyphSelectionOptions,
                sizeStyle=self.sizeStyle)
        self.glyphSelector.glyphNamesMode.set(0)

        y += radioGroupHeight + p
        textBoxHeight = self.textHeight * 4
        self.glyphSelector.glyphNames = EditText(
                (x, y, -p, textBoxHeight),
                "a A ampersand period")

        y += textBoxHeight + p
        self.glyphSelector.markGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                'mark glyphs',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        nsColor = rgb2nscolor((0, 0.5, 1, 0.5))
        self.glyphSelector.markColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=nsColor)

        y += self.buttonHeight + p
        self.glyphSelectorHeight = y

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedActions(self):
        '''
        A list of selected actions.

        '''
        actionsSelection = self.actionsSelector.actions.getSelection()
        actionsSorted    = self.actionsSelector.actions.get()
        actions = []
        for i, action in enumerate(actionsSorted):
            # action is not selected
            if i not in actionsSelection:
                continue
            actions.append(action)
        # done
        return actions

    @property
    def glyphNamesMode(self):
        '''
        The selected glyph names mode.

        '''
        selection = self.glyphSelector.glyphNamesMode.get()
        return self.glyphSelectionOptions[selection]

    @property
    def contourType(self):
        '''
        The selected contour type (PostScript or TrueType).

        '''
        value = self.actionsSelector.contourType.get()
        return ['PS', 'TT'][value]

    # ---------
    # callbacks
    # ---------

    def selectAllActionsCallback(self, sender):
        '''
        Select all actions in the UI.

        '''
        if sender.get():
            selection = list(range(len(self.actions)))
        else:
            selection = []
        self.actionsSelector.actions.setSelection(selection)

    def batchApplyActionsCallback(self, sender):
        '''
        Apply actions or preflight current settings.

        '''
        preflight = self.actionsSelector.preflight.get()
        if preflight:
            self.preflight()
        else:
            self.batchApplyActions()

    # reordering actions list

    def genericDragCallback(self, sender, indexes):
        return indexes

    def genericDropSelfCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        if not isProposal:
            indexes = [int(i) for i in sorted(dropInfo["data"])]
            indexes.sort()
            rowIndex = dropInfo["rowIndex"]
            items = sender.get()
            toMove = [items[index] for index in indexes]
            for index in reversed(indexes):
                del items[index]
            rowIndex -= len([index for index in indexes if index < rowIndex])
            for font in toMove:
                items.insert(rowIndex, font)
                rowIndex += 1
            sender.set(items)
        return True

    # -------
    # methods
    # -------

    def getGlyphNames(self, targetFont):
        '''
        Get selected glyph names for the current glyph names mode.

        '''
        glyphNamesMode = self.glyphNamesMode

        # font selection (works only with open fonts)
        if glyphNamesMode == "font selection":
            if targetFont.hasInterface():
                glyphNames = targetFont.selectedGlyphNames
            else:
                glyphNames = []

        # list of glyph names
        elif glyphNamesMode == "glyph names list":
            txt = self.glyphSelector.glyphNames.get()
            glyphNames = txt.strip().split()

        # "all glyphs in font"
        else:
            glyphNames = targetFont.keys()

        # done
        return glyphNames

    def preflightGlyphs(self):
        '''
        Preflight glyph selection settings.

        '''
        print('glyphs:')
        print('- %s' % self.glyphNamesMode)
        if self.glyphSelector.markGlyphs.get():
            print('- mark glyphs')
        print()

    def preflightActions(self):
        '''
        Preflight selected actions.

        '''
        print('actions:')
        if len(self.selectedActions):
            for action in self.selectedActions:
                if action == 'correct contour direction':
                    print('- %s (%s)' % (action, self.contourType))
                else:
                    print('- %s' % action)
        else:
            print('- [None]')
        print()

    def preflight(self):
        '''
        Print information about the batch operation before actually executing it.

        '''
        self.preflightTargetFonts()
        self.preflightGlyphs()
        self.preflightActions()

    def batchApplyActions(self):
        '''
        Apply actions to selected glyphs in all target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # no actions selected
        selectedActions = self.selectedActions
        if not len(selectedActions):
            print('no actions selected.\n')
            return

        # -------------------
        # batch apply actions
        # -------------------

        markGlyphs  = self.glyphSelector.markGlyphs.get()
        markColor   = nscolor2rgb(self.glyphSelector.markColor.get())
        contourType = self.actionsSelector.contourType.get()

        if self.verbose:
            print('batch applying actions...\n')

        for targetFontName, targetFont in targetFonts:
            if self.verbose:
                print('\tapplying actions to %s...' % targetFontName)

            glyphNames  = self.getGlyphNames(targetFont)

            for glyphName in glyphNames:
                glyph = targetFont[glyphName]
                glyph.prepareUndo('applying action')

                for action in selectedActions:

                    if self.verbose:
                        print('\t\t%s...' % action)

                    if action == 'auto starting points':
                        for contour in glyph.contours:
                            contour.autoStartSegment()

                    if action == 'correct contour direction':
                        glyph.correctDirection(trueType=contourType)

                    if action == 'decompose':
                        glyph.decompose()

                    if action == 'round to integer':
                        glyph.round()

                    if action == 'remove overlaps':
                        glyph.removeOverlap()

                    if action == 'add extreme points':
                        glyph.extremePoints()

                if markGlyphs:
                    glyph.markColor = markColor

                glyph.performUndo()

            # save fonts without UI
            if not targetFont.hasInterface():
                if self.verbose:
                    print()
                    print('\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        if self.verbose:
            print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    BatchActionsDialog()
