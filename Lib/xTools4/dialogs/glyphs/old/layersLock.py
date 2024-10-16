from vanilla import Button, CheckBox
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo import drawingTools as ctx
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from xTools4.dialogs.old import hDialog


class LockLayerWidthsDialog(hDialog, BaseWindowController):

    '''
    A dialog to enable selective locking/unlocking of glyph widths across layers.

    ::

        from xTools4.dialogs.glyphs.old.layersLock import LockLayerWidthsDialog
        LockLayerWidthsDialog()

    '''

    title = 'widths'
    key   = f'{hDialog.key}.glyphs.layers.lock'
    # windowType = 1

    def __init__(self):
        self.height  = self.textHeight * 3
        self.height += self.padding * 4 -2
        self.w = self.window((self.width, self.height), title=self.title)

        x = y = p = self.padding
        self.w.lockLayers = Button(
                (x, y, -p, self.textHeight),
                'lock',
                callback=self.lockGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.unlockLayers = Button(
                (x, y, -p, self.textHeight),
                'unlock',
                callback=self.unlockGlyphsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.showPreview = CheckBox(
                (x, y, -p, self.textHeight),
                "show icon",
                value=True,
                callback=self.previewCallback,
                sizeStyle=self.sizeStyle)

        self.setUpBaseWindowBehavior()
        addObserver(self, "drawCallback",     "drawBackground")
        addObserver(self, "drawCallback",     "spaceCenterDraw")
        addObserver(self, "drawCellCallback", "glyphCellDrawBackground")

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def preview(self):
        return self.w.showPreview.get()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "spaceCenterDraw")
        removeObserver(self, "glyphCellDrawBackground")

    def previewCallback(self, sender):
        UpdateCurrentGlyphView()

    def drawCellCallback(self, info):

        if not self.preview:
            return

        glyph = info["glyph"]
        font = glyph.font

        # get glyph lock status
        lockStatus = False
        if self.key in font.lib:
            if glyph.name in font.lib[self.key]:
                lockStatus = font.lib[self.key][glyph.name]

        if lockStatus:
            lockStatusText = '🔒'
            ctx.fontSize(12)
            ctx.text(lockStatusText, (2, 2))

    def drawCallback(self, notification):

        if not self.preview:
            return

        glyph = notification['glyph']
        scale = notification['scale']

        font = glyph.font

        # get glyph lock status
        lockStatus = False
        if self.key in font.lib:
            if glyph.name in font.lib[self.key]:
                lockStatus = font.lib[self.key][glyph.name]

        # copy width to all other layers
        if lockStatus:
            for layerName in font.layerOrder:
                layerGlyph = glyph.getLayer(layerName)
                layerGlyph.width = glyph.width

        # draw lock status in canvas
        if lockStatus:
            lockStatusText = '🔒'
            ctx.save()

            if 'spaceCenter' in notification:
                if scale < 20:
                    w, h = ctx.textSize(lockStatusText)
                    ctx.fontSize(12 * scale)
                    ctx.translate(glyph.width, 0)
                    ctx.rotate(180)
                    ctx.text(lockStatusText, (24, 28))
            else:
                ctx.fontSize(16 * scale)
                ctx.text(lockStatusText, (glyph.width - 28*scale, -28*scale))

            ctx.restore()

    def lockGlyphsCallback(self, sender):
        self.setLockStatus(True)
        UpdateCurrentGlyphView()

    def unlockGlyphsCallback(self, sender):
        self.setLockStatus(False)
        UpdateCurrentGlyphView()

    # -------
    # methods
    # -------

    def setLockStatus(self, value):

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        # get glyphName: lockStatus dict
        lockGlyphsDict = {}
        if self.key in font.lib:
            lockGlyphsDict = font.lib[self.key]

        # set lock status for selected glyphs
        for glyphName in glyphNames:
            if self.verbose:
                if value:
                    print(f'locking layer widths ({glyphName})...')
                else:
                    print(f'unlocking layer widths ({glyphName})...')
            lockGlyphsDict[glyphName] = value

        # save glyph lock dict in font lib
        font.lib[self.key] = lockGlyphsDict

        # update glyphs
        for glyphName in glyphNames:
            font[glyphName].changed()

# -------
# testing
# -------

if __name__ == '__main__':

    D = LockLayerWidthsDialog()
