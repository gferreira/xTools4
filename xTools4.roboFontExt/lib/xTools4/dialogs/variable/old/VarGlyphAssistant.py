import AppKit
import os, sys
import plistlib
from operator import itemgetter 
from vanilla import  Window, EditText, TextBox, Box, List, Button, Tabs
from mojo.roboFont import OpenWindow, OpenFont
from mojo.smartSet import readSmartSets
from xTools4.dialogs.variable.old.DesignSpaceSelector import DesignSpaceSelector
from xTools4.modules.linkPoints2 import readMeasurements
from xTools4.modules.measurements import Measurement


def getSegmentTypes(glyph):
    segments = []
    for ci, c in enumerate(glyph.contours):
        for si, s in enumerate(c.segments):
            if s.type == 'curve':
                segmentType = 'C'
            elif s.type == 'qcurve':
                segmentType = 'Q'
            else:
                segmentType = 'L'
            segments.append(segmentType)
    return segments


class VarGlyphAssistant(DesignSpaceSelector):
    
    title = 'VarGlyph Assistant'
    key   = 'com.fontBureau.varGlyphAssistant'

    _tabsTitles = ['designspace', 'glyphs', 'attributes', 'segments', 'measurements']

    _glyphAttrs = {}
    _glyphAttrsLabels = [
        'width',
        'left',
        'right',
        'contours',
        'segments',
        'points',
        'anchors',
        'components',
    ]
    _glyphCompatibility = {}

    _glyphSetsFiles = {}
    _glyphSets = {}

    _measurementFiles    = {}
    _measurements        = {}
    _measurementsUnits   = {}
    _measurementsPermill = {}

    def __init__(self):
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        self.initializeDesignspacesTab()
        self.initializeGlyphsTab()
        self.initializeAttributesTab()
        self.initializeCompatibilityTab()
        self.initializeMeasurementsTab()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    # initialize UI

    def initializeGlyphsTab(self):

        tab = self._tabs['glyphs']

        x = p = self.padding
        y = p/2
        x2 = x + self._colLeft + p

        tab.glyphSetsFilesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyph set files')

        y += self.lineHeight + p/2
        tab.glyphSetsFiles = List(
                (x, y, -p, self.lineHeight*3),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                selectionCallback=self.selectGlyphSetsFileCallback,
                otherApplicationDropSettings=dict(
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropGlyphSetsFilesCallback),
                )

        y += self.lineHeight*3 + p
        tab.glyphSetsLabel = TextBox(
                (x, y, self._colLeft, self.lineHeight),
                'glyphs sets')

        tab.glyphNamesLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'glyph names')

        y += self.lineHeight + p/2
        tab.glyphSets = List(
                (x, y, self._colLeft, -self.lineHeight - p*2),
                [],
                allowsMultipleSelection=True,
                allowsEmptySelection=False,
                selectionCallback=self.selectGlyphSetCallback)

        tab.glyphNames = EditText(
                (x2, y, -p, -self.lineHeight - p*2),
                'a b c A B C one two three')

        y = -(self.lineHeight + p)
        tab.updateGlyphs = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load')

    def initializeAttributesTab(self):

        tab = self._tabs['attributes']

        x = p = self.padding
        y = p/2
        tab.glyphsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, self._colLeft, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.selectGlyphAttrsCallback)

        y = p/2
        x2 = x + self._colLeft + p
        tab.glyphAttributesLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'glyph attributes')

        y += self.lineHeight + p/2
        tab.glyphAttributes = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=True,
                columnDescriptions=[{"title": t, "key": t, 'width': self._colFontName, 'minWidth': self._colFontName*0.9, 'maxWidth': self._colFontName*2} if ti == 0 else {"title": t, "key": t, 'width': self._colValue*1.6} for ti, t in enumerate(['file name'] + self._glyphAttrsLabels)],
            )

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.updateAttributesCallback)

    def initializeCompatibilityTab(self):

        tab = self._tabs['segments']

        x = p = self.padding
        y = p/2
        tab.glyphsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, self._colLeft, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.selectGlyphCompatibilityCallback)

        y = p/2
        x2 = x + self._colLeft + p
        tab.segmentsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'glyph segments')

        y += self.lineHeight + p/2
        tab.segments = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [])

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.updateCompatibilityCallback)

    def initializeMeasurementsTab(self):

        tab = self._tabs['measurements']

        x = p = self.padding
        y = p/2
        col1 = self._colLeft
        col2 = 220
        x2 = x  + col1 + p
        x3 = x2 + col2 + p

        tab.measurementFilesLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'measurement files')

        y += self.lineHeight + p/2
        tab.measurementFiles = List(
                (x, y, -p, self.lineHeight*3),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                enableDelete=True,
                # editCallback=self.selectDesignspaceCallback,
                selectionCallback=self.selectMeasurementFileCallback,
                otherApplicationDropSettings=dict(
                    type=AppKit.NSFilenamesPboardType,
                    operation=AppKit.NSDragOperationCopy,
                    callback=self.dropMeasurementFileCallback),
                )

        y += self.lineHeight*3 + p
        tab.glyphsLabel = TextBox(
                (x, y, col1, self.lineHeight),
                'glyphs')

        y += self.lineHeight + p/2
        tab.glyphs = List(
                (x, y, col1, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateGlyphMeasurementsCallback)

        y = self.lineHeight*4 + p*2
        tab.glyphMeasurementsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'measurements')

        y += self.lineHeight + p/2
        columnDescriptions = [
            { "title": "name", 'width': 60 },
            { "title": "dir",  'width': 30 },
            { "title": "pt1",  'width': 30 },
            { "title": "pt2",  'width': 30 },
        ]
        tab.glyphMeasurements = List(
                (x2, y, col2, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                # editCallback=self.editFontInfoValueCallback,
                enableDelete=False,
                selectionCallback=self.updateGlyphMeasurementValuesCallback)

        y = self.lineHeight*4 + p*2
        tab.glyphMeasurementValuesLabel = TextBox(
                (x3, y, -p, self.lineHeight),
                'values')

        y += self.lineHeight + p/2
        columnDescriptions = [
            { "title": "file name", 'width': self._colFontName },
            { "title": "units",     'width': 60 },
            { "title": "permill",   'width': 60 },
        ]
        tab.glyphMeasurementValues = List(
                (x3, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                # editCallback=self.editFontInfoValueCallback,
                enableDelete=False)

        y = -(self.lineHeight + p)
        tab.updateMeasurements = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.updateMeasurementGlyphsCallback)

        # x = -(p + self.buttonWidth)
        # tab.exportMeasurements = Button(
        #         (x, y, self.buttonWidth, self.lineHeight),
        #         'export',
        #         # callback=self.exportMeasurementsCallback,
        #     )

    # -------------
    # dynamic attrs
    # -------------

    @property
    def selectedGlyphSetsFile(self):
        tab = self._tabs['glyphs']
        selection = tab.glyphSetsFiles.getSelection()
        glyphSetsFiles = tab.glyphSetsFiles.get()
        selectedGlyphSetsFiles = [gs for i, gs in enumerate(glyphSetsFiles) if i in selection]
        if not len(selectedGlyphSetsFiles):
            return
        return selectedGlyphSetsFiles[0]

    @property
    def selectedGlyphSetsFilePath(self):
        if not self.selectedGlyphSetsFile:
            return
        return self._glyphSetsFiles[self.selectedGlyphSetsFile]

    @property
    def selectedGlyphSets(self):
        tab = self._tabs['glyphs']
        selection = tab.glyphSets.getSelection()
        glyphSets = tab.glyphSets.get()
        selectedGlyphSets = [gs for i, gs in enumerate(glyphSets) if i in selection]
        if not len(selectedGlyphSets):
            return
        return selectedGlyphSets

    @property
    def selectedGlyphAttributes(self):
        tab = self._tabs['attributes']
        selection = tab.glyphs.getSelection()
        glyphs = tab.glyphs.get()
        selectedGlyphs = [a for i, a in enumerate(glyphs) if i in selection]
        if not len(selectedGlyphs):
            return
        return selectedGlyphs[0]

    @property
    def selectedGlyphCompatibility(self):
        tab = self._tabs['segments']
        selection = tab.glyphs.getSelection()
        glyphs = tab.glyphs.get()
        selectedGlyphs = [a for i, a in enumerate(glyphs) if i in selection]
        if not len(selectedGlyphs):
            return
        return selectedGlyphs[0]

    # measurements

    @property
    def selectedMeasurementFile(self):
        tab = self._tabs['measurements']
        selection = tab.measurementFiles.getSelection()
        measurementFiles = tab.measurementFiles.get()
        selectedMeasurementFiles = [measurementFile for i, measurementFile in enumerate(measurementFiles) if i in selection]
        if not len(selectedMeasurementFiles):
            return
        return selectedMeasurementFiles[0]

    @property
    def selectedMeasurementsGlyph(self):
        tab = self._tabs['measurements']
        selection = tab.glyphs.getSelection()
        glyphs = tab.glyphs.get()
        selectedGlyphs = [a for i, a in enumerate(glyphs) if i in selection]
        if not len(selectedGlyphs):
            return
        return selectedGlyphs[0]

    @property
    def selectedGlyphMeasurement(self):
        tab = self._tabs['measurements']
        selection = tab.glyphMeasurements.getSelection()
        if not len(selection):
            return
        return selection[0]

    # ---------
    # callbacks
    # ---------

    # glyph sets

    def dropGlyphSetsFilesCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1] == '.roboFontSets']

        if not paths:
            return False

        if not isProposal:
            tab = self._tabs['glyphs']
            for path in paths:
                label = os.path.split(path)[-1]
                self._glyphSetsFiles[label] = path
                tab.glyphSetsFiles.append(label)
                tab.glyphSetsFiles.setSelection([0])

        return True

    def selectGlyphSetsFileCallback(self, sender):

        tab = self._tabs['glyphs']

        if not self.selectedGlyphSetsFile:
            tab.glyphSets.set([])
            tab.glyphNames.set('')
            return

        assert os.path.exists(self.selectedGlyphSetsFilePath)

        # load smart sets data into dict
        smartSets = readSmartSets(self.selectedGlyphSetsFilePath, useAsDefault=False, font=None)

        self._glyphSets = {}

        for smartSet in smartSets:
            for group in smartSet.groups:
                self._glyphSets[group.name] = group.glyphNames

        tab.glyphSets.set(self._glyphSets.keys())

    def selectGlyphSetCallback(self, sender):
        tab = self._tabs['glyphs']

        if not self.selectedGlyphSets:
            tab.glyphNames.set([])
            return

        glyphNames = []
        for glyphSet in self.selectedGlyphSets:
            glyphNames += self._glyphSets[glyphSet]

        tab.glyphNames.set(' '.join(glyphNames))

    # attributes

    def updateAttributesCallback(self, sender):
        
        if not self.selectedSources:
            return

        tab = self._tabs['attributes']
        glyphNames = self._tabs['glyphs'].glyphNames.get().split(' ')

        # collect glyph values into dict
        self._glyphAttrs = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)

            self._glyphAttrs[sourceFileName] = {}
            for glyphName in glyphNames:
                if glyphName in f:
                    g = f[glyphName]
                    self._glyphAttrs[sourceFileName][glyphName] = {}
                    for attr in self._glyphAttrsLabels:
                        if attr == 'width':
                            value = g.width
                        elif attr == 'left':
                            value = g.leftMargin
                        elif attr == 'right':
                            value = g.rightMargin
                        elif attr == 'contours':
                            value = len(g.contours)
                        elif attr == 'segments':
                            value = 0
                            for c in g.contours:
                                value += len(c)
                        elif attr == 'points':
                            value = 0
                            for c in g.contours:
                                value += len(c.points)
                        elif attr == 'anchors':
                            value = len(g.anchors)
                        elif attr == 'components':
                            value = len(g.components)
                        self._glyphAttrs[sourceFileName][glyphName][attr] = value

            f.close()

        tab.glyphs.set(glyphNames)
        tab.glyphs.setSelection([0])
        self.selectGlyphAttrsCallback(None)

    def selectGlyphAttrsCallback(self, sender):
        tab = self._tabs['attributes']
        glyphName = self.selectedGlyphAttributes

        listItems = []
        for sourceFileName in self._glyphAttrs:
            listItem = { 'file name' : sourceFileName }
            if glyphName in self._glyphAttrs[sourceFileName]:
                for attr in self._glyphAttrs[sourceFileName][glyphName]:
                    listItem[attr] = self._glyphAttrs[sourceFileName][glyphName][attr]
            else:
                for attr in self._glyphAttrsLabels:
                    listItem[attr] = ''

            listItems.append(listItem)

        tab.glyphAttributes.set(listItems)

    # compatibility

    def updateCompatibilityCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['segments']
        glyphNames = self._tabs['glyphs'].glyphNames.get().split(' ')

        # collect glyph compatibility data into dict
        self._glyphCompatibility = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)

            self._glyphCompatibility[sourceFileName] = {}
            for glyphName in glyphNames:
                if glyphName in f:
                    g = f[glyphName]
                    segments = getSegmentTypes(g)
                else:
                    segments = None
                self._glyphCompatibility[sourceFileName][glyphName] = segments

            # f.close()

        tab.glyphs.set(glyphNames)
        tab.glyphs.setSelection([0])
        self.selectGlyphCompatibilityCallback(None)

    def selectGlyphCompatibilityCallback(self, sender):

        tab = self._tabs['segments']
        glyphName = self.selectedGlyphCompatibility

        segmentsPosSize = tab.segments.getPosSize()
        del tab.segments

        sMax = 0
        for sourceFileName in self._glyphCompatibility:
            segmentsGlyph = self._glyphCompatibility[sourceFileName][glyphName]
            try:
                if len(segmentsGlyph) > sMax:
                    sMax = len(segmentsGlyph)
            except:
                pass

        listItems = []
        segmentsGlyphs = []
        for sourceFileName in self._glyphCompatibility:
            listItem = { 'file name' : sourceFileName }
            segmentsGlyph = self._glyphCompatibility[sourceFileName][glyphName]
            if segmentsGlyph:
                for si, segment in enumerate(segmentsGlyph):
                    listItem[str(si)] = segment
            else:
                for i in range(sMax):
                    listItem[str(i)] = ''
            listItems.append(listItem)
            segmentsGlyphs.append(segmentsGlyph)

        # for S in segmentsGlyphs:
        #     print(S)

        segmentsDescriptions  = [{'title': 'file name', 'minWidth': self._colFontName, 'width': self._colFontName*1.5}]
        segmentsDescriptions += [{'title': str(i), 'width': 20} for i in range(sMax)]

        # create list UI with sources
        tab.segments = List(
                segmentsPosSize, listItems,
                columnDescriptions=segmentsDescriptions,
                allowsMultipleSelection=True,
                enableDelete=False,
                allowsEmptySelection=False,
            )

    # measurements

    def dropMeasurementFileCallback(self, sender, dropInfo):
        isProposal = dropInfo["isProposal"]
        existingPaths = sender.get()

        paths = dropInfo["data"]
        paths = [path for path in paths if path not in existingPaths]
        paths = [path for path in paths if os.path.splitext(path)[-1].lower() == '.json']

        if not paths:
            return False

        if not isProposal:
            tab = self._tabs['measurements']
            for path in paths:
                label = os.path.split(path)[-1]
                self._measurementFiles[label] = path
                tab.measurementFiles.append(label)
                tab.measurementFiles.setSelection([0])

        return True

    def selectMeasurementFileCallback(self, sender):

        tab = self._tabs['measurements']

        if not self.selectedMeasurementFile:
            tab.glyphMeasurements.set([])
            return

        measurementFilePath = self._measurementFiles[self.selectedMeasurementFile]
        self._measurements = readMeasurements(measurementFilePath)

    def updateMeasurementGlyphsCallback(self, sender):
        tab = self._tabs['measurements']
        glyphNames = self._tabs['glyphs'].glyphNames.get().split(' ')
        tab.glyphs.set(glyphNames)

    def updateGlyphMeasurementsCallback(self, sender):

        tab = self._tabs['measurements']

        # no measurements file
        if not self._measurements:
            tab.glyphMeasurements.set([])
            return

        # no glyph measurements dict
        if not self._measurements.get('glyphs'):
            tab.glyphMeasurements.set([])
            return

        glyphName = self.selectedMeasurementsGlyph
        glyphMeasurementsKeys = self._measurements['glyphs'].get(glyphName)
        
        # make glyph measurements list
        listItems = []
        for k in glyphMeasurementsKeys:
            pt1, pt2 = k.split()
            listItem = {
                'name' : self._measurements['glyphs'][glyphName][k]['name'],
                'dir'  : self._measurements['glyphs'][glyphName][k]['direction'],
                'pt1'  : pt1,
                'pt2'  : pt2,
            }
            listItems.append(listItem) 

        # measure sources and store data

        self._measurementsUnits   = {}
        self._measurementsPermill = {}

        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]

            f = OpenFont(sourcePath, showInterface=False)

            self._measurementsUnits[sourceFileName]   = []
            self._measurementsPermill[sourceFileName] = []

            for key in glyphMeasurementsKeys:
                parts = key.split()

                # get point indexes
                if len(parts) == 2:
                    index1, index2 = parts
                else:
                    continue
                try:
                    index1 = int(index1)
                except:
                    pass
                try:
                    index2 = int(index2)
                except:
                    pass

                # setup measurement
                measurementName = self._measurements['glyphs'][glyphName][key]['name']
                M = Measurement(measurementName,
                    self._measurements['glyphs'][glyphName][key]['direction'],
                    glyphName, index1, glyphName, index2)

                # measure glyph
                valueUnits = M.measure(f)
                if valueUnits is None:
                    valueUnits = valuePermill = '-'
                elif valueUnits == 0:
                    valuePermill = 0
                else:
                    valuePermill = round(valueUnits*1000 / f.info.unitsPerEm)

                self._measurementsUnits[sourceFileName].append((measurementName, index1, index2, valueUnits, valuePermill))

            f.close()

        # update UI
        tab.glyphMeasurements.set(listItems)
        tab.glyphMeasurements.setSelection([0])

    def updateGlyphMeasurementValuesCallback(self, sender):

        tab = self._tabs['measurements']

        listItems = []
        for sourceName, measurements in self._measurementsUnits.items():
            measurement = measurements[self.selectedGlyphMeasurement]
            if measurement is None:
                continue
            measurementName, index1, index2, valueUnits, valuePermill = measurement
            listItem = {
                "file name" : sourceName,
                "units"     : valueUnits,
                "permill"   : valuePermill,
            }
            listItems.append(listItem)

        sortedItems = sorted(listItems, key=itemgetter('units', 'file name'))
        tab.glyphMeasurementValues.set(sortedItems)


if __name__ == '__main__':

    OpenWindow(VarGlyphAssistant)

