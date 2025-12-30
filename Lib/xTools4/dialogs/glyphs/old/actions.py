import AppKit
from vanilla import Group, CheckBox, Button, List, RadioGroup, EditText, ColorWell
from mojo import drawingTools as ctx
from mojo.events import removeObserver
from mojo.roboFont import RGlyph
from mojo.pens import DecomposePointPen
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.optimize import equalizeCurves
from xTools4.modules.fontutils import isQuadratic
from xTools4.dialogs.glyphs.old.base import GlyphsDialogBase


KEY = 'com.xTools4.dialogs.glyphs.actions'


def actionsGlyphFactory(glyph, actions=None):

    quadratic = isQuadratic(glyph.font)

    if 'decompose' not in actions:
        g = RGlyph(glyph).copy()
    else:
        g = RGlyph()
        g.width = glyph.width
        pen = g.getPointPen()
        decomposePen = DecomposePointPen(glyph.layer, pen)
        glyph.drawPoints(decomposePen)

    for action in actions:
        if action == 'balance handles':
            equalizeCurves(g, roundPos=False)
        if action == 'auto starting points':
            for contour in g.contours:
                contour.autoStartSegment()
        if action == 'correct contour direction':
            g.correctDirection(trueType=quadratic)
        if action == 'decompose':
            g.decompose()
        if action == 'round to integer':
            g.round()
        if action == 'remove overlaps':
            g.removeOverlap()
        if action == 'add extreme points':
            g.extremePoints()

    return g


class GlyphActionsDialog(GlyphsDialogBase):

    '''
    A dialog to apply actions to the selected glyphs.

    ::

        from xTools4.dialogs.glyphs.old.actions import GlyphActionsDialog
        GlyphActionsDialog()

    '''

    title = 'actions'
    key   = KEY
    settings = {
        'previewPointRadius' : 5,
    }
    actions = [
        'balance handles',
        'decompose',
        'remove overlaps',
        'add extreme points',
        'auto starting points',
        'correct contour direction',
        'round to integer',
    ]

    def __init__(self):
        self.height  = self.textHeight * (len(self.actions) + 2)
        self.height += self.padding * 4
        self.w = self.window(
            (self.width, self.height), self.title,
            maxSize=(self.width * 1.5, self.height+16),
            minSize=(self.width, self.height+16))

        x = y = p = self.padding
        listHeight = self.textHeight * len(self.actions)
        self.w.actions = List(
                (x, y, -p, listHeight),
                self.actions,
                drawFocusRing=False,
                selectionCallback=self.updatePreviewCallback,
                selfDropSettings=dict(type="genericListPboardType",
                        operation=AppKit.NSDragOperationMove,
                        callback=self.genericDropSelfCallback),
                dragSettings=dict(type="genericListPboardType",
                        callback=self.genericDragCallback))

        y += listHeight + p
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "apply",
                callback=self.applyActionsCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.initGlyphsWindowBehaviour()
        registerRepresentationFactory(Glyph, "%s.preview" % self.key, actionsGlyphFactory)
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedActions(self):
        '''
        A list of selected actions.

        '''
        actionsSelection = self.w.actions.getSelection()
        actionsSorted    = self.w.actions.get()
        actions = []
        for i, action in enumerate(actionsSorted):
            # action is not selected
            if i not in actionsSelection:
                continue
            actions.append(action)
        # done
        return tuple(actions)

    # @property
    # def quadratic(self):
    #     '''
    #     The selected contour type (cubic or quadratic).

    #     '''
    #     return self.w.contourType.get()

    # ---------
    # callbacks
    # ---------

    def applyActionsCallback(self, sender):
        '''
        Apply actions or preflight current settings.

        '''
        self.apply()

    def windowCloseCallback(self, sender):
        '''
        Removes observers and representation factories after the window is closed.

        '''
        super().windowCloseCallback(sender)
        removeObserver(self, "drawBackground")
        removeObserver(self, "drawPreview")
        unregisterRepresentationFactory(Glyph, "%s.preview" % self.key)

    # reordering actions list

    def genericDragCallback(self, sender, indexes):
        return indexes

    def genericDropSelfCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        if not isProposal:
            indexes = [int(i) for i in sorted(dropInfo["data"])]
            indexes.sort()
            rowIndex = dropInfo["rowIndex"]
            items = sender.get()
            toMove = [items[index] for index in indexes]
            for index in reversed(indexes):
                del items[index]
            rowIndex -= len([index for index in indexes if index < rowIndex])
            for font in toMove:
                items.insert(rowIndex, font)
                rowIndex += 1
            sender.set(items)
        return True

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

        # get preview
        previewGlyph = g.getRepresentation("%s.preview" % self.key,
            actions=self.selectedActions)

        # draw preview
        if notification['notificationName'] == 'drawBackground':
            self.drawPreview(previewGlyph, s)
        else:
            self.drawPreview(previewGlyph, s, plain=True)

    # -------
    # methods
    # -------

    def drawPreview(self, glyph, previewScale, plain=False):

        ctx.save()

        if not plain:
            ctx.fill(*self.previewFillColor)
            ctx.stroke(*self.previewStrokeColor)
            ctx.strokeWidth(self.previewStrokeWidth * previewScale)
        else:
            w = h = 10000
            ctx.stroke(None)
            ctx.fill(1)
            ctx.rect(-w * previewScale, -h * previewScale, w * previewScale * 2, h * previewScale * 2)
            ctx.fill(0)

        ctx.drawGlyph(glyph)

        # draw points
        r = self.settings['previewPointRadius'] * previewScale
        ctx.fill(None)
        for contour in glyph.contours:
            # draw points
            for pt in contour.points:
                ctx.oval(pt.x - r, pt.y - r, r*2, r*2)
            # draw starting point
            for i, pt in enumerate(contour.bPoints):
                if i == 0:
                    x, y = pt.anchor
                    ctx.oval(x - r*2, y - r*2, r*4, r*4)

        ctx.restore()

    def apply(self):
        '''
        Apply actions to selected glyphs in the current font.

        '''

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

        if not len(self.selectedActions):
            print('no actions selected.\n')
            return

        # ----------
        # print info
        # ----------

        if self.verbose:
            print('applying actions:\n')
            print("\tactions:")
            for action in self.selectedActions:
                print(f"\t- {action}")
            print(f"\n\tlayers: {', '.join(layerNames)}")
            print(f"\n\tglyphs: {', '.join(glyphNames)}")
            print()

        # ----------------
        # transform glyphs
        # ----------------

        quadratic = isQuadratic(font)

        for glyphName in glyphNames:
            for layerName in layerNames:
                g = font[glyphName].getLayer(layerName)
                g.prepareUndo('actions')
                # representation does decomposition differently
                # so we need to apply the actions separately here
                for action in self.selectedActions:
                    if action == 'balance handles':
                        equalizeCurves(g, roundPos=False)
                    if action == 'auto starting points':
                        for c in g.contours:
                            c.autoStartSegment()
                    if action == 'correct contour direction':
                        g.correctDirection(trueType=quadratic)
                    if action == 'decompose':
                        g.decompose()
                    if action == 'round to integer':
                        g.round()
                    if action == 'remove overlaps':
                        g.removeOverlap()
                    if action == 'add extreme points':
                        g.extremePoints()
                g.changed()
                g.performUndo()

        # done
        font.changed()
        if self.verbose:
            print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    GlyphActionsDialog()
