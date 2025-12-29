from vanilla import *
from xTools4.dialogs.old import hDialog

KEY = 'com.xTools4.dialogs.glyphs.glyphData'
class SelectGlyphDataDialog(hDialog):

    title = "glyph data"

    # key  = hDialog.key
    # key += '.glyphs.glyphDataSelect'

    glyphData = [
        'contours',
        'components',
        'advance width',
        'left margin',
        'right margin',
        'anchors',
        'guidelines',
        'image',
        'unicode',
        'mark color',
        'glyph lib',
    ]

    def __init__(self):
        self.height = self.textHeight * len(self.glyphData) + self.padding * 2 - 3
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        y -= 3
        for dataType in self.glyphData:
            attrName = dataType.split(' ')
            attrName = [a.capitalize() if i else a for i, a in enumerate(attrName)]
            attrName = ''.join(attrName)
            checkBox = CheckBox(
                (x, y, - p, self.textHeight),
                dataType,
                value=False, #self.settings[action],
                sizeStyle=self.sizeStyle)
            setattr(self.w, attrName, checkBox)
            y += self.textHeight

        self.openWindow()

if __name__ == "__main__":

    SelectGlyphDataDialog()
