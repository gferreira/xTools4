from importlib import reload
import xTools4.modules.glyphMemeProofer
reload(xTools4.modules.glyphMemeProofer)

import os, time
import AppKit
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import *
from mojo.UI import GetFile, GetFolder
from mojo.roboFont import OpenWindow
from mojo.smartSet import readSmartSets
from fontTools.designspaceLib import DesignSpaceDocument
from fontParts.world import OpenFont
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.xproject import measurementsPathKey, smartSetsPathKey
from xTools4.modules.glyphMemeProofer import GlyphMemeProofer


KEY = 'com.xTools4.dialogs.variable.glyphMemeProofer'


class GlyphMemeProoferController:

    title      = 'GlyphMemeProofer'
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
                sizeStyle='small')

        y += self.lineHeight + p/2
        group1.reloadButton = Button(
                (x, y, -p, self.lineHeight),
                'reload ↺',
                callback=self.reloadCallback,
                sizeStyle='small'
            )

        y += self.lineHeight + p
        group1.groupSelector = PopUpButton((x, y, -p, self.lineHeight),
                [],
                callback=self.groupSelectorCallback
            )

        y += self.lineHeight + p
        group1.glyphSelector = PopUpButton((x, y, -p, self.lineHeight),
                [],
                callback=self.glyphSelectorCallback
            )

        y += self.lineHeight + p
        group1.glyphMeme = List(
                (x, y, -p, -self.lineHeight*2 - p*2.5),
                [],
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                enableDelete=False,
            )

        y = -self.lineHeight*2 - p*1.5
        group1.makeProof = Button(
                (x, y, -p, self.lineHeight),
                'make proof',
                sizeStyle='small',
                callback=self.makeProofCallback
            )

        y = -self.lineHeight*1 - p*1
        group1.savePDF = Button(
                (x, y, -p, self.lineHeight),
                'save PDF…',
                sizeStyle='small',
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
        fileName = self.designspace.lib.get(measurementsPathKey)
        if fileName:
            return os.path.join(self.sourcesFolder, fileName)

    @property
    def smartSetsPath(self):
        fileName = self.designspace.lib.get(smartSetsPathKey)
        if fileName:
            return os.path.join(self.sourcesFolder, fileName)

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

    def groupSelectorCallback(self, sender):
        group = self._groups[0]['view']
        selectedGroup = group.groupSelector.getItem()
        group.glyphSelector.setItems(self.glyphGroups[selectedGroup])
        self.glyphSelectorCallback(None)

    def glyphSelectorCallback(self, sender):
        group = self._groups[0]['view']
        glyphName = group.glyphSelector.getItem()
        measurementsDict = self.measurements.get(glyphName, {})
        measurements = sorted(list(set([m['name'] for m in measurementsDict.values()])))
        group.glyphMeme.set(measurements)
        group.glyphMeme.setSelection(range(len(measurements)))

    def reloadCallback(self, sender):
        self._loadDesignspace()

    def makeProofCallback(self, sender):

        group = self._groups[0]['view']
        glyphName = group.glyphSelector.getItem()

        DB.newDrawing()

        self.proofer = GlyphMemeProofer(glyphName, self.designspacePath)
        # self.proofer.anchorsDraw = False
        self.proofer.draw()

        pdfData = DB.pdfImage()

        group = self._groups[1]['view']
        group.canvas.setPDFDocument(pdfData)

    def savePDFCallback(self, sender):

        proofsFolder = GetFolder(message="Choose a folder to save this PDF")
        if not proofsFolder:
            return

        familyName = os.path.splitext(os.path.split(self.designspace.path)[-1])[0]

        self.proofer.save(proofsFolder, familyName)

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
        self.measurements = measurements['glyphs']

        if self.verbose:
            print('done.\n')

    def _loadSmartSets(self):

        if self.verbose:
            print(f'loading glyph groups from {os.path.split(self.smartSetsPath)[-1]}... ', end='')

        smartSets = readSmartSets(self.smartSetsPath, useAsDefault=False, font=None)

        self.glyphGroups = {}
        for smartGroup in smartSets:
            if not smartGroup.groups:
                continue
            for smartSet in smartGroup.groups:
                # remove component glyphs from glyph lists
                glyphNames = []
                for glyphName in smartSet.glyphNames:
                    if glyphName not in self.defaultFont:
                        continue
                    g = self.defaultFont[glyphName]
                    if not len(g.components):
                        glyphNames.append(glyphName)
                if len(glyphNames):
                    self.glyphGroups[smartSet.name] = glyphNames

        group = self._groups[0]['view']

        group.groupSelector.setItems(self.glyphGroups.keys())
        self.groupSelectorCallback(None)

        if self.verbose:
            print('done.\n')


if __name__ == '__main__':

    OpenWindow(GlyphMemeProoferController)
