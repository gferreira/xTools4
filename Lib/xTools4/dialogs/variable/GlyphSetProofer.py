import os, time
import AppKit
import drawBot as DB
from drawBot.ui.drawView import DrawView
from vanilla import *
from mojo.UI import PutFile
from mojo.roboFont import OpenWindow
from fontParts.world import OpenFont
from xTools4.modules.designspacePlus import DesignSpacePlus
from xTools4.modules.glyphSetProofer import GlyphSetProofer


KEY = 'com.xTools4.dialogs.variable.glyphSetProofer'


class GlyphSetProoferUI:

    title      = 'GlyphSetProofer'
    width      = 800
    height     = 600
    padding    = 10
    lineHeight = 22
    verbose    = True

    checks = {
        'width'      : True,
        'left'       : True,
        'right'      : True,
        'points'     : True,
        'components' : True,
        'anchors'    : True,
        'unicodes'   : True,
    }

    _designspaces = {}
    _sources      = {}

    def __init__(self):
        self.w = Window(
                (self.width, self.height),
                title=self.title,
                minSize=(self.width*0.7, self.height*0.7))

        group1 = Group((0, 0, -0, -0))

        x = y = p = self.padding
        group1.designspacesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'designspaces')

        y += self.lineHeight
        group1.designspaces = List(
                (x, y, -p, self.lineHeight*3),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                selectionCallback=self.selectDesignspaceCallback,
                otherApplicationDropSettings=dict(
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropDesignspaceCallback),
            )

        y += self.lineHeight*3 + p
        group1.sourcesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources')

        y += self.lineHeight
        group1.sources = List(
                (x, y, -p, -self.lineHeight*2 - p*3),
                [],
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                enableDelete=False)

        y = -self.lineHeight*2 - p*2
        group1.makeProof = Button(
                (x, y, -p, self.lineHeight),
                'make proof',
                callback=self.makeProofsCallback)

        y = -self.lineHeight*1 - p*1
        group1.savePDF = Button(
                (x, y, -p, self.lineHeight),
                'save PDF…',
                callback=self.savePDFCallback)

        group2 = Group((0, 0, -0, -0))
        x = p = self.padding
        y = 0
        group2.canvas = DrawView((x, y, -p, -p))

        self._groups = [
            dict(view=group1, identifier="pane1", size=123*2, minSize=123*1.5, maxSize=123*3, canCollapse=False),
            dict(view=group2, identifier="pane2", canCollapse=False),
        ]
        self.w.splitView = SplitView((0, 0, -0, -0), self._groups, dividerStyle='thin')

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.workspaceWindowIdentifier = KEY
        self.w.open()

    # dynamic attributes

    @property
    def selectedDesignspace(self):
        group = self._groups[0]['view']
        selection = group.designspaces.getSelection()
        designspaces = group.designspaces.get()
        selectedDesignspaces = [designspace for i, designspace in enumerate(designspaces) if i in selection]
        if not len(selectedDesignspaces):
            return
        return selectedDesignspaces[0]

    @property
    def selectedDesignspacePath(self):
        if not self.selectedDesignspace:
            return
        return self._designspaces[self.selectedDesignspace]

    @property
    def selectedDesignspacePlus(self):
        if not self.selectedDesignspacePath:
            return
        return DesignSpacePlus(self.selectedDesignspacePath)

    @property
    def sources(self):
        group = self._groups[0]['view']
        designspacePlus = self.selectedDesignspacePlus
        return designspacePlus.document.sources

    @property
    def selectedSources(self):
        group = self._groups[0]['view']
        selection = group.sources.getSelection()
        sources = group.sources.get()
        selectedSources = [source for i, source in enumerate(sources) if i in selection]
        if not len(selectedSources):
            return
        return selectedSources

    # callbacks

    def dropDesignspaceCallback(self, sender, dropInfo):

        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.designspace']

        if not paths:
            return False

        if not isProposal:
            group = self._groups[0]['view']
            for path in paths:
                label = os.path.split(path)[-1]
                self._designspaces[label] = path
                group.designspaces.append(label)
                group.designspaces.setSelection([0])

        return True

    def selectDesignspaceCallback(self, sender):

        group = self._groups[0]['view']

        if not self.selectedDesignspace:
            group.sources.set([])
            return

        self._sources = {}
        for source in self.selectedDesignspacePlus.document.sources:
            if source.path == self.selectedDesignspacePlus.default.path:
                continue
            sourceFileName = os.path.splitext(os.path.split(source.path)[-1])[0]
            self._sources[sourceFileName] = source.path

        group.sources.set(self._sources.keys())

    def makeProofsCallback(self, sender):

        default = self.selectedDesignspacePlus.default
        if default is None:
            return

        group = self._groups[1]['view']

        sourcePaths = [self._sources[p] for p in self.selectedSources]

        print('building PDF proof... ', end='')
        # DB.newDrawing()
        start = time.time()
        P = GlyphSetProofer(default.familyName, default.path, sourcePaths)
        P.build(savePDF=False)
        end = time.time()
        print(f'done in {end - start:.2f} seconds.\n')

        pdfData = DB.pdfImage()
        group.canvas.setPDFDocument(pdfData)

    def savePDFCallback(self, sender):

        default = self.selectedDesignspacePlus.default
        if default is None:
            return

        pdfPath = PutFile(
                message="Choose a location for this PDF",
                fileName=f"glyphset_{default.familyName.replace(' ', '-')}.pdf"
            )
        DB.saveImage(pdfPath)


if __name__ == '__main__':

    OpenWindow(GlyphSetProoferUI)
