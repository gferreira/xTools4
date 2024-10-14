# from importlib import reload
# import xTools4.modules.fontutils
# reload(xTools4.modules.fontutils)
# import xTools4.dialogs.batch.base
# reload(xTools4.dialogs.batch.base)

from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from vanilla import List, CheckBox, Button, TextBox, EditText, PopUpButton, Group, RadioGroup, ColorWell
from mojo.events import addObserver, removeObserver
from mojo.roboFont import CurrentFont
from mojo.UI import AccordionView
from xTools4.modules.fontinfo import FontInfoAttributes, FontInfoAttributesIgnorePrefix
from xTools4.modules.fontutils import getFontID
from xTools4.modules.anchors import copyAnchors
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.dialogs.batch.base import BatchDialogBase


class BatchCopyDialog(BatchDialogBase):

    '''
    A dialog to copy data from one source font to all selected target fonts.

    .. code-block:: python

        from xTools4.dialogs.batch.copy import BatchCopyDialog
        BatchCopyDialog()

    '''

    title = 'batch copy'
    key   = f'{BatchDialogBase.key}.copy'

    fontInfo = dict(FontInfoAttributes)
    del fontInfo['WOFF']
    del fontInfo['Miscellaneous']

    attrsIgnorePrefix = FontInfoAttributesIgnorePrefix

    glyphData = [
        'contours',
        'components',
        'anchors',
        'width',
        'mark color',
        # 'unicodes',
        # 'guidelines',
        # 'image',
    ]

    def __init__(self):
        self.height = 480
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, 280))

        # build groups
        self.initFontSelectorGroup()
        self.initFontInfoSelectorGroup()
        self.initGlyphDataSelectorGroup()
        self.initKerningSelectorGroup()
        self.initGroupsSelectorGroup()
        self.initFeaturesSelectorGroup()

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
                canResize=False),
            dict(label="glyphs",
                view=self.glyphDataSelector,
                size=self.glyphDataSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="kerning",
                view=self.kerningSelector,
                size=self.kerningSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="groups",
                view=self.groupsSelector,
                size=self.groupsSelectorHeight,
                collapsed=True,
                canResize=False),
            dict(label="features",
                view=self.featuresSelector,
                size=self.featuresSelectorHeight,
                collapsed=True,
                canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
        addObserver(self, "updateSourceFontsCallback", "fontBecameCurrent")
        self.updateSourceFonts()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initFontSelectorGroup(self):
        '''
        Initialize fontSelector group.

        '''
        self.fontSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.fontSelector.sourceLabel = TextBox(
                (x, y, -p, self.textHeight),
                "source font:",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.fontSelector.sourceFont = PopUpButton(
                (x, y, -p, self.textHeight),
                [],
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.5
        self.fontSelector.getCurrentFont = CheckBox(
                (x, y, -p, self.textHeight),
                "current font",
                value=True,
                sizeStyle=self.sizeStyle,
                callback=self.updateSourceFontsCallback)

        y += self.textHeight + p
        self.fontSelector.targetLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target fonts:",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        listHeight = -(self.textHeight + p) * 4
        self.fontSelector.targetFonts = List(
                (x, y, -p, listHeight),
                [],
                drawFocusRing=False,
                enableDelete=False,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropCallback))

        y = -(self.textHeight + p) * 4 + p
        self.fontSelector.addOpenFonts = CheckBox(
                (x, y, -p, self.textHeight),
                "add all open fonts",
                callback=self.addOpenFontsCallback,
                value=True,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 3
        self.fontSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                "select all target fonts",
                callback=self.selectAllTargetFontsCallback,
                value=False,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2
        self.fontSelector.addFontsFolder = Button(
                (x, y, -p, self.textHeight),
                "add fonts folder…",
                callback=self.addFontsFolderCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.fontSelector.clearFonts = Button(
                (x, y, -p, self.textHeight),
                "clear font lists",
                callback=self.clearFontsCallback,
                sizeStyle=self.sizeStyle)

        self.fontSelectorHeight = 340

    def initFontInfoSelectorGroup(self):
        '''
        Initialize fontInfoSelector group.

        '''
        self.fontInfoSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.fontInfoSelector.selectAll = CheckBox(
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
                setattr(self.fontInfoSelector, '%s%sGroup' % (k, kk), sectionTitle)
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
                    setattr(self.fontInfoSelector, attrName, checkBox)
                    y += self.textHeight
                y += p

        self.fontInfoSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "copy font info",
                callback=self.batchCopyFontInfoCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.fontInfoSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.fontInfoSelectorHeight = y

    def initGlyphDataSelectorGroup(self):
        '''
        Initialize glyphDataSelector group.

        '''
        self.glyphDataSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        radioGroupHeight = self.textHeight * 2
        self.glyphDataSelector.glyphNamesMode = RadioGroup(
                (x, y, -p, radioGroupHeight),
                ["font selection", "glyph names list"],
                sizeStyle=self.sizeStyle)
        self.glyphDataSelector.glyphNamesMode.set(1)

        y += radioGroupHeight + p
        textBoxHeight = self.textHeight * 4
        self.glyphDataSelector.glyphNames = EditText(
                (x, y, -p, textBoxHeight),
                "a A ampersand period")

        y += textBoxHeight + p
        self.glyphDataSelector.glyphDataLabel = TextBox(
                (x, y, -p, self.textHeight),
                "glyph data:",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        listHeight = len(self.glyphData) * self.textHeight
        self.glyphDataSelector.glyphData = List(
                (x, y, -p, listHeight),
                self.glyphData,
                drawFocusRing=False)

        y += listHeight + p
        self.glyphDataSelector.removeSourceGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                'remove source glyphs',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.glyphDataSelector.clearTargetContours = CheckBox(
                (x, y, -p, self.textHeight),
                'clear target contours',
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.glyphDataSelector.selectGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "select target glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.glyphDataSelector.customColorCheckbox = CheckBox(
                (x, y, -p, self.textHeight),
                "mark target glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.5
        nsColor = rgb2nscolor((1, 0, 0, 0.5))
        self.glyphDataSelector.customColor = ColorWell(
                (x, y, -p, self.textHeight),
                color=nsColor)

        y += self.textHeight + p
        self.glyphDataSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "copy glyph data",
                callback=self.batchCopyGlyphDataCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.glyphDataSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.5
        self.glyphDataSelectorHeight = y

    def initKerningSelectorGroup(self):
        '''
        Initialize kerningSelector group.

        '''
        self.kerningSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.kerningSelector.clearTargetKerning = CheckBox(
                (x, y, -p, self.textHeight),
                "clear target kerning",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.kerningSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "copy kerning",
                callback=self.batchCopyKerningCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.kerningSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.kerningSelectorHeight = y

    def initGroupsSelectorGroup(self):
        '''
        Initialize groupsSelector group.

        '''
        self.groupsSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.groupsSelector.clearTargetGroups = CheckBox(
                (x, y, -p, self.textHeight),
                "clear target groups",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.groupsSelector.copyPlainGroups = CheckBox(
                (x, y, -p, self.textHeight),
                "copy plain groups",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.groupsSelector.copyKerningGroups = CheckBox(
                (x, y, -p, self.textHeight),
                "copy kerning groups",
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.groupsSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "copy groups",
                callback=self.batchCopyGroupsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.groupsSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.groupsSelectorHeight = y

    def initFeaturesSelectorGroup(self):
        '''
        Initialize featuresSelector group.

        '''
        self.featuresSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.featuresSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "copy features",
                callback=self.batchCopyFeaturesCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.featuresSelectorHeight = y

    # -------------
    # dynamic attrs
    # -------------

    @property
    def targetFonts(self):
        '''
        A list of all selected target fonts (excluding the source font).

        '''
        # get source font
        if self.sourceFont:
            sourceFontID, sourceFont = self.sourceFont
        else:
            sourceFontID = sourceFont = self.sourceFont

        # get target fonts
        targetSelection = self.fontSelector.targetFonts.getSelection()
        targetFonts = []
        for i, targetFontID in enumerate(sorted(self.fonts.keys())):
            # skip source font
            if sourceFontID and targetFontID == sourceFontID:
                continue
            # target font is not selected
            if i not in targetSelection:
                continue
            # get target RFont
            targetFont = self.getFont(targetFontID)
            targetFonts.append((targetFontID, targetFont))

        # done
        return targetFonts

    @property
    def sourceFont(self):
        '''
        The selected source font.

        '''
        if self.fontSelector.getCurrentFont.get():
            f = CurrentFont()
            if not f:
                print('no current font selected (checkbox disabled)\n')
                self.fontSelector.getCurrentFont.set(False)
                return
            sourceFontID = getFontID(f)
            sourceFont = f
        else:
            i = self.fontSelector.sourceFont.get()
            if not len(self.fonts):
                return
            sourceFontID = sorted(self.fonts.keys())[i]
            sourceFont = self.getFont(sourceFontID)
        return sourceFontID, sourceFont

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
                    checkBox = getattr(self.fontInfoSelector, attrName)
                    value = checkBox.get()
                    if value:
                        attrs.append(kkk)
        return attrs

    @property
    def glyphNames(self):
        '''
        A list of selected glyph names.

        '''
        # get glyph names mode
        mode = self.glyphDataSelector.glyphNamesMode.get()
        # selected glyphs
        if mode == 0:
            if not self.sourceFont:
                return
            sourceFont = self.sourceFont[1]
            return sourceFont.selectedGlyphNames
        # string input
        else:
            txt = self.glyphDataSelector.glyphNames.get()
            return txt.strip().split()

    @property
    def selectedGlyphData(self):
        '''
        A list of selected glyph data types.

        '''
        selection  = self.glyphDataSelector.glyphData.getSelection()
        attributes = self.glyphDataSelector.glyphData.get()
        return [attr for i, attr in enumerate(attributes) if i in selection]

    @property
    def glyphDataOptions(self):
        '''
        A list of selected glyph options.

        '''
        options = []
        if self.glyphDataSelector.removeSourceGlyphs.get():
            options.append('remove source glyphs')
        if self.glyphDataSelector.clearTargetContours.get():
            options.append('clear target contours')
        if self.glyphDataSelector.customColorCheckbox.get():
            options.append('mark target glyphs')
        if self.glyphDataSelector.selectGlyphs.get():
            options.append('select target glyphs')
        return options

    # ---------
    # callbacks
    # ---------

    def updateSourceFontsCallback(self, sender):
        self.updateSourceFonts()

    def selectAllFontInfoCallback(self, sender):
        value = sender.get()
        for section in self.fontInfo.keys():
            for subsection in self.fontInfo[section].keys():
                attrName = '%s%sGroup' % (section, subsection)
                checkBox = getattr(self.fontInfoSelector, attrName)
                checkBox.set(value)
                for attribute in self.fontInfo[section][subsection]:
                    attrName = '%s_%s_%s' % (section, subsection, attribute)
                    checkBox = getattr(self.fontInfoSelector, attrName)
                    checkBox.set(value)

    def selectFontInfoSubSectionCallback(self, sender):
        section, subsection = sender.getTitle().split('>')
        section = section.strip()
        subsection = subsection.strip()
        value = sender.get()
        for attribute in self.fontInfo[section][subsection]:
            attrName = '%s_%s_%s' % (section, subsection, attribute)
            checkBox = getattr(self.fontInfoSelector, attrName)
            checkBox.set(value)

    def batchCopyFontInfoCallback(self, sender):
        preflight = self.fontInfoSelector.preflight.get()
        if preflight:
            self.preflight(fontInfo=True)
        else:
            self.batchCopyFontInfo()

    def batchCopyGlyphDataCallback(self, sender):
        preflight = self.glyphDataSelector.preflight.get()
        if preflight:
            self.preflight(glyphData=True)
        else:
            self.batchCopyGlyphData()

    def batchCopyKerningCallback(self, sender):
        preflight = self.kerningSelector.preflight.get()
        if preflight:
            self.preflight(kerning=True)
        else:
            self.batchCopyKerning()

    def batchCopyGroupsCallback(self, sender):
        preflight = self.groupsSelector.preflight.get()
        if preflight:
            self.preflight(groups=True)
        else:
            self.batchCopyGroups()

    def batchCopyFeaturesCallback(self, sender):
        self.batchCopyFeatures()

    # ---------
    # observers
    # ---------

    # overwrite BatchDialogBase methods

    def removeFontCallback(self, notification):
        # get closed font (RFont)
        closedFont = notification['font']
        # remove closed font from fonts dict
        fonts = {}
        for fontID in self.fonts.keys():
            font = self.fonts[fontID]
            if font != closedFont:
                fonts[fontID] = font
        self.fonts = fonts
        # update lists
        self.updateTargetFonts()
        self.updateSourceFonts()

    def windowCloseCallback(self, sender):
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontWillClose")
        removeObserver(self, "fontBecameCurrent")
        super().windowCloseCallback(sender)

    # -------
    # methods
    # -------

    def updateSourceFonts(self):
        '''
        Update the source font pop-up menu in the UI.

        '''
        # source is list of all fonts
        if not self.fontSelector.getCurrentFont.get():
            fontIDs = sorted(self.fonts.keys())
            self.fontSelector.sourceFont.setItems(fontIDs)
        # source is current font
        else:
            # get current font
            f = CurrentFont()
            if f is not None:
                fontID = getFontID(f)
                # set current font
                self.fontSelector.sourceFont.setItems([fontID])
            # no font open
            else:
                self.fontSelector.sourceFont.setItems([])

    def preflightSourceFont(self):
        '''
        Preflight the source font.

        '''
        print('source font:')
        if self.sourceFont:
            print('- %s' % self.sourceFont[0])
        else:
            print('- [None]')
        print()

    def preflightFontInfo(self):
        '''
        Preflight font info settings.

        '''
        print('font info attributes:')
        if len(self.selectedAttributes):
            for attr in self.selectedAttributes:
                print('- %s' % attr)
        # no font info selected
        else:
            print('- [None]')
        print()

    def preflightGlyphData(self):
        '''
        Preflight glyph data settings.

        '''
        # glyph names
        print('glyph names:')
        if self.glyphNames:
            for glyphName in self.glyphNames:
                print('- %s' % glyphName)
        # no glyph names defined
        else:
            print('- [None]')
        print()

        # glyph data
        print('glyph data:')
        if len(self.selectedGlyphData):
            for d in self.selectedGlyphData:
                print('- %s' % d)
        # no glyph data selected
        else:
            print('- [None]')
        print()

        # glyph options
        print('options:')
        if len(self.glyphDataOptions):
            for option in self.glyphDataOptions:
                print('- %s' % option)
        # no options selected
        else:
            print('- [None]')
        print()

    def preflightKerning(self):
        '''
        Preflight kerning settings.

        '''
        print('kerning options:')
        clearTargetKerning = self.kerningSelector.clearTargetKerning.get()
        if clearTargetKerning:
            print('- clear target kerning')
        # no option selected
        else:
            print('- [None]')
        print()

    def preflightGroups(self):
        '''
        Preflight groups settings.

        '''
        clearTargetGroups = self.groupsSelector.clearTargetGroups.get()
        copyPlainGroups   = self.groupsSelector.copyPlainGroups.get()
        copyKerningGroups = self.groupsSelector.copyKerningGroups.get()
        print('groups options:')
        if any([clearTargetGroups, copyPlainGroups, copyKerningGroups]):
            if clearTargetGroups:
                print('- clear target groups')
            if copyPlainGroups:
                print('- copy plain groups')
            if copyKerningGroups:
                print('- copy kerning groups')
        # no option selected
        else:
            print('- [None]')
        print()

    def preflight(self, fontInfo=False, glyphData=False, kerning=False, groups=False):
        '''
        Print information about the batch operation before actually executing it.

        '''
        self.preflightSourceFont()
        self.preflightTargetFonts()

        if fontInfo:
            self.preflightFontInfo()

        if glyphData:
            self.preflightGlyphData()

        if kerning:
            self.preflightKerning()

        if groups:
            self.preflightGroups()

    def batchCopyFontInfo(self):
        '''
        Batch copy font info values from source font to target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no source font
        if not self.sourceFont:
            print('no source font selected.\n')
            return

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # no font info attributes selected
        selectedAttributes = self.selectedAttributes
        if not len(self.selectedAttributes):
            print('no font info attributes selected.\n')
            return

        # --------------------
        # batch copy font info
        # --------------------

        print('batch copying font info...\n')

        # get source font
        sourceFontName, sourceFont = self.sourceFont
        print('\tsource font: %s\n' % sourceFontName)

        # get target fonts
        for targetFontName, targetFont in targetFonts:
            print('\tcopying font info to %s...' % targetFontName)

            # get font info attributes
            for attr in selectedAttributes:
                value = getattr(sourceFont.info, attr)
                print('\t\tcopying %s...' % attr)
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

    def batchCopyGlyphData(self):
        '''
        Batch copy glyph data from source font to target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no source font
        if not self.sourceFont:
            print('no source font selected.\n')
            return

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # no glyphs selected
        glyphNames = self.glyphNames
        if not len(glyphNames):
            print('no glyphs selected or specified.\n')
            return

        # ---------------------
        # batch copy glyph data
        # ---------------------

        print('batch copying glyph data...\n')

        # get source font
        sourceFontName, sourceFont = self.sourceFont
        print('\tsource font: %s\n' % sourceFontName)

        # get settings
        glyphDataOptions   = self.glyphDataOptions
        selectedGlyphData  = self.selectedGlyphData
        selectTargetGlyphs = 'select target glyphs' in glyphDataOptions

        # get custom mark color
        customMarkColor = None
        if 'mark target glyphs' in glyphDataOptions:
            nsColor = self.glyphDataSelector.customColor.get()
            customMarkColor = nscolor2rgb(nsColor)

        # get target fonts
        for targetFontName, targetFont in targetFonts:
            print("\tcopying glyph data to font '%s'...\n" % targetFontName)

            # get glyph names
            for glyphName in glyphNames:

                # source font does not have a glyph with this name
                if glyphName not in sourceFont:
                    print("\t\tglyph '%s' not in source font\n" % glyphName)
                    continue

                # get source glyph
                sourceGlyph = sourceFont[glyphName]

                # get target glyph
                if glyphName not in targetFont:
                    targetFont.newGlyph(glyphName)
                targetGlyph = targetFont[glyphName]

                print("\t\tcopying data in glyph '%s'..." % glyphName)

                # clear target contours
                if 'clear target contours' in glyphDataOptions:
                    print('\t\t\tdeleting target contours...')
                    targetGlyph.clear()

                # copy glyph data
                for glyphData in selectedGlyphData:

                    # advance width
                    if glyphData == 'width':
                        print('\t\t\tcopying width...')
                        targetGlyph.width = sourceGlyph.width

                    # contours
                    if glyphData == 'contours':
                        print('\t\t\tcopying contours...')
                        pen = targetGlyph.getPointPen()
                        sourceGlyph.drawPoints(pen, contours=True, components=False)

                    # components
                    if glyphData == 'components':
                        print('\t\t\tcopying components...')
                        pen = targetGlyph.getPointPen()
                        sourceGlyph.drawPoints(pen, contours=False, components=True)

                    # anchors
                    if glyphData == 'anchors':
                        print('\t\t\tcopying anchors...')
                        copyAnchors(sourceGlyph, targetGlyph, clear=False, proportional=False)

                    # mark color
                    if glyphData == 'mark color' and not customMarkColor:
                        print('\t\t\tcopying mark color...')
                        targetGlyph.markColor = sourceGlyph.markColor

                    # guidelines
                    if glyphData == 'guidelines':
                        print('\t\t\tcopying guidelines... [not implemented]')

                    # image
                    if glyphData == 'image':
                        print('\t\t\tcopying image... [not implemented]')

                # custom mark color
                if customMarkColor:
                    print('\t\t\tsetting custom mark color...')
                    targetGlyph.markColor = customMarkColor

                # done with glyph
                print()

            # select glyphs
            if selectTargetGlyphs:
                print('\t\tselecting glyphs...')
                targetFont.selectedGlyphNames = glyphNames
                print()

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\t\tsaving %s...' % targetFontName)
                targetFont.save()
                targetFont.close()
                print()

        # remove source glyphs
        if 'remove source glyphs' in glyphDataOptions:
            for glyphName in glyphNames:
                sourceFont.removeGlyph(glyphName)

        # done
        print('...done.\n')

    def batchCopyKerning(self):
        '''
        Batch copy kerning from source font to target fonts.

        '''

        # -----------------
        # assert conditions
        # -----------------

        # no source font
        if not self.sourceFont:
            print('no source font selected.\n')
            return

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')

        # ------------------
        # batch copy kerning
        # ------------------

        print('batch copying kerning...\n')

        # get source font
        sourceFontName, sourceFont = self.sourceFont
        print('\tsource font: %s\n' % sourceFontName)

        # get settings
        clearTargetKerning = self.kerningSelector.clearTargetKerning.get()

        # get target fonts
        for targetFontName, targetFont in targetFonts:

            # clear target kerning
            if clearTargetKerning:
                targetFont.kerning.clear()

            # copy kerning
            print('\tcopying kerning to %s...' % targetFontName)
            for kernPair, value in sourceFont.kerning.items():
                targetFont.kerning[kernPair] = value

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\t\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchCopyGroups(self):
        '''
        Batch copy groups from source font to target fonts.

        '''

        #-------------------
        # assert conditions
        #-------------------

        # no source font
        if not self.sourceFont:
            print('no source font selected.\n')
            return

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')

        #-------------------
        # batch copy groups
        #-------------------

        print('batch copying groups...\n')

        # get source font
        sourceFontName, sourceFont = self.sourceFont
        print('\tsource font: %s\n' % sourceFontName)

        # get settings
        clearTargetGroups = self.groupsSelector.clearTargetGroups.get()
        copyPlainGroups   = self.groupsSelector.copyPlainGroups.get()
        copyKerningGroups = self.groupsSelector.copyKerningGroups.get()

        # get target fonts
        for targetFontName, targetFont in targetFonts:

            # clear target groups
            if clearTargetGroups:
                targetFont.groups.clear()

            # copy groups
            print('\tcopying groups to %s...\n' % targetFontName)
            for groupName, glyphNames in sourceFont.groups.items():

                # do not copy kerning groups
                if groupName.startswith('public.kern') and not copyKerningGroups:
                    continue

                # do not copy plain groups
                elif not groupName.startswith('public.kern') and not copyPlainGroups:
                    continue

                # copy groups
                else:
                    print('\t\tcopying group %s...' % groupName)
                    targetFont.groups[groupName] = glyphNames

            # save fonts without UI
            if not targetFont.hasInterface():
                print()
                print('\t\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

    def batchCopyFeatures(self):
        '''
        Batch copy OpenType features from source font to target fonts.

        '''

        #-------------------
        # assert conditions
        #-------------------

        # no source font
        if not self.sourceFont:
            print('no source font selected.\n')
            return

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # get source font
        sourceFontName, sourceFont = self.sourceFont
        print('\tsource font: %s\n' % sourceFontName)

        # no features in source font
        if not len(sourceFont.features.text):
            print('source font features are empty.\n')
            return

        #---------------------
        # batch copy features
        #---------------------

        print('batch copying features...\n')

        # get target fonts
        for targetFontName, targetFont in targetFonts:

            # copy features
            print("\tcopying features to font '%s'...\n" % targetFontName)
            targetFont.features.text = sourceFont.features.text

            # save fonts without UI
            if not targetFont.hasInterface():
                print('\t\tsaving font...')
                targetFont.save()
                targetFont.close()

            # done with font
            print()

        # done
        print('...done.\n')

# --------
# testing
# --------

if __name__ == '__main__':

    BatchCopyDialog()
