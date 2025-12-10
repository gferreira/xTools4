# menuTitle: TempGlyphs

import os, sys
from AppKit import NSFilenamesPboardType, NSDragOperationCopy
from vanilla import FloatingWindow, List, Button, TextBox, EditText, RadioGroup, ProgressBar, Group
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.ufoLib.glifLib import GlyphSet
from mojo.UI import AccordionView
from mojo.roboFont import OpenFont, NewFont, CurrentFont

KEY = 'com.xTools4.tempGlyphs'
class TempGlyphs:

    '''
    - open a sparse source for editing
    - drag and drop UFO source fonts into the sources list
    - click the 'import' button to import glyphs from the selected source into selected (template) glyphs in the current font
    - imported glyphs are added to the `skipExportGlyphs` list in the font lib
    - click the 'clear' button to delete imported glyphs when editing is finished

    '''

    title      = 'TempGlyphs'
    width      = 123*2
    height     = 180
    padding    = 10
    lineHeight = 22
    verbose    = True
    font       = None
    _sources   = {}

    def __init__(self):
        self.w = FloatingWindow(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width, self.height),
                maxSize=(self.width*2, self.width)
            )

        x = y = p = self.padding
        self.w.sourceFontsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources',
                sizeStyle='small')

        y += self.lineHeight
        self.w.sourceFonts = List(
                (x, y, -p, -(self.lineHeight*3) - p*2.5),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                otherApplicationDropSettings=dict(
                    type=NSFilenamesPboardType,
                    operation=NSDragOperationCopy,
                    callback=self.dropCallback)
                )

        y = -(self.lineHeight*3) - p*2
        self.w.importButton = Button(
                (x, y, -p, self.lineHeight),
                'import',
                callback=self.importButtonCallback,
                sizeStyle='small')

        y = -(self.lineHeight*2) - p*1.5
        self.w.toggleButton = Button(
                (x, y, -p, self.lineHeight),
                'toggle',
                callback=self.toggleButtonCallback,
                sizeStyle='small')

        y = -(p + self.lineHeight)
        self.w.clearButton = Button(
                (x, y, -p, self.lineHeight),
                'clear',
                callback=self.clearButtonCallback,
                sizeStyle='small')

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    @property
    def selectedSource(self):
        selection = self.w.sourceFonts.getSelection()
        sources   = self.w.sourceFonts.get()
        if selection is None or not sources:
            return
        return sources[selection[0]]

    def dropCallback(self, sender, dropInfo):

        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.ufo']

        if not paths:
            return False

        if not isProposal:
            for path in paths:
                label = os.path.splitext(os.path.split(path)[-1])[0]
                self._sources[label] = path
                self.w.sourceFonts.append(label)
                self.w.sourceFonts.setSelection([0])

        return True

    def _assertConditions(self):

        self.font = CurrentFont()

        if self.font is None:
            if self.verbose:
                print('please open a font first.\n')
            return

        if not self.font.templateSelectedGlyphNames:
            if self.verbose:
                print('please select some glyphs in the current font.\n')
            return

        return True

    def importButtonCallback(self, sender):

        if not self._assertConditions():
            return

        ufoPath = self._sources.get(self.selectedSource)
        if ufoPath is None:
            if self.verbose:
                print('please define a source font first.\n')
            return

        srcFont = OpenFont(ufoPath, showInterface=False)

        if self.verbose:
            print('importing glyphs from selected source...\n')

        skipExportGlyphs = self.font.lib.get('public.skipExportGlyphs', [])

        for glyphName in self.font.templateSelectedGlyphNames:
            if glyphName not in srcFont:
                continue
            self.font.insertGlyph(srcFont[glyphName])
            if glyphName not in skipExportGlyphs:
                skipExportGlyphs.append(glyphName)

        srcFont.close()

        self.font.lib['public.skipExportGlyphs'] = skipExportGlyphs
        self.font.changed()

        if self.verbose:
            print('...done.\n')

    def toggleButtonCallback(self, sender):

        if not self._assertConditions():
            return

        skipExportGlyphs = self.font.lib.get('public.skipExportGlyphs', [])

        if self.verbose:
            print("toggling temp glyph status...\n")

        for glyphName in self.font.templateSelectedGlyphNames:
            if glyphName in skipExportGlyphs:
                skipExportGlyphs.remove(glyphName)
            else:
                skipExportGlyphs.append(glyphName)

        for glyphName in self.font.templateSelectedGlyphNames:
            self.font[glyphName].changed()

        self.font.lib['public.skipExportGlyphs'] = skipExportGlyphs

        if self.verbose:
            print('...done.\n')

    def clearButtonCallback(self, sender):

        self.font = CurrentFont()

        if self.font is None:
            return

        skipExportGlyphs   = self.font.lib.get('public.skipExportGlyphs', [])
        templateGlyphOrder = self.font.templateGlyphOrder

        for glyphName in skipExportGlyphs:
            if glyphName in self.font:
                del self.font[glyphName]

        self.font.lib['public.skipExportGlyphs'] = []
        self.font.templateGlyphOrder = templateGlyphOrder


if __name__ == '__main__':

    TempGlyphs()
