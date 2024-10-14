import os, shutil
from vanilla import Button, CheckBox, FloatingWindow, TextBox, List
from mojo.roboFont import CurrentFont, NewFont, OpenFont
from mojo.UI import GetFolder
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from xTools4.dialogs.old import hDialog
from xTools4.modules.messages import noFontOpen, showMessage
from xTools4.modules.fontutils import markGlyphs


class ExportLayersDialog(hDialog, BaseWindowController):

    title = 'layers'
    key = '%s.font.exportLayers' % hDialog.key
    settings = {}

    def __init__(self):
        self.height  = self.textHeight * 8
        self.height += self.padding * 4
        self.w = self.window(
            (self.width, self.height), self.title,
            maxSize=(self.width*1.5, self.height*2),
            minSize=(self.width, self.height))
        
        x = y = p = self.padding
        self.w.fontName = TextBox(
            (x, y, -p, self.textHeight),
            '',
            sizeStyle=self.sizeStyle)

        _y = -(self.textHeight + p - 2)
        self.w.openLayerFonts = CheckBox(
            (x, _y, -p, self.textHeight),
            'open font',
            sizeStyle=self.sizeStyle)

        _y -= self.textHeight
        self.w.overwriteUFO = CheckBox(
            (x, _y, -p, self.textHeight),
            'overwrite ufo',
            sizeStyle=self.sizeStyle)

        _y -= (self.textHeight + p- 5)
        self.w.exportButton = Button(
            (x, _y, -p, self.textHeight),
            'export',
            callback=self.exportLayersCallback,
            sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        _y -= p
        self.w.layersList = List(
            (x, y, -p, _y),
            [],
            allowsEmptySelection=False)

        addObserver(self, 'fontBecameCurrentCallback', "fontBecameCurrent")
        addObserver(self, 'fontDidCloseCallback', "fontDidClose")
        self.setUpBaseWindowBehavior()
        self.setFont(CurrentFont())
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedLayers(self):
        selection  = self.w.layersList.getSelection()
        layerNames = self.w.layersList.get()
        return [layerName for i, layerName in enumerate(layerNames) if i in selection]

    @property
    def openLayerFonts(self):
        return self.w.openLayerFonts.get()

    @property
    def overwriteUFO(self):
        return self.w.overwriteUFO.get()

    # -------
    # methods
    # -------

    def setFont(self, font):
        if font is None:
            self.w.layersList.set([])
            self.w.fontName.set("no font open")
        else:
            self.w.layersList.set(font.layerOrder)
            fontName = '%s %s' % (font.info.familyName, font.info.styleName)
            self.w.fontName.set(fontName)

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, 'fontBecameCurrent')
        removeObserver(self, 'fontDidClose')

    def fontBecameCurrentCallback(self, notification):
        font = notification['font']
        self.setFont(font)

    def fontDidCloseCallback(self, notitication):
        self.setFont(CurrentFont())

    def exportLayersCallback(self, sender):

        srcFont = CurrentFont()
        if srcFont is None:
            print(noFontOpen)
            return

        print('exporting selected layers to UFO...\n') 

        for layerName in self.selectedLayers:
            layer = srcFont.getLayer(layerName)

            # insert layer in new font
            dstFont = NewFont(showInterface=False)
            newLayer = dstFont.insertLayer(layer, name=layerName)

            # make layer the default and only layer
            dstFont.defaultLayer = newLayer
            # if 'foreground' in dstFont.layerOrder:
            #     dstFont.removeLayer('foreground')

            # copy selected font infos attrs from source font
            attrs = ['familyName', 'xHeight', 'capHeight', 'descender', 'ascender', 'unitsPerEm']
            for attr in attrs:
                value = getattr(srcFont.info, attr)
                setattr(dstFont.info, attr, value)
            dstFont.info.styleName = layerName
            dstFont.glyphOrder = srcFont.glyphOrder

            # get layer UFO path
            if srcFont.path is None:
                folder = GetFolder(message='Please choose a folder to save the UFO.', title='export layer')
            else:
                folder = os.path.dirname(srcFont.path)
            dstFontPath = os.path.join(folder, f'{layerName}.ufo')

            # remove existing UFO
            if os.path.exists(dstFontPath):
                if self.overwriteUFO:
                    shutil.rmtree(dstFontPath)
                else:
                    print(f'skipping, {dstFontPath} already exists.\n')

            # save layer to UFO
            if not os.path.exists(dstFontPath):
                print(f"\tsaving layer '{layerName}' to {dstFontPath}...") 
                dstFont.save(dstFontPath)

            # open exported layer font
            if self.openLayerFonts:
                print(f'\topening {dstFontPath}...') 
                dstFont.openInterface()
            else:
                dstFont.close()
                
            print()

        print('...done.\n') 

# -------
# testing
# -------

if __name__ == '__main__':

    ExportLayersDialog()

