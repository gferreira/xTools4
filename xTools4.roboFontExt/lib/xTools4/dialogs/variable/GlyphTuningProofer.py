import os, time
import AppKit
import drawBot as DB
from vanilla import *
from fontTools.designspaceLib import DesignSpaceDocument
from drawBot.ui.drawView import DrawView
from mojo.UI import GetFile, GetFolder
from mojo.roboFont import OpenWindow, OpenFont
from mojo.smartSet import readSmartSets
from xTools4.modules.measurements import readMeasurements
from xTools4.modules.tuningPreview import TuningPreview
from xTools4.modules.xprojectLib import smartSetsPathKey, measurementsPathKey


KEY = 'com.xTools4.dialogs.variable.glyphTuningProofer'


class GlyphTuningProoferController:

    title      = 'GlyphTuningProofer'
    width      = 800
    height     = 600
    padding    = 10
    lineHeight = 22
    verbose    = True

    designspacePath  = None
    measurementsPath = None
    smartSetsPath    = None

    def __init__(self):

        self.w = Window(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width*0.7, self.height*0.7))

        group1 = Group((0, 0, -0, -0))

        x = y = p = self.padding
        col1 = 90

        group1.getDesignspaceButton = Button(
                (x, y, -p, self.lineHeight),
                'designspace…',
                callback=self.getDesignspaceCallback,
            )

        y += self.lineHeight + p
        group1.reloadButton = Button(
                (x, y, -p, self.lineHeight),
                'reload ↺',
                callback=self.reloadCallback,
            )

        y += self.lineHeight + p
        group1.line = HorizontalLine((x, y, -p, 1))

        y += p + 1
        group1.caseSelector = PopUpButton((x, y, -p, self.lineHeight),
                [],
                callback=self.caseSelectorCallback,
            )

        y += self.lineHeight + p
        group1.groupSelector = PopUpButton((x, y, -p, self.lineHeight),
                [],
                callback=self.groupSelectorCallback,
            )

        y += self.lineHeight + p
        group1.glyphSelector = PopUpButton((x, y, -p, self.lineHeight),
                [],
                # callback=self.glyphSelectorCallback,
            )

        y += self.lineHeight + p
        group1.duovars = CheckBox(
                (x, y, -p, self.lineHeight),
                'duovars',
                value=True)

        y += self.lineHeight
        group1.trivars = CheckBox(
                (x, y, -p, self.lineHeight),
                'trivars',
                value=False,
            )

        y += self.lineHeight
        group1.quadvars = CheckBox(
                (x, y, -p, self.lineHeight),
                'quadvars',
                value=False,
            )

        y = -self.lineHeight*2 - p*2
        group1.makeProof = Button(
                (x, y, -p, self.lineHeight),
                'make proof',
                callback=self.makeProofCallback
            )

        y = -self.lineHeight*1 - p*1
        group1.savePDF = Button(
                (x, y, -p, self.lineHeight),
                'save PDF…',
                callback=self.savePDFCallback
            )

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
    def familyName(self):
        if self.defaultFont is None:
            return
        return self.defaultFont.info.familyName

    @property
    def sourcesFolder(self):
        return os.path.dirname(self.designspacePath)

    @property
    def measurementsPath(self):
        relativePath = self.designspace.lib.get(measurementsPathKey)
        if relativePath:
            return os.path.normpath(os.path.join(self.sourcesFolder, relativePath))

    @property
    def smartSetsPath(self):
        relativePath = self.designspace.lib.get(smartSetsPathKey)
        if relativePath:
            return os.path.normpath(os.path.join(self.sourcesFolder, relativePath))

    def getDesignspaceCallback(self, sender):

        designspacePath = GetFile(
            message='Select designspace file:',
            title=self.title, 
            allowsMultipleSelection=False,
            fileTypes=["designspace"]
        )
        if designspacePath is None:
            return
        self.designspacePath = designspacePath
        self._loadDesignspace()

    def caseSelectorCallback(self, sender):
        group = self._groups[0]['view']
        selectedCase = group.caseSelector.getItem()
        if selectedCase is None:
            return
        if not self.smartSets:
            return
        group.groupSelector.setItems(self.smartSets[selectedCase])
        self.groupSelectorCallback(None)

    def groupSelectorCallback(self, sender):
        group = self._groups[0]['view']
        selectedCase = group.caseSelector.getItem()
        selectedGroup = group.groupSelector.getItem()
        if selectedCase is None or selectedGroup is None:
            return
        if not self.smartSets:
            return
        group.glyphSelector.setItems(self.smartSets[selectedCase][selectedGroup])
        # self.glyphSelectorCallback(None)

    # def glyphSelectorCallback(self, sender):
    #     group = self._groups[0]['view']
    #     self.glyphName = group.glyphSelector.getItem()

    def reloadCallback(self, sender):
        self._loadDesignspace()

    def makeProofCallback(self, sender):

        group = self._groups[0]['view']
        glyphName = group.glyphSelector.getItem()

        DB.newDrawing()

        referenceSource = self.designspace.default.path

        self.proofer = TuningPreview(self, referenceSource)
        self.proofer.draw(glyphName, level=1)

        pdfData = DB.pdfImage()

        group = self._groups[1]['view']
        group.canvas.setPDFDocument(pdfData)

    def savePDFCallback(self, sender):

        print('saving...\n')

        # proofsFolder = GetFolder(message="Choose a folder to save this PDF")
        # if not proofsFolder:
        #     return

        # familyName = os.path.splitext(os.path.split(self.designspace.path)[-1])[0]

        # self.proofer.save(proofsFolder, familyName)

    def _loadDesignspace(self):

        if self.verbose:
            print(f'loading designspace from {os.path.split(self.designspacePath)[-1]}... ', end='')

        self.designspace = DesignSpaceDocument()
        self.designspace.read(self.designspacePath)
        self.defaultFont = OpenFont(self.designspace.default.path, showInterface=False)

        if self.verbose:
            print('done.\n')

        self._loadMeasurements()
        self._loadSmartSets()

    def _loadMeasurements(self):

        if self.verbose:
            print(f'loading measurements from {os.path.split(self.measurementsPath)[-1]}... ', end='')

        measurements = readMeasurements(self.measurementsPath)
        print(measurements.keys())
        self.measurements = measurements['glyphs']

        if self.verbose:
            print('done.\n')

    def _loadSmartSets(self):

        if self.verbose:
            print(f'loading glyph groups from {os.path.split(self.smartSetsPath)[-1]}... ', end='')

        smartSetsRaw = readSmartSets(self.smartSetsPath, useAsDefault=False, font=None)

        self.smartSets = {}
        for smartGroup in smartSetsRaw:
            self.smartSets[smartGroup.name] = {}
            if smartGroup.groups:
                for smartSet in smartGroup.groups:
                    self.smartSets[smartGroup.name][smartSet.name] = smartSet.glyphNames
            else:
                self.smartSets[smartGroup.name] = smartGroup.glyphNames

        group = self._groups[0]['view']

        group.caseSelector.setItems(self.smartSets.keys())
        self.caseSelectorCallback(None)

        if self.verbose:
            print('done.\n')


if __name__ == '__main__':

    OpenWindow(GlyphTuningProoferController)
