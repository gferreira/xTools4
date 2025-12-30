from vanilla import *
from mojo.UI import AccordionView
from xTools4.dialogs.batch.base import BatchDialogBase


KEY = f'{BatchDialogBase.key}.boilerplate'


class BoilerplateBatchDialog(BatchDialogBase):

    '''
    A dummy boilerplate dialog which doesn't do anything.

    ::

        from xTools4.dialogs.batch.boilerplate import BoilerplateBatchDialog
        BoilerplateBatchDialog()

    '''

    title = 'batch something'
    key = KEY

    options = [
        'one option',
        'another option',
        'a third option',
    ]

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, self.height))

        # build groups
        self.initFontSelectorGroup()
        self.initDoSomethingGroup()

        # build accordion
        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="something",
                view=self.doSomethingSelector,
                size=self.doSomethingSelectorHeight,
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

    def initDoSomethingGroup(self):

        self.doSomethingSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding
        listHeight = 140 # self.textHeight * len(self.options)
        self.doSomethingSelector.options = List(
                (x, y, -p, listHeight),
                self.options,
                drawFocusRing=False)

        y += listHeight + p
        self.doSomethingSelector.selectAll = CheckBox(
                (x, y, -p, self.textHeight),
                "select all",
                callback=self.selectAllOptionsCallback,
                value=False,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.doSomethingSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "do something",
                callback=self.batchDoSomethingCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.doSomethingSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.doSomethingSelectorHeight = y

    # -------------
    # dynamic attrs
    # -------------

    # ...

    # ---------
    # callbacks
    # ---------

    def selectAllOptionsCallback(self, sender):
        if sender.get():
            selection = list(range(len(self.doSomethingSelector.options)))
        else:
            selection = []
        self.doSomethingSelector.options.setSelection(selection)

    def batchDoSomethingCallback(self, sender):
        if self.doSomethingSelector.preflight.get():
            self.preflight()
        else:
            self.batchDoSomething()

    # -------
    # methods
    # -------

    def preflight(self):
        self.preflightTargetFonts()

    def batchDoSomething(self):
        print('doing something...\n')

# -------
# testing
# -------

if __name__ == '__main__':

    BoilerplateBatchDialog()
