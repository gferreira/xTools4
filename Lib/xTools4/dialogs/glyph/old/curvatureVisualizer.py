from vanilla import CheckBox, ColorWell, Slider, TextBox
from mojo import drawingTools as ctx
from mojo.roboFont import RGlyph
from mojo.events import addObserver, removeObserver
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.curvatureVisualizer import *
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


def curvatureCombFactory(glyph, steps, scale):
    '''
    A factory function which returns curvature combs for all curve segments in a glyph.

    '''
    glyph = RGlyph(glyph).copy()
    glyph.clearComponents()
    return makeCurvatureCombGlyph(glyph, steps, scale)


class CurvatureVisualizerDialog(GlyphsDialogBase):

    '''
    A dialog to visualize the curvature of bezier contours in the current glyph.

    ::

        from hTools3.dialogs.glyph.curvatureVisualizer import CurvatureVisualizerDialog
        CurvatureVisualizerDialog()

    '''

    title = 'curvature'
    key = '%s.curvatureVisualizer' % GlyphsDialogBase.key
    settings = {
        # 'curvatureCombDraw'  : True,
        'curvatureCombColor' : (0, 1, 0, 0.5),
        'curvatureCombSteps' : 20,
        'curvatureCombScale' : 1000,
    }

    def __init__(self):
        self.height  = self.textHeight * 6
        self.height += self.buttonHeight
        self.height += self.padding * 4
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.curvatureCombColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['curvatureCombColor']))

        y += self.buttonHeight + p * 0.75
        self.w.curvatureCombScaleLabel = TextBox(
                (x, y, -p, self.textHeight),
                "scale",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.curvatureCombScale = Slider(
                (x, y, -p, self.textHeight),
                value=self.settings['curvatureCombScale'],
                minValue=500,
                maxValue=5000,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.75
        self.w.curvatureCombStepsLabel = TextBox(
                (x, y, -p, self.textHeight),
                "steps",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.curvatureCombSteps = Slider(
                (x, y, -p, self.textHeight),
                value=self.settings['curvatureCombSteps'],
                minValue=10,
                maxValue=40,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * 0.75
        self.w.selectionOnly = CheckBox(
                (x, y, -p, self.textHeight),
                "selection only",
                value=False,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "show preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.setUpBaseWindowBehavior()

        addObserver(self, "backgroundPreview", "drawBackground")
        registerRepresentationFactory(Glyph, "%s.preview" % self.key, curvatureCombFactory)

        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def curvatureCombSteps(self):
        return int(self.w.curvatureCombSteps.get())

    @property
    def curvatureCombScale(self):
        return self.w.curvatureCombScale.get()

    @property
    def curvatureCombColor(self):
        return nscolor2rgb(self.w.curvatureCombColor.get())

    @property
    def showPreview(self):
        return self.w.preview.get()

    @property
    def selectionOnly(self):
        return self.w.selectionOnly.get()

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        unregisterRepresentationFactory(Glyph, "%s.preview" % self.key)

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

        lines, shapes = g.getRepresentation("%s.preview" % self.key, steps=self.curvatureCombSteps, scale=self.curvatureCombScale)

        visualizer = SegmentCurvatureVisualizer(ctx)
        visualizer.curvatureCombColor = self.curvatureCombColor
        visualizer.curvatureCombStrokeWidth  = 1 * s
        visualizer.curvatureCombStrokeWidth2 = 2 * s

        for ci, contour in enumerate(g.contours):
            for si, segment in enumerate(contour.segments):

                if self.selectionOnly and not segment.selected:
                    continue

                if not si < len(lines[ci]):
                    continue
                if not si < len(shapes[ci]):
                    continue

                segmentLines  = lines[ci][si]
                segmentShapes = shapes[ci][si]
                visualizer._drawCurvatureComb(segmentLines, segmentShapes)

# -------
# testing
# -------

if __name__ == '__main__':

    CurvatureVisualizerDialog()
