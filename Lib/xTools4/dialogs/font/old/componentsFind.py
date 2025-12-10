from vanilla import FloatingWindow, EditText, List, Button, TextBox, ColorWell
from mojo.UI import OpenGlyphWindow
from mojo.roboFont import CurrentFont
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.fontutils import findGlyphComponents
from xTools4.dialogs.old import hDialog

KEY = 'com.xTools4.componentsFind'
class FindGlyphComponentsDialog(hDialog):

    '''
    A dialog to find all components of a given glyph and change the base glyph in the selected glyphs.

    '''

    title = "components"
    key = '%s.font.componentsFind' % hDialog.key
    settings = {
        'markColor' : (0, 1, 1, 0.3),
    }

    def __init__(self):
        self.height  = 360
        self.w = self.window((self.width, self.height), self.title, minSize=(self.width, self.height))
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        y -= 2
        self.w.findLabel = TextBox(
                (x, y, -p, self.textHeight),
                'find',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.baseGlyph = EditText(
                (x, y, -p, self.textHeight),
                '',
                continuous=True,
                sizeStyle=self.sizeStyle,
                callback=self.findComponentsCallback)

        y += self.textHeight + p
        listHeight = -(self.textHeight + p) * 3  -(self.buttonHeight + p) - p
        self.w.composedGlyphs = List((x, y, -p, listHeight),
                 [],
                 doubleClickCallback=self.selectionCallback,
                 allowsMultipleSelection=True,
                 allowsEmptySelection=False)

        y = -(self.textHeight + p) * 3  -(self.buttonHeight + p)
        self.w.markColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.settings['markColor']))

        y = -(self.textHeight + p) * 3
        self.w.markButton = Button(
                (x, y, -p, self.textHeight),
                'mark',
                sizeStyle=self.sizeStyle,
                callback=self.markComponentsCallback)

        y = -(self.textHeight + p) * 2
        self.w.newBaseGlyph = EditText(
                (x, y, -p, self.textHeight),
                '',
                sizeStyle=self.sizeStyle)

        y = -(self.textHeight + p)
        self.w.replaceButton = Button(
                (x, y, -p, self.textHeight),
                'replace',
                sizeStyle=self.sizeStyle,
                callback=self.replaceComponentsCallback)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedGlyphNames(self):
        selection  = self.w.composedGlyphs.getSelection()
        glyphNames = self.w.composedGlyphs.get()
        return [g for i, g in enumerate(glyphNames) if i in selection]

    @property
    def markColor(self):
        nsColor = self.w.markColor.get()
        return nscolor2rgb(nsColor)

    # ---------
    # callbacks
    # ---------

    def findComponentsCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        componentMapping = font.getReverseComponentMapping()
        baseGlyphName = self.w.baseGlyph.get()            
        components = componentMapping[baseGlyphName] if baseGlyphName in componentMapping else []
        self.w.composedGlyphs.set(components)

    def selectionCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        glyphName = self.selectedGlyphNames[0]
        OpenGlyphWindow(glyph=font[glyphName], newWindow=True)

    def markComponentsCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        for glyphName in self.selectedGlyphNames:
            glyph = font[glyphName]
            glyph.prepareUndo('mark components')
            glyph.markColor = self.markColor
            glyph.performUndo()

    def replaceComponentsCallback(self, sender):
        font = CurrentFont()
        if font is None:
            return
        oldBase = self.w.baseGlyph.get()
        newBase = self.w.newBaseGlyph.get()
        for glyphName in self.selectedGlyphNames:
            glyph = font[glyphName]
            for component in glyph.components:
                if component.baseGlyph == oldBase:
                    component.baseGlyph = newBase

