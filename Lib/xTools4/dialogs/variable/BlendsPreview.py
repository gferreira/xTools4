from importlib import reload
import xTools4.modules.blendsPreview
reload(xTools4.modules.blendsPreview)

import os, time
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import Window, Button, CheckBox, TextBox, Slider, List
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont, CurrentFont, CurrentGlyph
from ufoProcessor.ufoOperator import UFOOperator
from xTools4.modules.encoding import psname2char
from xTools4.modules.sys import timer
from xTools4.modules.blendsPreview import BlendsPreview
from xTools4.dialogs.variable.GlyphMeme import tempEditModeKey


class BlendsPreviewController:

    title       = 'BlendsPreview'
    width       = 800
    height      = 600
    padding     = 10
    lineHeight  = 20
    verbose     = True
    buttonWidth = 75
    colWidth    = 123*1.4

    axesList   = []
    ignoreAxes = ['XTSP']

    designspacePath = None
    designspace     = None
    operator        = None

    def __init__(self):

        self.w = Window(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width*0.7, self.height*0.7))

        x = y = p = self.padding
        self.w.canvas = DrawView((x + self.colWidth + p, y, -p, -p))

        self.w.loadDesignspaceButton = Button(
                (x, y, self.colWidth, self.lineHeight),
                'designspace…',
                callback=self.loadDesignspaceCallback,
                sizeStyle='small')

        y += self.lineHeight + p
        tableHeight = self.lineHeight * 5
        self.w.axesList = List(
            (x, y, self.colWidth, tableHeight),
            [],
            columnDescriptions=[{"title": "axis", "width": 40,}, {"title": "values"}],
        )

        y += tableHeight + p
        self.w.loadReferenceFontButton = Button(
                (x, y, self.colWidth, self.lineHeight),
                'reference font…',
                callback=self.loadReferenceFontCallback,
                sizeStyle='small')

        y += self.lineHeight + p
        self.w.compare = CheckBox(
            (x+3, y, self.colWidth, self.lineHeight),
            'compare',
            value=False,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        y += self.lineHeight
        self.w.margins = CheckBox(
            (x+3, y, self.colWidth, self.lineHeight),
            'margins',
            value=True,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        y += self.lineHeight
        self.w.wireframe = CheckBox(
            (x+3, y, self.colWidth, self.lineHeight),
            'points',
            value=False,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        y += self.lineHeight
        self.w.labels = CheckBox(
            (x+3, y, self.colWidth, self.lineHeight),
            'labels',
            value=True,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        y += self.lineHeight
        self.w.levels = CheckBox(
            (x+3, y, self.colWidth, self.lineHeight),
            'levels',
            value=False,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        y += self.lineHeight
        self.w.levelsShowLabel = TextBox(
            (x, y + 4, self.colWidth/2, self.lineHeight),
            'show levels',
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        self.w.levelsShow = Slider(
            (x+self.colWidth/2, y, self.colWidth/2, self.lineHeight),
            minValue=1,
            maxValue=4,
            value=2,
            tickMarkCount=4,
            stopOnTickMarks=True,
            # callback=self.updatePreviewCallback,
            sizeStyle='small')

        y = -(self.lineHeight*2 + p*1.5)
        self.w.updatePreviewButton = Button(
                (x, y, self.colWidth, self.lineHeight),
                'update preview',
                callback=self.updatePreviewCallback,
                sizeStyle='small')

        y += self.lineHeight + p/2
        self.w.savePDFButton = Button(
                (x, y, self.colWidth, self.lineHeight),
                'save pdf…',
                callback=self.savePDFCallback,
                sizeStyle='small')

        # self._updatePreview()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = "BlendsPreview"
        self.w.open()

    @property
    def compare(self):
        return self.w.compare.get()

    @property
    def margins(self):
        return self.w.margins.get()

    @property
    def wireframe(self):
        return self.w.wireframe.get()

    @property
    def labels(self):
        return self.w.labels.get()

    @property
    def levels(self):
        return int(self.w.levels.get())

    @property
    def levelsShow(self):
        return self.w.levelsShow.get()

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

    def loadReferenceFontCallback(self, sender):
        self.referenceFontPath = GetFile(message='Select reference font:')
        if self.referenceFontPath is None:
            return

        if self.verbose:
            print(f'loading reference font {os.path.split(self.referenceFontPath)[-1]}... ', end='')

        self.referenceFont = OpenFont(self.referenceFontPath, showInterface=False)

        if self.verbose:
            print('done.\n')

    def updatePreviewCallback(self, sender):
        self._updatePreview()

    def savePDFCallback(self, sender):
        pass

    # methods

    def _updateAxesList(self):
        axesList = self.w.axesList.get()

        axesItems = []
        for axis in self.operator.doc.axes:
            for axisName in self.blendedAxes:
                if axisName in self.ignoreAxes:
                    continue
                if axisName == axis.name:
                    axesItems.append({
                        'axis' : axis.tag,
                        'values': f'{int(axis.minimum)} {int(axis.default)} {int(axis.maximum)}',
                    })

        self.w.axesList.set(axesItems)

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

        axesListItems = self.w.axesList.get()
        axesList = [ (item['axis'], [int(v) for v in item['values'].split()]) for item in axesListItems ]

        # make PDF proof

        B = BlendsPreview(self.designspacePath)
        B.compareFontPath = self.referenceFontPath
        B.axesList = axesList

        B.compare    = self.compare
        B.margins    = self.margins
        B.labels     = self.labels
        B.levels     = self.levels
        B.wireframe  = self.wireframe
        B.levelsShow = self.levelsShow

        B.draw(glyphName)

        # display pdf

        pdfData = DB.pdfImage()
        self.w.canvas.setPDFDocument(pdfData)



if __name__ == '__main__':

    OpenWindow(BlendsPreviewController)
