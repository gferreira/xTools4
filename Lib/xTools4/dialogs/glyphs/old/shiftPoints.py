from vanilla import TextBox, RadioGroup, Button, CheckBox
from mojo import drawingTools as ctx
from mojo.UI import getDefault, NumberEditText
from xTools4.modules.glyphutils import deselectPoints, selectPointsLine, shiftSelectedPoints
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


### WARNING: THIS TOOL CURRENTLY CRASHES RF4.5b (NOT SURE WHY)

KEY = 'com.xTools4.shiftPoints'
class ShiftPointsDialog(GlyphsDialogBase):

    title = 'shift'
    key   = f'{GlyphsDialogBase.key}.pointsShift'
    settings = {
        'axis'      : 1,
        'side'      : 1,
        'pos'       : 250,
        'delta'     : 100,
        'direction' : 1,
    }
    glyphNames = []

    def __init__(self):
        self.height  = self.textHeight * 7
        self.height += self.padding * 7.3
        self.w = self.window((self.width, self.height), self.title)
        self.w.workspaceWindowIdentifier = KEY

        x = y = p = self.padding
        col = (self.width - p * 2) * 0.5
        self.w.posLabel = TextBox(
                (x, y, col, self.textHeight),
                'pos',
                sizeStyle=self.sizeStyle)
        self.w.posValue = NumberEditText(
                (col, y, -p, self.textHeight),
                text=self.settings['pos'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.axisLabel = TextBox(
                (x, y, col, self.textHeight),
                "axis",
                sizeStyle=self.sizeStyle)
        self.w.axis = RadioGroup(
                (col, y, -p, self.textHeight),
                ["x", "y"],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.axis.set(self.settings['axis'])

        x = p
        y += self.textHeight + p * 0.5
        self.w.sideLabel = TextBox(
                (x, y, col, self.textHeight),
                "side",
                sizeStyle=self.sizeStyle)
        self.w.side = RadioGroup(
                (col, y, -p, self.textHeight),
                ["-", "+"],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.side.set(self.settings['direction'])

        y += self.textHeight + p
        self.w.deltaLabel = TextBox(
                (x, y, col, self.textHeight),
                'delta',
                sizeStyle=self.sizeStyle)
        self.w.deltaValue = NumberEditText(
                (col, y, -p, self.textHeight),
                text=self.settings['delta'],
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle,
                allowFloat=False,
                continuous=False)

        y += self.textHeight + p
        self.w.shiftDirectionLabel = TextBox(
                (x, y, col, self.textHeight),
                "shift",
                sizeStyle=self.sizeStyle)
        self.w.shiftDirection = RadioGroup(
                (col, y, -p, self.textHeight),
                ["-", "+"],
                sizeStyle=self.sizeStyle,
                callback=self.updatePreviewCallback,
                isVertical=False)
        self.w.shiftDirection.set(self.settings['side'])

        y += self.textHeight + p
        self.w.buttonApply = Button(
                (x, y, -p, self.textHeight),
                "apply",
                sizeStyle=self.sizeStyle,
                callback=self.applyCallback)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def position(self):
        return self.w.posValue.get()

    @property
    def side(self):
        return int(self.w.side.get())

    @property
    def axis(self):
        return ['x', 'y'][int(self.w.axis.get())]

    @property
    def direction(self):
        return self.w.shiftDirection.get()

    @property
    def delta(self):
        return self.w.deltaValue.get()

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if not g:
            return

        if not g.bounds:
            return

        # make preview
        previewGlyph = self.makeGlyph(g, preview=True)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)
            
    # -------
    # methods
    # -------

    def drawPreview(self, glyph, scale, plain=False):

        ctx.save()

        w = 10000
        h = 10000

        # draw glyph
        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * scale)
        else:
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * scale, -h * scale, w * scale * 2, h * scale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        # draw position
        if not plain:
            if self.axis == 'y':
                x1, x2 = -w, w
                y1 = y2 = self.position
            else:
                x1 = x2 = self.position
                y1, y2 = -h, h
            ctx.lineDash(self.previewStrokeWidth * scale, self.previewStrokeWidth * scale)
            ctx.line((x1, y1), (x2, y2))

        # done
        ctx.restore()

    def makeGlyph(self, glyph, preview=False):
        if preview:
            glyph = glyph.copy()
        # flip shift direction
        delta = self.delta
        if not self.direction:
            delta *= -1.0
        # select points
        selectPointsLine(glyph, self.position, axis=self.axis, side=self.side)
        # move points
        shiftSelectedPoints(glyph, delta, axis=self.axis)
        # done
        deselectPoints(glyph)
        return glyph

    def apply(self):

        # -----------------
        # assert conditions
        # -----------------

        font = self.getCurrentFont()
        if not font:
            return

        glyphNames = self.getGlyphNames()
        if not glyphNames:
            return

        layerNames = self.getLayerNames()
        if not layerNames:
            layerNames = [font.defaultLayer.name]

        # ----------
        # print info
        # ----------

        sides = ['left', 'right'] if self.axis == 'x' else ['down', 'up']
        directions = ['-', '+']

        if self.verbose:
            print('moving selected points:\n')
            print(f'\tposition: {self.position}')
            print(f'\taxis: {self.axis}')
            print(f'\tside: {sides[self.side]}')
            print(f'\tdistance: {self.delta}')
            print(f'\tdirection: {directions[self.direction]}')
            print(f'\tlayers: {", ".join(layerNames)}')
            print(f'\tglyphs: {", ".join(glyphNames)}')

        # ----------------
        # transform glyphs
        # ----------------

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('shift points')
                self.makeGlyph(g)
                g.changed()
                g.performUndo()

        # done
        font.changed()
        print('\n...done.\n')

# -------
# testing
# -------

if __name__ == "__main__":

    ShiftPointsDialog()
