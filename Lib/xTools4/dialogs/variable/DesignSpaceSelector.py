import os
import ezui
from defcon import Font
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont
from fontTools.designspaceLib import DesignSpaceDocument
from xTools4.modules.linkPoints2 import readMeasurements # getPointAtIndex, getIndexForPoint, getAnchorPoint
from xTools4.modules.xproject import measurementsPathKey

KEY = 'com.xTools4.dialogs.variable.designSpaceSelector'

def getSourceName(src):
    return os.path.splitext(src.filename)[0]


class DesignSpaceSelector_EZUI(ezui.WindowController):

    title       = 'DesignSpaceSelector'
    width       = 123*5 
    height      = 640
    buttonWidth = 100
    rowHeight   = 17
    verbose     = True

    key = KEY

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
    >>= HorizontalStack
    >>> ( open )         @openButton
    >>> ( reload ↺ )     @reloadButton
    """

    _measurementsData = {}

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
        reloadButton=dict(
            width=buttonWidth,
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
        self.w.workspaceWindowIdentifier = self.KEY
        self.w.open()

    # dynamic attrs

    @property
    def defaultFont(self):
        if self.designspace is None:
            return
        defaultName = getSourceName(self.designspace.default)
        if defaultName in self.sources:
            return self.sources[defaultName].font

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

        sourcesFolder = os.path.dirname(designspacePath)

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

        # load measurements
        measurementsFile = self.designspace.lib.get(measurementsPathKey)
        if measurementsFile:
            measurementsPath = os.path.join(sourcesFolder, measurementsFile)
            self._measurementsData = readMeasurements(measurementsPath)
            self._loadMeasurements()

    # def sourcesDoubleClickCallback(self, sender):
    #     self.openButtonCallback(None)

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

    def reloadButtonCallback(self, sender):
        print('reloading sources...', end=' ')
        for src in self.designspace.sources:
            src.font = Font(src.path)
        print('done.\n')

    def sourcesSelectionCallback(self, sender):
        self._updateLists()

    def openSourceCallback(self, sender):

        selectedItems = sender.getSelectedItems()
        selectedSourceNames = [src['fileName'] for src in selectedItems]

        for srcName in selectedSourceNames:
            if srcName in self.sources:
                src = self.sources[srcName]
                if self.verbose:
                    print(f'\topening {srcName}...')
                OpenFont(src.path)
        
        if self.verbose:
            print('done...\n')

    # def loadMeasurementsButtonCallback(self, sender):
    #     jsonPath = GetFile(message='Select JSON file with measurements:')
    #     if jsonPath is None:
    #         return

    #     if self.verbose:
    #         print(f'loading data from {os.path.split(jsonPath)[-1]}... ')

    #     self._measurementsData = readMeasurements(jsonPath)
    #     self._loadMeasurements()

    def _updateLists(self):
        # implement method when subclassing object
        # loads font data in other tabs
        pass

    def _loadMeasurements(self):
        # implement method when subclassing object
        # loads measurements in another tab
        pass


if __name__ == '__main__':

    OpenWindow(DesignSpaceSelector_EZUI)
