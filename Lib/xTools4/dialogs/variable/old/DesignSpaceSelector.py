import AppKit
import os
from operator import itemgetter
from vanilla import Window, TextBox, CheckBox, List, Tabs, Button
from mojo.roboFont import OpenFont, OpenWindow
from xTools4.modules.designspacePlus import DesignSpacePlus, getVarDistance


class DesignSpaceSelector:

    title         = 'DesignSpaceSelector'
    width         = 123*5
    height        = 640
    padding       = 10
    lineHeight    = 22
    buttonWidth   = 100
    verbose       = True

    _colLeft      = 160
    _colFontName  = 240
    _colValue     = 50

    _tabsTitles   = ['designspace'] # expand in subclass

    #: A dictionary of designspace names (keys) and their .designspace paths (values).
    _designspaces = {}

    _axisColumns  = ['name', 'tag', 'default', 'minimum', 'maximum']

    #: A dictionary of source font names (keys) and their UFO paths (values).
    _sources      = {}

    #: Source groups by distance from location to default (+ label width for UI)
    _sourceTypes  = [
        ('default',   65),
        ('duovars',   70),
        ('trivars',   62),
        ('quadvars',  77),
        ('othervars', 70),
    ]

    def __init__(self):
        # overwrite in subclass
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width, 360))
        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)
        self.initializeDesignspacesTab()
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    # initialize UI

    def initializeDesignspacesTab(self):

        tab = self._tabs['designspace']

        x = p = self.padding
        y = p/2
        tab.designspacesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'designspaces')

        y += self.lineHeight + p/2
        tab.designspaces = List(
                (x, y, -p, self.lineHeight*3),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                # editCallback=self.selectDesignspaceCallback,
                selectionCallback=self.selectDesignspaceCallback,
                otherApplicationDropSettings=dict(
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropDesignspaceCallback),
                )

        y += self.lineHeight*3 + p

        # tab.axesLabel = TextBox(
        #         (x, y, -p, self.lineHeight),
        #         'axes')

        # y += self.lineHeight + p/2
        # axesDescriptions = []
        # for i, columnTitle in enumerate(self._axisColumns):
        #     D = {}
        #     D["title"] = columnTitle
        #     if i:
        #         D["width"] = 80
        #     else:
        #         D["minWidth"] = 80
        #         D["width"]    = 120
        #         D["maxWidth"] = 200
        #     axesDescriptions.append(D)
        # tab.axes = List(
        #         (x, y, -p, self.lineHeight*7),
        #         [],
        #         drawFocusRing=False,
        #         # editCallback=self.editAxesCallback,
        #         allowsSorting=True,
        #         # selfDropSettings=dict(type="genericListPboardType",
        #         #         operation=AppKit.NSDragOperationMove,
        #         #         callback=self.genericDropSelfCallback),
        #         # dragSettings=dict(type="genericListPboardType",
        #         #         callback=self.genericDragCallback),
        #         columnDescriptions=axesDescriptions,
        #     )

        # y += self.lineHeight*7 + p
        tab.sourcesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'sources')

        y += self.lineHeight + p/2
        tab.sources = List(
                (x, y, -p, -(self.lineHeight + p*2)),
                [])

        y = -(self.lineHeight + p)
        for sourceType, labelWidth in self._sourceTypes:
            checkBox = CheckBox(
                (x, y, self.buttonWidth-p, self.lineHeight),
                sourceType,
                value=True,
                callback=self.updateSourcesListCallback,
                sizeStyle='small')
            setattr(tab, sourceType, checkBox)
            x += labelWidth

        x = -(p + self.buttonWidth)
        tab.openSelectedSources = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'open',
                callback=self.openSelectedSourcesCallback,
            )

    # -------------
    # dynamic attrs
    # -------------

    @property
    def _tabs(self):
        tabsDict = {}
        for tabTitle in self._tabsTitles:
            tabIndex = self._tabsTitles.index(tabTitle)
            tabsDict[tabTitle] = self.w.tabs[tabIndex]
        return tabsDict

    @property
    def selectedDesignspace(self):
        '''Returns the name of the currently selected designspace.'''
        tab = self._tabs['designspace']
        selection = tab.designspaces.getSelection()
        designspaces = tab.designspaces.get()
        selectedDesignspaces = [designspace for i, designspace in enumerate(designspaces) if i in selection]
        if not len(selectedDesignspaces):
            return
        return selectedDesignspaces[0]

    @property
    def selectedDesignspacePath(self):
        '''Returns the .designspace path of the currently selected designspace.'''
        if not self.selectedDesignspace:
            return
        return self._designspaces[self.selectedDesignspace]

    @property
    def selectedDesignspacePlus(self):
        '''Returns a DesignSpacePlus object for the currently selected designspace.'''
        if not self.selectedDesignspacePath:
            return
        return DesignSpacePlus(self.selectedDesignspacePath)

    @property
    def sourceFilters(self):
        '''Returns a dictionary with source filter names (keys) and their checkbox statuses (value).'''
        tab = self._tabs['designspace']
        filters = {}
        for sourceType, w in self._sourceTypes:
            checkBox = getattr(tab, sourceType)
            filters[sourceType] = checkBox.get()
        return filters

    @property
    def sources(self):
        '''Returns a list of filtered SourceDescriptor objects.'''
        tab = self._tabs['designspace']
        filters = self.sourceFilters
        designspacePlus = self.selectedDesignspacePlus
        # all filters == no filters
        if all(filters.values()):
            return designspacePlus.document.sources
        # filter sources
        filteredSources = []
        if self.sourceFilters['default']:
            filteredSources += [designspacePlus.default]
        if self.sourceFilters['duovars']:
            filteredSources += designspacePlus.duovars
        if self.sourceFilters['trivars']:
            filteredSources += designspacePlus.trivars
        if self.sourceFilters['quadvars']:
            filteredSources += designspacePlus.quadvars
        if self.sourceFilters['othervars']:
            filteredSources += designspacePlus.othervars
        return filteredSources

    @property
    def selectedSources(self):
        '''Returns currently selected source list items.'''
        tab = self._tabs['designspace']
        selection = tab.sources.getSelection()
        sources = tab.sources.get()
        selectedSources = [source for i, source in enumerate(sources) if i in selection]
        if not len(selectedSources):
            return
        return selectedSources

    # -------
    # methods
    # -------

    def collectAllSources(self):
        '''Collect all designspace sources into a dict of file names (keys) and UFO source paths (values).'''
        self._sources = {}
        for source in self.selectedDesignspacePlus.document.sources:
            sourceFileName = os.path.splitext(os.path.split(source.path)[-1])[0]
            self._sources[sourceFileName] = source.path

    # ---------
    # callbacks
    # ---------

    def dropDesignspaceCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.designspace']

        if not paths:
            return False

        if not isProposal:
            tab = self._tabs['designspace']
            for path in paths:
                label = os.path.split(path)[-1]
                self._designspaces[label] = path
                tab.designspaces.append(label)
                tab.designspaces.setSelection([0])

        return True

    def selectDesignspaceCallback(self, sender):

        tab = self._tabs['designspace']

        if not self.selectedDesignspace:
            # tab.axes.set([])
            tab.sources.set([])
            return

        # update axes list
        # axesItems = []
        # for axis in self.selectedDesignspacePlus.document.axes:
        #     axisItem = { attr : getattr(axis, attr) for attr in self._axisColumns }
        #     axesItems.append(axisItem)
        # tab.axes.set(axesItems)

        self.collectAllSources()
        self.updateSourcesListCallback(None)

    '''
    def editAxesCallback(self, sender):
        tab = self._tabs['designspace']
        self.axesOrder = [a['tag'] for a in tab.axes.get()]

        if not hasattr(tab, 'sources'):
            return

        _sourceItems = tab.sources.get()
        sourceItems = []
        for item in _sourceItems:
            D = {}
            for k, v in item.items():
                D[k] = v
            sourceItems.append(D)

        if len(self.axesOrder):
            sourceItems = sorted(sourceItems, key=itemgetter(*self.axesOrder))

        tab.sources.set(sourceItems)

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
    '''

    def updateSourcesListCallback(self, sender):

        # make list items
        sourcesDescriptions  = [{'title': 'n', 'width': 20}]
        sourcesDescriptions += [{'title': 'file name', 'width': self._colFontName, 'minWidth': self._colFontName*0.9}] # , 'maxWidth': self._colFontName*3
        sourcesDescriptions += [{'title': axis.tag, 'width': self._colValue} for axis in self.selectedDesignspacePlus.document.axes]
        sourcesItems = []
        for source in self.sources:
            sourceFileName = os.path.splitext(os.path.split(source.path)[-1])[0]
            n = getVarDistance(source, self.selectedDesignspacePlus.default)
            sourceItem = {
                'n'         : n,
                'file name' : sourceFileName,
            }
            for axis in self.selectedDesignspacePlus.document.axes:
                sourceItem[axis.tag] = source.location[axis.name]
            sourcesItems.append(sourceItem)

        # update source list
        tab = self._tabs['designspace']
        sourcesListPosSize = tab.sources.getPosSize()
        del tab.sources
        tab.sources = List(
            sourcesListPosSize, sourcesItems,
            columnDescriptions=sourcesDescriptions,
            allowsMultipleSelection=True,
            allowsSorting=True,
            enableDelete=False,
            # selectionCallback=self.selectedSourcesCallback,
            # doubleClickCallback=self.openSourceCallback
        )

    # def selectedSourcesCallback(self, sender):
    #     # print(self.selectedSources) # list items
    #     pass

    def openSelectedSourcesCallback(self, sender):

        print(self.selectedSources)

        if not self.selectedSources:
            return

        for srcItem in self.selectedSources:
            sourcePath = self._sources[srcItem['file name']]
            if not os.path.exists(sourcePath):
                if self.verbose:
                    print(f"this source does not exist: '{sourcePath}'")
                continue
            if self.verbose:
                print(f"opening '{sourcePath}'...", end=' ')
            f = OpenFont(sourcePath, showInterface=True)

    # def openSourceCallback(self, sender):
    #     selectedSource = self.selectedSources[0]
    #     sourcePath = self._sources[selectedSource['file name']]
    #     if not os.path.exists(sourcePath):
    #         if self.verbose:
    #             print(f"this source does not exist: '{sourcePath}'")
    #         return
    #     if self.verbose:
    #         print(f"opening '{sourcePath}'...", end=' ')
    #     f = OpenFont(sourcePath, showInterface=True)
    #     if self.verbose:
    #         print('done!\n')

# ----
# test
# ----

if __name__ == '__main__':

    OpenWindow(DesignSpaceSelector)

