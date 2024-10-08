import os
import ezui
from defcon import Font
from mojo.roboFont import OpenWindow, OpenFont
from fontTools.designspaceLib import DesignSpaceDocument


def getSourceName(src):
    return os.path.splitext(src.filename)[0]


class DesignSpaceSelector_EZUI(ezui.WindowController):

    title       = 'DesignSpaceSelector'
    width       = 123*5 
    height      = 640
    buttonWidth = 100
    rowHeight   = 17
    verbose     = True

    designspace = None
    sources     = []

    content = """
    = Tabs
    * Tab: designspace   @designspaceTab
    >= VerticalStack
    >> designspaces
    >> |-files--------|
    >> | designspaces |  @designspaces
    >> |--------------|
    >> sources
    >> |--------------|
    >> | sources      |  @sources
    >> |--------------|
    >> ( open )          @openButton
    """

    descriptionData = dict(
        designspaces=dict(
            alternatingRowColors=True,
            height=60,
            itemType="dict",
            acceptedDropFileTypes=[".designspace"],
            allowsDropBetweenRows=True,
            allowsInternalDropReordering=True,
            allowsMultipleSelection=False,
            allowsEmptySelection=False,
            columnDescriptions=[
                dict(
                    identifier="path",
                    title="path",
                    cellClassArguments=dict(
                        showFullPath=True
                    )
                ),
            ]
        ),
        sources=dict(
            alternatingRowColors=True,
            height='auto',
            allowsMultipleSelection=True,
            allowsEmptySelection=False,
            columnDescriptions=[
                dict(
                    identifier="name",
                    title="name",
                    editable=False,
                ),
            ],
        ),
        openButton=dict(
            width=buttonWidth,
        ),
    )

    # subclasses should add all NSTables to this list
    # used to change table row height when starting up
    _tables = ['designspaces', 'sources']

    def build(self):
        self.w = ezui.EZWindow(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            size=(self.width, self.height),
            minSize=(self.width, 360),
        )

    def started(self):
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        for itemName in self._tables:
            self.w.getItem(itemName).getNSTableView().setRowHeight_(self.rowHeight)
        self.w.open()

    # callbacks

    def designspacesCreateItemsForDroppedPathsCallback(self, sender, paths):
        items = []
        for path in paths:
            item = dict(path=path)
            items.append(item)
        return items

    def designspacesSelectionCallback(self, sender):

        designspacesTable = self.w.getItem("designspaces")
        designspacesSelection = designspacesTable.getSelectedItems()

        if not designspacesSelection:
            return

        selectedDesignspace = designspacesSelection[0]
        designspacePath = selectedDesignspace['path']

        self.designspace = DesignSpaceDocument()
        self.designspace.read(designspacePath)

        # load font objects directly into designspace
        for src in self.designspace.sources:
            src.font = Font(src.path)

        # source name is UFO file name without .ufo extension
        self.sources =  { getSourceName(src): src for src in self.designspace.sources }

        sourcesTable = self.w.getItem("sources")
        sourcesItems = []
        for i, src in enumerate(self.designspace.sources):
            sourcesItems.append(dict(name=getSourceName(src)))

        sourcesTable.set(sourcesItems)

    def sourcesDoubleClickCallback(self, sender):
        self.openButtonCallback(None)

    def openButtonCallback(self, sender):

        sourcesTable = self.w.getItem("sources")
        selectedSources = sourcesTable.getSelectedItems()

        if not selectedSources:
            return

        selectedSourceNames = [src['name'] for src in selectedSources]
        if self.verbose:
            print('opening selected sources...')

        for srcName in selectedSourceNames:
            if srcName in self.sources:
                src = self.sources[srcName]
                if self.verbose:
                    print(f'\topening {srcName}...')
                OpenFont(src.path)
        
        if self.verbose:
            print('done...\n')


if __name__ == '__main__':

    OpenWindow(DesignSpaceSelector_EZUI)
