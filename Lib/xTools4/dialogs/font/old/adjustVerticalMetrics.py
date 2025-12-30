from vanilla import Box, TextBox
from mojo.roboFont import CurrentFont, CurrentGlyph
from mojo.UI import NumberEditText
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
# from xTools4.modules.fontutils import getFontID
from xTools4.modules.messages import noFontOpen, showMessage
from xTools4.dialogs.old import hDialog
from xTools4.dialogs.old.misc.numberEditText01 import NumberEditText_01


KEY = f'{hDialog.key}.font.adjustVerticalMetrics'


class AdjustVerticalMetricsDialog(hDialog, BaseWindowController):

    '''
    A dialog to adjust a font’s dimensions interactively using sliders.

    '''

    title = "dimensions"
    key   = KEY
    col1  = 80

    vMetrics = [
        'xHeight',
        'ascender',
        'descender',
        'capHeight',
        'unitsPerEm',
        'italicAngle',
    ]

    def __init__(self):
        self.font = self.getCurrentFont()

        self.height  = self.textHeight * len(self.vMetrics)
        self.height += self.padding * (len(self.vMetrics) + 1)
        self.width  *= 1.2
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        # self.w.box = Box((x, y, -p, self.textHeight * 1.2))
        # self.w.box.text = TextBox((5, 0, -p, self.textHeight), '', sizeStyle=self.sizeStyle)

        self.controls = {}
        for vMetric in self.vMetrics:
            self.controls[vMetric] = {}
            self.controls[vMetric]['label'] = TextBox(
                    (x, y, self.col1, self.textHeight),
                    vMetric,
                    sizeStyle=self.sizeStyle)
            NumberInputClass = NumberEditText_01 if vMetric == 'italicAngle' else NumberEditText
            allowFloat = True if vMetric == 'italicAngle' else False
            self.controls[vMetric]['value'] = NumberInputClass(
                    (x + self.col1, y, -p, self.textHeight),
                    text='',
                    callback=self.setVMetricsCallback,
                    allowFloat=allowFloat,
                    sizeStyle=self.sizeStyle,
                    continuous=False)
            y += self.textHeight + p

        for vMetric in self.controls.keys():
            setattr(self.w, '%sLabel' % vMetric, self.controls[vMetric]['label'])
            setattr(self.w, '%sValue' % vMetric, self.controls[vMetric]['value'])
            # setattr(self, vMetric, property(lambda self: getattrcontrols[vMetric]['value'].get()))

        addObserver(self, 'fontBecameCurrentCallback', "fontBecameCurrent")
        addObserver(self, 'fontDidCloseCallback', "fontDidClose")

        self.w.workspaceWindowIdentifier = KEY

        self.setUpBaseWindowBehavior()
        self.loadFontValues()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def xHeight(self):
        return self.controls['xHeight']['value'].get()

    @property
    def ascender(self):
        return self.controls['ascender']['value'].get()

    @property
    def descender(self):
        return self.controls['descender']['value'].get()

    @property
    def capHeight(self):
        return self.controls['capHeight']['value'].get()

    @property
    def unitsPerEm(self):
        return self.controls['unitsPerEm']['value'].get()

    @property
    def italicAngle(self):
        return self.controls['italicAngle']['value'].get()

    # -------
    # methods
    # -------

    def loadFontValues(self):
        # self.w.box.text.set(getFontID(self.font))
        if self.font is None:
            for vMetric in self.vMetrics:
                slider = self.controls[vMetric]['value']
                slider.set('')
        else:
            for vMetric in self.vMetrics:
                value = getattr(self.font.info, vMetric)
                value = 0 if value is None else abs(int(value))
                self.controls[vMetric]['value'].set(value)

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, 'fontBecameCurrent')
        removeObserver(self, 'fontDidClose')

    def fontBecameCurrentCallback(self, notification):
        font = notification['font']
        self.font = font
        self.loadFontValues()

    def fontDidCloseCallback(self, notitication):
        self.font = CurrentFont()
        self.loadFontValues()

    def setVMetricsCallback(self, sender):
        if not self.font:
            return
        for vMetric in self.vMetrics:
            value = getattr(self, vMetric)
            if vMetric in ['descender', 'italicAngle']:
                value = -value
            setattr(self.font.info, vMetric, value)

# -------
# testing
# -------

if __name__ == '__main__':

    AdjustVerticalMetricsDialog()
