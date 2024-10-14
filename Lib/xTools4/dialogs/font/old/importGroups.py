from vanilla import Button, CheckBox
from mojo.roboFont import CurrentFont
from xTools4.dialogs.old import hDialog


class ImportGroupsDialog(hDialog):

    '''
    A dialog to import, paint and clear glyph groups.

    '''

    title = 'groups'
    key = '%s.font.importGroups' % hDialog.key
    settings = {}
    windowType = 1

    def __init__(self):
        self.height  = self.textHeight * 4
        self.height += self.padding * 5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.paintGroups = Button(
                (x, y, -p, self.textHeight),
                "paint",
                sizeStyle=self.sizeStyle,
                callback=self.paintCallback)

        y += self.textHeight + p
        self.w.cropGlyphset = CheckBox(
                (x, y, -p, self.textHeight),
                "crop glyphset",
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.importGroups = Button(
                (x, y, -p, self.textHeight),
                "import",
                sizeStyle=self.sizeStyle,
                callback=self.importCallback)

        y += self.textHeight + p
        self.w.deleteGroups = Button(
                (x, y, -p, self.textHeight),
                "clear",
                sizeStyle=self.sizeStyle,
                callback=self.deleteCallback)

        self.w.open()

    # ---------
    # callbacks
    # ---------

    def paintCallback(self, sender):
        pass

    def importCallback(self, sender):
        pass

    def deleteCallback(self, sender):
        pass

# -------
# testing
# -------

if __name__ == '__main__':

    ImportGroupsDialog()
