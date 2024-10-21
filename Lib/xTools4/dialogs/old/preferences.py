from vanilla import TextBox, ColorWell, Slider, CheckBox, Group
from mojo.UI import UpdateCurrentGlyphView, AccordionView
from xTools4.dialogs.old import hDialog
from xTools4.modules.color import rgb2nscolor, nscolor2rgb


class PreferencesDialog(hDialog):

    '''
    A dialog to edit global hTools3 settings.

    ::

        from hTools3.dialogs.preferences import PreferencesDialog
        PreferencesDialog()

    '''

    title = 'settings'
    key = f'{hDialog.key}.preferences'

    def __init__(self):
        self.height  = self.textHeight * 7
        self.height += self.buttonHeight * 2
        self.height += self.padding * 6
        self.w = self.window(
                (self.width, self.height), self.title,
                minSize=(self.width, self.height - self.textHeight*2 - self.padding +2),
                maxSize=(self.width, self.height + 15))

        self.initPreviewGroup()
        self.initOptionsGroup()
        self.initAccordionView()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initPreviewGroup(self):

        self.previewGroup =  Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.previewGroup.previewFillColorLabel = TextBox(
                (x, y, -p, self.textHeight),
                'fill color',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.previewGroup.previewFillColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.previewFillColor),
                callback=self.savePreviewFillColorCallback)

        y += self.buttonHeight + p
        self.previewGroup.previewStrokeColorLabel = TextBox(
                (x, y, -p, self.textHeight),
                'stroke color',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.previewGroup.previewStrokeColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.previewStrokeColor),
                callback=self.saveStrokeColorCallback)

        y += self.buttonHeight + p
        self.previewGroup.previewStrokeWidthLabel = TextBox(
                (x, y, -p, self.textHeight),
                'stroke width',
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.previewGroup.previewStrokeWidth = Slider(
                (x, y, -p, self.textHeight),
                value=self.previewStrokeWidth,
                minValue=0,
                maxValue=5,
                tickMarkCount=6,
                stopOnTickMarks=True,
                callback=self.savePreviewStrokeWidthCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.previewGroupHeight = y

    def initOptionsGroup(self):

        self.optionsGroup =  Group((0, 0, -0, -0))

        x = y = p = self.padding
        self.optionsGroup.verbose = CheckBox(
                (x, y, -p, self.textHeight),
                "verbose",
                value=self.verbose,
                callback=self.saveVerboseCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.optionsGroupHeight = y

    def initAccordionView(self):
        descriptions = [
            dict(label="preview",
                view=self.previewGroup,
                size=self.previewGroupHeight,
                collapsed=False,
                canResize=False),
            dict(label="options",
                view=self.optionsGroup,
                size=self.optionsGroupHeight,
                collapsed=False,
                canResize=False),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

    # ---------
    # callbacks
    # ---------

    def savePreviewFillColorCallback(self, sender):
        color = sender.get()
        # saves color in the user preferences!
        self.previewFillColor = color
        self.updatePreview()

    def saveStrokeColorCallback(self, sender):
        color = sender.get()
        # saves color in the user preferences!
        self.previewStrokeColor = color
        self.updatePreview()

    def savePreviewStrokeWidthCallback(self, sender):
        value = sender.get()
        # saves stroke with in the user preferences!
        self.previewStrokeWidth = int(value)
        self.updatePreview()

    def saveVerboseCallback(self, sender):
        value = sender.get()
        # saves verbose setting in the user preferences!
        self.verbose = value
        self.updatePreview()

    # -------
    # methods
    # -------

    def updatePreview(self):
        UpdateCurrentGlyphView()

# -------
# testing
# -------

if __name__ == "__main__":

    PreferencesDialog()
