from vanilla import TextBox, List
from mojo.events import addObserver, removeObserver
from mojo.roboFont import CurrentFont
from defconAppKit.windows.baseWindow import BaseWindowController
from xTools4.dialogs.old import hDialog

KEY = 'com.xTools4.dialogs.glyphs.modifiersLayers'
class SelectLayersDialog(hDialog, BaseWindowController):

    title      = "layers"
    key        = f'{hDialog.key}.glyphs.layersSelect'
    windowType = 0

    def __init__(self):
        self.height = self.textHeight * 8 + self.padding * 2 + 5
        self.w = self.window(
            (self.width, self.height), self.title,
            maxSize=(self.width, self.height * 1.5),
            minSize=(self.width, self.height))
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        self.w.fontName = TextBox(
                (x, y, -p, self.textHeight),
                '',
                sizeStyle=self.sizeStyle)

        y += self.textHeight + 5
        self.w.list = List(
                (x, y, -p, -p),
                [],
                allowsEmptySelection=True,
                drawFocusRing=False,
                rowHeight=self.buttonNudge)

        addObserver(self, 'fontBecameCurrentCallback', "fontBecameCurrent")
        addObserver(self, 'fontDidCloseCallback',      "fontDidClose")

        self.setUpBaseWindowBehavior()
        self.setFont(CurrentFont())

        self.w.vanillaWrapper = self
        self.openWindow()

    def windowCloseCallback(self, sender):
        removeObserver(self, 'fontBecameCurrent')
        removeObserver(self, 'fontDidClose')
        del self.w.vanillaWrapper
        super().windowCloseCallback(sender)

    def fontBecameCurrentCallback(self, notification):
        font = notification['font']
        self.setFont(font)

    def fontDidCloseCallback(self, notitication):
        font = CurrentFont()
        self.setFont(font)

    def setFont(self, font):
        if font is None:
            self.w.list.set([])
            self.w.fontName.set("(no font open)")
        else:
            self.w.list.set(font.layerOrder)
            for i, layerName in enumerate(font.layerOrder):
                if layerName == font.defaultLayer.name:
                    self.w.list.setSelection([i])
            fontName = f'{font.info.familyName} {font.info.styleName}'
            self.w.fontName.set(fontName)


if __name__ == "__main__":

    SelectLayersDialog()
