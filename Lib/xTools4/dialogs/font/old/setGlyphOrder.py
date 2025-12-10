from vanilla import *
from mojo.roboFont import CurrentFont
from mojo.UI import GetFile
from xTools4.dialogs.old import hDialog
from xTools4.modules.encoding import importEncoding, setGlyphOrder, psname2char, importGroupsFromEncoding, paintGroups
from xTools4.modules.fontutils import clearMarkColors

KEY = 'com.xTools4.setGlyphOrder'
class SetGlyphOrderDialog(hDialog):

    title    = 'font'
    key      = f'{hDialog.key}.font.glyphOrder'
    settings = {}

    def __init__(self):
        self.height  = self.textHeight * 4
        self.height += self.padding * 4
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        self.w.getFileButton = Button(
            (x, y, -p, self.textHeight),
            'select...',
            sizeStyle=self.sizeStyle,
            callback=self.getEncodingFileCallback)

        y += self.textHeight + p
        self.w.setGlyphOrder = Button(
            (x, y, -p, self.textHeight),
            'set glyph order',
            sizeStyle=self.sizeStyle,
            callback=self.setglyphOrder)

        y += self.textHeight + p
        self.w.createGlyphs = CheckBox(
                (x, y, -p, self.textHeight),
                "create glyphs",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.paintGroups = CheckBox(
                (x, y, -p, self.textHeight),
                "paint groups",
                value=False,
                sizeStyle=self.sizeStyle)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def glyphOrder(self):
        return importEncoding(self.encPath)

    @property
    def createGlyphs(self):
        print(self.w.createGlyphs.get())
        return self.w.createGlyphs.get()

    # ---------
    # callbacks
    # ---------

    def getEncodingFileCallback(self, sender):
        self.encPath = GetFile(message='Get encoding file…', title=self.title)

    # -------
    # methods
    # -------

    def setglyphOrder(self, sender):

        font = CurrentFont()
        if font is None:
            return

        setGlyphOrder(font, self.encPath, verbose=False, createGlyphs=self.createGlyphs)

        # print characters
        # txt = [psname2char(g) for g in self.glyphOrder if psname2char(g)]
        # print(''.join(sorted(txt)))

        # paint remaining glyphs
        if not self.w.paintGroups.get():
            restGlyphs = set(font.keys()).difference(set(self.glyphOrder))
            clearMarkColors(font)
            for glyphName in restGlyphs:
                font[glyphName].markColor = 1, 0, 0, 0.3

        # paint groups
        else:
            groups = importGroupsFromEncoding(self.encPath)
            paintGroups(font, groups, crop=False)
