# from importlib import reload
# import xTools4.dialogs
# reload(xTools4.dialogs)

import os
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from vanilla import Group, TextBox, List, CheckBox, Button, PopUpButton
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.UI import AccordionView, GetFolder
from mojo.roboFont import AllFonts, CurrentFont, RFont, OpenFont
from mojo.events import addObserver, removeObserver
from xTools4.dialogs.old import hDialog
from xTools4.modules.fontutils import getFontID

KEY = 'com.xTools4.batchBase'
class BatchDialogBase(hDialog, BaseWindowController):

    '''
    A Base object for tools which do something to several fonts.

    '''

    title = 'batch'
    key   = f'{hDialog.key}.batch'

    #: The type of the window.
    #: 
    #: - ``0``: FloatingWindow
    #: - ``1``: HUDFloatingWindow
    #: - ``2``: Window
    windowType = 0

    #: A dictionary to hold a set of fonts for batch processing.
    fonts = {}

    def __init__(self):
        self.height = 400
        self.width *= 3
        self.w = self.window(
                (self.width, self.height),
                self.title,
                minSize=(self.width, self.height))
        self.w.workspaceWindowIdentifier = KEY

        # build groups
        self.initFontSelectorGroup()

        # build accordion
        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window
        self.initBatchWindowBehaviour()
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
        self.fontSelector.targetLabel = TextBox(
                (x, y, -p, self.textHeight),
                "target fonts:",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        listHeight = -(self.textHeight + p) * 2 - (self.textHeight * 2 + p) - p
        self.fontSelector.targetFonts = List(
                (x, y, -p, listHeight),
                [],
                drawFocusRing=False,
                enableDelete=False,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropCallback))

        y = -(self.textHeight + p) * 2 - (self.textHeight * 2 + p)
        self.fontSelector.addOpenFonts = CheckBox(
                (x, y, -p, self.textHeight),
                "add all open fonts",
                callback=self.addOpenFontsCallback,
                value=True,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2 - (self.textHeight + p)
        self.fontSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                "select all target fonts",
                callback=self.selectAllTargetFontsCallback,
                value=False,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2
        self.fontSelector.addFontsFolder = Button(
                (x, y, -p, self.textHeight),
                "add fonts folder...",
                callback=self.addFontsFolderCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.fontSelector.clearFonts = Button(
                (x, y, -p, self.textHeight),
                "clear font lists",
                callback=self.clearFontsCallback,
                sizeStyle=self.sizeStyle)

        self.fontSelectorHeight = 300

    def initBatchWindowBehaviour(self):
        '''
        Initialize Batch window behaviour.

        '''
        self.setUpBaseWindowBehavior()

        addObserver(self, "addOpenFontsCallback", "newFontDidOpen")
        addObserver(self, "addOpenFontsCallback", "fontDidOpen")
        addObserver(self, "removeFontCallback",   "fontWillClose")

        self.addOpenFonts()
        self.updateTargetFonts()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def targetFonts(self):
        '''
        A list of all selected target fonts.

        Returns:
            A list of font objects (RFont).

        '''
        targetSelection = self.fontSelector.targetFonts.getSelection()
        targetFonts = []
        for i, targetFontID in enumerate(sorted(self.fonts.keys())):
            if i not in targetSelection:
                continue
            targetFont = self.getFont(targetFontID)
            targetFonts.append((targetFontID, targetFont))
        return targetFonts

    @property
    def targetFontPaths(self):
        '''
        A list with the paths of all selected target fonts.

        Returns:
            A list of strings (UFO paths).

        '''
        targetSelection = self.fontSelector.targetFonts.getSelection()
        targetFontPaths = []
        for i, targetFontID in enumerate(sorted(self.fonts.keys())):
            if i not in targetSelection:
                continue
            targetFontPath = self.getFontPath(targetFontID)
            targetFontPaths.append(targetFontPath)
        return targetFontPaths

    # ---------
    # callbacks
    # ---------

    def selectAllTargetFontsCallback(self, sender):
        '''
        Select all target fonts in the UI.

        '''
        if sender.get():
            selection = list(range(len(self.fontSelector.targetFonts)))
        else:
            selection = []
        self.fontSelector.targetFonts.setSelection(selection)

    def addOpenFontsCallback(self, sender):
        '''
        Add all open fonts to the dialog. Update the internal list and the UI.

        '''
        self.addOpenFonts()
        self.updateTargetFonts()

    def addFontsFolderCallback(self, sender):
        '''
        Select a folder and add all UFOs in the folder to the dialog.

        '''
        # get folder
        msg = 'get a folder with UFO files'
        folder = GetFolder(message=msg, title=self.title)
        if not folder:
            print('No folder selected.\n')
            return
        # update fonts list
        self.addFontsFolder(folder)
        self.updateTargetFonts()

    def clearFontsCallback(self, sender):
        '''
        Clear the internal fonts list and update the UI.

        '''
        self.fontSelector.addOpenFonts.set(False)
        self.fonts = {}
        self.updateTargetFonts()

    def removeFontCallback(self, notification):
        '''
        Removes a font from the fonts list after its font window is closed.

        Args:
            notification: A fontDidClose notification.

        '''
        # get closed font (RFont)
        closedFont = notification['font']
        # remove closed font from fonts dict
        fonts = {}
        for fontID in self.fonts.keys():
            font = self.fonts[fontID]
            if font != closedFont:
                fonts[fontID] = font
        self.fonts = fonts
        # update list
        self.updateTargetFonts()

    def windowCloseCallback(self, sender):
        '''
        Removes observers from the dialog after the window is closed.

        '''
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
        super().windowCloseCallback(sender)

    def dropCallback(self, sender, dropInfo):

        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.ufo']

        if not paths:
            return False

        if not isProposal:
            for ufoPath in paths:
                fontID = getFontID(ufoPath)
                self.fonts[fontID] = ufoPath
            self.updateTargetFonts()

        return True

    # -------
    # methods
    # -------

    def addOpenFonts(self):
        '''
        Adds all open fonts to the internal fonts dictionary.

        '''
        show = self.fontSelector.addOpenFonts.get()
        for f in AllFonts():
            fontID = getFontID(f)
            if show:
                self.fonts[fontID] = f
            else:
                if fontID in self.fonts:
                    del self.fonts[fontID]

    def addFontsFolder(self, folder):
        '''
        Adds all fonts from a folder to the internal fonts dictionary.

        Args:
            folder (str): The path to a folder with UFOs.

        '''
        for f in os.listdir(folder):
            if os.path.splitext(f)[-1] == '.ufo':
                fontPath = os.path.join(folder, f)
                fontID = getFontID(fontPath)
                self.fonts[fontID] = fontPath

    def updateTargetFonts(self):
        '''
        Update the list of target fonts in the UI.

        '''
        fontsList = sorted(self.fonts.keys())
        self.fontSelector.targetFonts.set(fontsList)

    def getFont(self, fontID):
        '''
        Get the font object for a given font ID.

        Args:
            fontID (str): A font identification string.

        Returns:
            A font object (RFont).

        '''
        font = self.fonts[fontID]
        if not isinstance(font, RFont):
            font = OpenFont(font, showInterface=False)
        return font

    def getFontPath(self, fontID):
        '''
        Get the font path for a given font ID.

        Args:
            fontID (str): A font identification string.

        Returns:
            The path to the font file.

        '''
        font = self.fonts[fontID]
        if isinstance(font, RFont):
            return font.path
        return font

    def preflightTargetFonts(self):
        '''
        Preflight target fonts.

        '''
        print('target fonts:')
        if len(self.targetFonts):
            for targetFont in self.targetFonts:
                print('- %s' % targetFont[0])
        else:
            print('- [None]')
        print()


class BatchDialogBaseCopy(BatchDialogBase):

    '''
    A Base object for batch dialogs which copy something from one source font to a bunch of fonts.

    '''

    sourceFontNotInTargetFonts = True

    # ------------
    # initializers
    # ------------

    def initBatchCopyWindowBehaviour(self):
        '''
        Initialize Batch Copy window behaviour.

        '''
        self.setUpBaseWindowBehavior()

        addObserver(self, "addOpenFontsCallback",      "newFontDidOpen")
        addObserver(self, "addOpenFontsCallback",      "fontDidOpen")
        addObserver(self, "removeFontCallback",        "fontWillClose")
        addObserver(self, "updateSourceFontsCallback", "fontBecameCurrent")

        self.addOpenFonts()
        self.updateSourceFonts()
        self.updateTargetFonts()

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
        listHeight = -(self.textHeight + p) * 2 - (self.textHeight * 2 + p) - p
        self.fontSelector.targetFonts = List(
                (x, y, -p, listHeight),
                [],
                drawFocusRing=False,
                enableDelete=False,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropCallback))

        y = -(self.textHeight + p) * 2 - (self.textHeight * 2 + p)
        self.fontSelector.addOpenFonts = CheckBox(
                (x, y, -p, self.textHeight),
                "add all open fonts",
                callback=self.addOpenFontsCallback,
                value=True,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2 - (self.textHeight + p)
        self.fontSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                "select all target fonts",
                callback=self.selectAllTargetFontsCallback,
                value=False,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p) * 2
        self.fontSelector.addFontsFolder = Button(
                (x, y, -p, self.textHeight),
                "add fonts folder...",
                callback=self.addFontsFolderCallback,
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.fontSelector.clearFonts = Button(
                (x, y, -p, self.textHeight),
                "clear font lists",
                callback=self.clearFontsCallback,
                sizeStyle=self.sizeStyle)

        self.fontSelectorHeight = 340

    # -------------
    # dynamic attrs
    # -------------

    @property
    def sourceFont(self):
        '''
        The selected source font.

        Returns:
            A tuple with the font ID and the font object.

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
    def targetFonts(self):
        '''
        A list of all selected target fonts (excluding the source font).

        Returns:
            A list of font objects (RFont).

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
            if self.sourceFontNotInTargetFonts:
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

    # ---------
    # callbacks
    # ---------

    def updateSourceFontsCallback(self, sender):
        self.updateSourceFonts()

    # ---------
    # observers
    # ---------

    def removeFontCallback(self, notification):
        '''
        Removes a font from the fonts list after its font window is closed.

        Args:
            A fontDidClose notification.

        '''
        # TODO: rewrite using decorator
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
        '''
        Removes observers from the dialog after the window is closed.

        '''
        removeObserver(self, "newFontDidOpen")
        removeObserver(self, "fontDidOpen")
        removeObserver(self, "fontDidClose")
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


# -------
# testing
# -------

if __name__ == '__main__':

    BatchDialogBase()
    BatchDialogBaseCopy()
