from vanilla import CheckBox, ColorWell, Slider, TextBox
from mojo import drawingTools as ctx
from mojo.roboFont import RGlyph
from mojo.events import addObserver, removeObserver
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.structureVisualizer import BezierStructureVisualizer
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase

# ---------
# factories
# ---------

def bezierStructureFactory(glyph, strokeWidth=2):
    g = RGlyph(glyph).copy()
    g.clearComponents()
    B = BezierStructureVisualizer(ctx)
    return B._structure(g)

# ------
# dialog
# ------

class StructureVisualizerDialog(GlyphsDialogBase):

    title = 'structure'
    key   = f'{GlyphsDialogBase.key}.structureVisualizer'
    settings = {
        'strokeWidth'          : 2,
        'colorCurves'          : (0.0, 0.0, 1.0),  # curves
        'colorLines'           : (0.0, 0.5, 1.0),  # lines
        'colorHandlesStraight' : (1.0, 0.0, 0.0),
        'colorHandlesSlanted'  : (1.0, 0.5, 0.0),
    }

    def __init__(self):
        self.height  = self.textHeight * 8
        self.height += self.padding * 9.5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.colorCurves = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['colorCurves']))

        y += self.buttonHeight + p * 0.75
        self.w.colorLines = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['colorLines']))

        y += self.buttonHeight + p * 0.75
        self.w.previewSegments = CheckBox(
                (x, y, -p, self.textHeight),
                "segments",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.75
        self.w.colorHandlesStraight = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['colorHandlesStraight']))

        y += self.buttonHeight + p * 0.75
        self.w.colorHandlesSlanted = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['colorHandlesSlanted']))

        y += self.buttonHeight + p*0.75
        self.w.previewHandles = CheckBox(
                (x, y, -p, self.textHeight),
                "handles",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p

        valueMin  = 1
        valueMax  = 8
        tickCount = valueMax - valueMin
        self.w.strokeWidth = Slider(
                (x, y, -p, self.textHeight),
                value=self.settings['strokeWidth'],
                minValue=valueMin,
                maxValue=valueMax,
                tickMarkCount=tickCount,
                stopOnTickMarks=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "show preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.setUpBaseWindowBehavior()

        addObserver(self, "backgroundPreview", "drawBackground")
        registerRepresentationFactory(Glyph, f"{self.key}.preview", bezierStructureFactory)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def strokeWidth(self):
        return int(self.w.strokeWidth.get())

    @property
    def colorCurves(self):
        return nscolor2rgb(self.w.colorCurves.get())
    
    @property
    def colorLines(self):
        return nscolor2rgb(self.w.colorLines.get())
    
    @property
    def colorHandlesStraight(self):
        return nscolor2rgb(self.w.colorHandlesStraight.get())
    
    @property
    def colorHandlesSlanted(self):
        return nscolor2rgb(self.w.colorHandlesSlanted.get())

    @property
    def showSegments(self):
        return self.w.previewSegments.get()

    @property
    def showHandles(self):
        return self.w.previewHandles.get()
    
    @property
    def showPreview(self):
        return self.w.preview.get()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        unregisterRepresentationFactory(Glyph, f"{self.key}.preview")

    # ---------
    # observers
    # ---------

    def backgroundPreview(self, notification):

        g = notification['glyph']
        s = notification['scale']

        # assert conditions

        if not self.w.preview.get():
            return

        if g is None:
            return

        # draw preview
        lineSegments, curveSegments, handlesStraight, handlesSlanted = g.getRepresentation(f"{self.key}.preview")

        ctx.save()
        ctx.fill(None)
        ctx.strokeWidth(self.strokeWidth*s)
        ctx.lineCap('round')

        if self.showHandles:
            ctx.stroke(*self.colorHandlesStraight)
            for p1, p2 in handlesStraight:
                ctx.newPath()
                ctx.moveTo(p1)
                ctx.lineTo(p2)
                ctx.drawPath()

            ctx.stroke(*self.colorHandlesSlanted)
            for p1, p2 in handlesSlanted:
                ctx.newPath()
                ctx.moveTo(p1)
                ctx.lineTo(p2)
                ctx.drawPath()

        if self.showSegments:
            ctx.stroke(*self.colorCurves)
            for p1, p2 in lineSegments:
                ctx.newPath()
                ctx.moveTo(p1)
                ctx.lineTo(p2)
                ctx.drawPath()

            ctx.stroke(*self.colorLines)
            for p1, p2, p3, p4 in curveSegments:
                ctx.newPath()
                ctx.moveTo(p1)
                ctx.curveTo(p2, p3, p4)
                ctx.drawPath()
        
        ctx.restore()

# -------
# testing
# -------

if __name__ == '__main__':

    StructureVisualizerDialog()
