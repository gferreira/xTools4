from importlib import reload
import xTools4.modules.blendsPreview
reload(xTools4.modules.blendsPreview)

import os, time
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import Window, Button, CheckBox, TextBox, EditText, Slider, List, Group, SplitView, HorizontalLine, ColorWell
from mojo.UI import GetFile, PutFile
from mojo.roboFont import OpenWindow, CurrentFont, CurrentGlyph
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.encoding import psname2char
from xTools4.modules.sys import timer
from xTools4.modules.blendsPreview import BlendsPreview
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.dialogs.variable.GlyphMeme import tempEditModeKey

KEY = 'com.xTools4.dialogs.variable.blendsPreview'

class BlendsPreviewController:

    title       = 'BlendsPreview'
    width       = 800
    height      = 600
    padding     = 10
    lineHeight  = 20
    verbose     = True
    buttonWidth = 75

    axesList    = []
    ignoreAxes  = ['XTSP']

    designspacePath   = None
    designspace       = None
    operator          = None
    referenceFontPath = None

    def __init__(self):

        self.w = Window(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width*0.7, self.height*0.7))

        group1 = Group((0, 0, -0, -0))

        x = y = p = self.padding
        col1 = 90

        group1.loadDesignspaceButton = Button(
                (x, y, -p, self.lineHeight),
                'designspace…',
                callback=self.loadDesignspaceCallback,
                sizeStyle='small')

        y += self.lineHeight + p/2
        group1.reloadButton = Button(
                (x, y, -p, self.lineHeight),
                'reload ↺',
                callback=self.reloadCallback,
                sizeStyle='small')

        y += self.lineHeight + p
        tableHeight = self.lineHeight * 5
        group1.axesList = List(
            (x, y, -p, tableHeight),
            [],
            columnDescriptions=[
                {"title": "axis", "width": 40 },
                {"title": "values", "editable" : True },
            ],
        )

        y += tableHeight + p
        group1.loadReferenceFontButton = Button(
                (x, y, -p, self.lineHeight),
                'reference font…',
                callback=self.loadReferenceFontCallback,
                sizeStyle='small')

        y += self.lineHeight + p
        group1.compare = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'compare',
            value=False,
            sizeStyle='small')

        y += self.lineHeight
        group1.margins = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'margins',
            value=True,
            sizeStyle='small')

        y += self.lineHeight
        group1.points = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'points',
            value=False,
            sizeStyle='small')

        y += self.lineHeight
        group1.labels = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'labels',
            value=True,
            sizeStyle='small')

        y += self.lineHeight
        group1.levels = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'levels',
            value=False,
            sizeStyle='small')

        # y += self.lineHeight
        # group1.levelsShowLabel = TextBox(
        #     (x, y + 4, col1, self.lineHeight),
        #     'show levels',
        #     sizeStyle='small')

        # group1.levelsShow = Slider(
        #     (x + col1, y, -p, self.lineHeight),
        #     minValue=1,
        #     maxValue=4,
        #     value=4,
        #     tickMarkCount=4,
        #     stopOnTickMarks=True,
        #     sizeStyle='small')

        y += self.lineHeight + p
        group1.line1 = HorizontalLine((x, y, -p, 1))

        y += p
        group1.monovar = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'monovar',
            value=True,
            sizeStyle='small')

        y += self.lineHeight
        group1.duovars = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'duovars',
            value=True,
            sizeStyle='small')

        y += self.lineHeight
        group1.trivars = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'trivars',
            value=True,
            sizeStyle='small')

        y += self.lineHeight
        group1.quadravars = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'quadvars',
            value=True,
            sizeStyle='small')

        y += self.lineHeight + p
        group1.line2 = HorizontalLine((x, y, -p, 1))

        y += p
        group1.header = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'header',
            value=True,
            sizeStyle='small')

        y += self.lineHeight
        group1.footer = CheckBox(
            (x+3, y, -p, self.lineHeight),
            'footer',
            value=False,
            sizeStyle='small')

        y += self.lineHeight + p
        group1.line3 = HorizontalLine((x, y, -p, 1))

        y += p
        group1.updatePreviewButton = Button(
                (x, y, -p, self.lineHeight),
                'update preview',
                callback=self.updatePreviewCallback,
                sizeStyle='small')

        y += self.lineHeight + p/2
        group1.savePDFButton = Button(
                (x, y, -p, self.lineHeight),
                'save pdf…',
                callback=self.savePDFCallback,
                sizeStyle='small')

        group2 = Group((0, 0, -0, -0))
        x = p = self.padding
        y = 0
        group2.canvas = DrawView((x, y, -p, -p))

        self._groups = [
            dict(view=group1, identifier="pane1", size=123*2, minSize=123*1.5, maxSize=123*2.5, canCollapse=False),
            dict(view=group2, identifier="pane2", canCollapse=False),
        ]
        self.w.splitView = SplitView((0, 0, -0, -0), self._groups, dividerStyle='thin')

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    @property
    def _group1(self):
        return self._groups[0]['view']

    @property
    def _group2(self):
        return self._groups[1]['view']

    @property
    def compare(self):
        return self._group1.compare.get()

    @property
    def margins(self):
        return self._group1.margins.get()

    @property
    def points(self):
        return self._group1.points.get()

    @property
    def labels(self):
        return self._group1.labels.get()

    @property
    def levels(self):
        return int(self._group1.levels.get())

    @property
    def header(self):
        return int(self._group1.header.get())

    @property
    def footer(self):
        return int(self._group1.footer.get())

    @property
    def levelsShow(self):
        levels = []
        if self._group1.monovar.get():
            levels.append(1)
        if self._group1.duovars.get():
            levels.append(2)
        if self._group1.trivars.get():
            levels.append(3)
        if self._group1.quadravars.get():
            levels.append(4)
        return levels # self._group1.levelsShow.get()

    @property
    def parametricAxes(self):
        return self.operator.doc.default.location.keys()

    @property
    def blendedAxes(self):
        allAxes = [axis.name for axis in self.operator.doc.axes]
        return list(set(allAxes).difference(set(self.parametricAxes)))

    # callbacks

    def loadDesignspaceCallback(self, sender):
        self.designspacePath = GetFile(message='Select designspace file:')
        if self.designspacePath is None:
            return

        if self.verbose:
            print(f'loading designspace from {os.path.split(self.designspacePath)[-1]}... ', end='')

        if self.verbose:
            print('done.\n')

        # initiate operator
        self.operator = UFOOperator()
        self.operator.read(self.designspacePath)
        self.operator.loadFonts()

        self._updateAxesList()

    def reloadCallback(self, sender):
        if not self.operator:
            return
        self.operator.read(self.designspacePath)
        self.operator.loadFonts()

        self._updateAxesList()

    def loadReferenceFontCallback(self, sender):
        self.referenceFontPath = GetFile(message='Select reference font:')
        if not self.referenceFontPath:
            return

        if self.verbose:
            print(f'loading reference font {os.path.split(self.referenceFontPath)[-1]}... ', end='')

        self._group1.compare.set(True)

        if self.verbose:
            print('done.\n')

    def updatePreviewCallback(self, sender):
        self._updatePreview()

    def savePDFCallback(self, sender):
        pdfPath = PutFile(message="Choose a location for this PDF", fileName="blending-preview.pdf")
        if not pdfPath:
            return
        DB.saveImage(pdfPath)

    # methods

    def _updateAxesList(self):
        axesItems = []
        for axis in self.operator.doc.axes:
            for axisName in self.blendedAxes:
                if axisName in self.ignoreAxes or axisName.startswith('TN'):
                    continue
                if axisName == axis.name:
                    axesItems.append({
                        'axis' : axis.tag,
                        'values': f'{int(axis.minimum)} {int(axis.default)} {int(axis.maximum)}',
                    })

        self._group1.axesList.set(axesItems)

    def _updatePreview(self):

        if not self.designspacePath:
            return

        font = CurrentFont()
        if font is None:
            return

        glyph = CurrentGlyph()
        if glyph is not None:
            if font.lib.get(tempEditModeKey) == 'glyphs':
                glyphName = glyph.name[:glyph.name.rfind('.')]
            else:
                glyphName = glyph.name
        else:
            if len(font.selectedGlyphs):
                glyphName = font.selectedGlyphs[0].name
                if font.lib.get(tempEditModeKey) == 'glyphs':
                    glyphName = glyphName[:glyphName.rfind('.')]
            else:
                glyphName = None

        axesListItems = self._group1.axesList.get()
        axesList = [ (item['axis'], [int(v) for v in item['values'].split()]) for item in axesListItems ]

        # make PDF proof

        B = BlendsPreview(self.designspacePath)
        B.compareFontPath = self.referenceFontPath
        B.axesList = axesList

        for attr in [
                'compare',
                'margins',
                'labels',
                'levels',
                'levelsShow',
                'points',
                'header',
                'footer',
            ]:
            setattr(B, attr, getattr(self, attr))

        B.draw(glyphName)

        # display pdf

        pdfData = DB.pdfImage()
        self._group2.canvas.setPDFDocument(pdfData)



if __name__ == '__main__':

    OpenWindow(BlendsPreviewController)
