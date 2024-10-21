from importlib import reload
import variableValues.measurements
reload(variableValues.measurements)
import variableValues.dialogs.DesignSpaceSelector
reload(variableValues.dialogs.DesignSpaceSelector)
import variableValues.kerningPreview
reload(variableValues.kerningPreview)
import variableValues.validation
reload(variableValues.validation)

import AppKit
import os, csv
from vanilla import Window, TextBox, List, Button, Tabs, LevelIndicatorListCell, Group, CheckBox, SplitView, TextEditor
from fontParts.world import OpenFont
try:
    import drawBot as DB
    from drawBot.ui.drawView import DrawView
except:
    print('DrawBot extension not installed.')
from mojo.UI import PutFile, CodeEditor
from mojo.roboFont import OpenWindow
from variableValues.dialogs.DesignSpaceSelector import DesignSpaceSelector
from variableValues.kerningPreview  import VariableKerningPreview
from variableValues.linkPoints import readMeasurements
from variableValues.measurements import Measurement
from variableValues.validation import validateFonts # checkCompatibility, checkEquality


class VarFontAssistant(DesignSpaceSelector):
    
    title = 'VarFont Assistant'
    key   = 'com.fontBureau.varFontAssistant'

    _tabsTitles = ['designspace', 'font info', 'kerning', 'measurements', 'validation']

    _measurementFiles = {}
    _measurements = {}
    _measurementsPermill = {}

    _fontAttrs = {
        'familyName'                         : 'family name',
        'styleName'                          : 'style name',
        'unitsPerEm'                         : 'unitsPerEm',
        'xHeight'                            : 'xHeight',
        'capHeight'                          : 'capHeight',
        'descender'                          : 'descender',
        'ascender'                           : 'ascender',
        'italicAngle'                        : 'italic angle',
        'openTypeOS2WeightClass'             : 'OS2 weight',
        'openTypeOS2WidthClass'              : 'OS2 width',
        'openTypeOS2WeightClass'             : 'OS2 weight',
        'openTypeOS2TypoAscender'            : 'OS2 typo ascender',
        'openTypeOS2TypoDescender'           : 'OS2 typo descender',
        'openTypeOS2TypoLineGap'             : 'OS2 line gap',
        'openTypeOS2WinAscent'               : 'OS2 win ascender',
        'openTypeOS2WinDescent'              : 'OS2 win descender',
        'openTypeOS2StrikeoutSize'           : 'OS2 strikeout size',
        'openTypeOS2StrikeoutPosition'       : 'OS2 strikeout position',
        'openTypeHheaAscender'               : 'hhea ascender',
        'openTypeHheaDescender'              : 'hhea descender',
        'openTypeHheaLineGap'                : 'hhea line gap',
        'styleMapFamilyName'                 : 'style map family',
        'styleMapStyleName'                  : 'style map style',
        'copyright'                          : 'copyright',
        'trademark'                          : 'trademark',
        'openTypeNameDesigner'               : 'designer',
        'openTypeNameDesignerURL'            : 'designer URL',
        'openTypeNameManufacturer'           : 'manufacturer',
        'openTypeNameManufacturerURL'        : 'manufacturer URL',
        'openTypeNameLicense'                : 'license',
        'openTypeNameLicenseURL'             : 'license URL',
        'openTypeNameVersion'                : 'version',
        'openTypeNameUniqueID'               : 'uniqueID',
        'openTypeNameDescription'            : 'description',
        'openTypeNamePreferredFamilyName'    : 'preferred family',
        'openTypeNamePreferredSubfamilyName' : 'preferred subfamily',
        'openTypeNameCompatibleFullName'     : 'compatible name',
        'openTypeNameWWSFamilyName'          : 'WWS family',
        'openTypeNameWWSSubfamilyName'       : 'WWS subfamily',
    }
    _fontValues = {}

    _kerningPairsAll  = []
    _kerning          = {}

    _checks      = {
        'width'         : False,
        'left'          : False,
        'right'         : False,
        'points'        : True,
        'components'    : True,
        'anchors'       : True,
        'unicodes'      : True,
    }

    settings = {
        'kerningSampleWidth'    : 900,
        'kerningSampleHeight'   : 100,
        'kerningSampleScale'    : 0.045,
        'kerningSampleFontSize' : 96,
    }

    def __init__(self):
        self.w = Window(
                (self.width, self.height), title=self.title,
                minSize=(self.width, 360))

        x = y = p = self.padding
        self.w.tabs = Tabs((x, y, -p, -p), self._tabsTitles)

        self.initializeDesignspacesTab()
        self.initializeFontValuesTab()
        self.initializeKerningTab()
        self.initializeMeasurementsTab()
        self.initializeValidationTab()

        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    # initialize UI

    def initializeMeasurementsTab(self):

        tab = self._tabs['measurements']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

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
        tab.measurementsLabel = TextBox(
                (x, y, col, self.lineHeight),
                'measurements')

        y += self.lineHeight + p/2
        tab.measurements = List(
                (x, y, col, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateMeasurementsCallback,
            )

        y = self.lineHeight*4 + p*2
        tab.fontMeasurementsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'values')

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName,
                'minWidth' : self._colFontName*0.9,
                'maxWidth' : self._colFontName*2,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'permill',
                'width'    : self._colValue,
            },
            # {
            #     "title"    : 'level',
            #     'width'    : self._colValue*1.5,
            #     'cell'     : LevelIndicatorListCell(style="continuous", maxValue=1600),
            # },
        ]
        y += self.lineHeight + p/2
        tab.fontMeasurements = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
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
                callback=self.loadMeasurementsCallback,
            )

        x = -(p + self.buttonWidth)
        tab.exportMeasurements = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'export',
                callback=self.exportMeasurementsCallback,
            )

    def initializeFontValuesTab(self):

        tab = self._tabs['font info']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

        tab.fontAttrsLabel = TextBox(
                (x, y, col, self.lineHeight),
                'attributes')

        y += self.lineHeight + p/2
        tab.fontAttrs = List(
                (x, y, col, -(self.lineHeight + p*2)),
                self._fontAttrs.values(),
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                selectionCallback=self.updateFontValuesCallback,
            )

        y = p/2
        tab.fontInfoLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'values')

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName,
                'minWidth' : self._colFontName*0.9,
                'maxWidth' : self._colFontName*2,
            },
            {
                "title"    : 'value',
                # 'width'    : self._colValue,
            },
            # {
            #     "title"    : 'level',
            #     'width'    : self._colValue*1.5,
            #     'cell'     : LevelIndicatorListCell(style="continuous", maxValue=1600),
            # },
        ]
        y += self.lineHeight + p/2
        tab.fontValues = List(
                (x2, y, -p, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                # editCallback=self.editFontInfoValueCallback,
                enableDelete=False)

        y = -(self.lineHeight + p)
        tab.updateValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadFontValuesCallback,
            )

        x = -(p + self.buttonWidth)
        tab.saveFontValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                callback=self.saveFontValuesCallback,
            )

    def initializeKerningTab(self):

        tab = self._tabs['kerning']

        x = p = self.padding
        y = p/2
        col = self._colLeft * 2
        tab.pairsLabel = TextBox(
                (x, y, -p, self.lineHeight),
                'pairs')

        tab.pairsCounter = TextBox(
                (x, y, col, self.lineHeight),
                '',
                alignment='right')

        y += self.lineHeight + p/2
        tab.pairs = List(
                (x, y, col, -(self.lineHeight + p*2)),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=[{"title": t} for t in ['1st', '2nd']],
                selectionCallback=self.updateKerningValuesCallback,
            )

        x2 = x + col + p
        y = p/2

        # preview group

        kerningPreview = Group((0, 0, -0, -0))
        _x = _y = 0
        kerningPreview.label = TextBox(
                (_x, _y, -p, self.lineHeight),
                'preview')

        _y = self.lineHeight + p/2
        kerningPreview.canvas = DrawView((_x, _y, -p, -(self.lineHeight + p*2)))

        _y = -(self.lineHeight + p)
        kerningPreview.showMetrics = CheckBox(
            (_x, _y, self.buttonWidth, self.lineHeight),
            "show metrics",
            callback=self.updateKerningPreviewCallback,
            value=False)

        _x += self.buttonWidth + p
        kerningPreview.showKerning = CheckBox(
            (_x, _y, self.buttonWidth, self.lineHeight),
            "show kerning",
            callback=self.updateKerningPreviewCallback,
            value=True)

        # values group

        kerningValues = Group((0, 0, -0, -0))
        _x = 0
        _y = p/2
        kerningValues.label = TextBox(
                (_x, _y, -p, self.lineHeight),
                'values')

        _y += self.lineHeight + p/2
        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", maxValue=200),
            },
        ]
        kerningValues.list = List(
                (_x, _y, -p, -p),
                [],
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                #editCallback=self.editKerningCallback,
                enableDelete=False)

        # make splitview

        tab._splitDescriptors = [
            dict(view=kerningPreview, identifier="kerningPreview"),
            dict(view=kerningValues,  identifier="kerningValues"),
        ]
        tab.splitview = SplitView(
                (x2, y, -0, -(self.lineHeight+p)),
                tab._splitDescriptors,
                dividerStyle='thin',
                isVertical=False)

        y = -(self.lineHeight + p)
        tab.loadKerningValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'load',
                callback=self.loadKerningPairsCallback,
            )

        x = -(p + self.buttonWidth)
        tab.saveValues = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'save',
                callback=self.saveKerningCallback,
            )

    def initializeValidationTab(self):
        tab = self._tabs['validation']

        x = p = self.padding
        y = p/2
        col = self._colLeft
        x2 = x + col + p

        tab.checksLabel = TextBox(
                (x, y, col, self.lineHeight),
                'checks')

        y += self.lineHeight + p/2
        for check, value in self._checks.items():
            checkbox = CheckBox(
                (x, y, -p, self.lineHeight),
                check, value=value)
            setattr(tab, check, checkbox)
            y += self.lineHeight

        y = p/2
        tab.checkResultsLabel = TextBox(
                (x2, y, -p, self.lineHeight),
                'result')

        y += self.lineHeight + p/2
        tab.checkResults = CodeEditor(
                (x2, y, -p, -(self.lineHeight + p*2)),
                text='',
                readOnly=True,
                showLineNumbers=False)

        y = -(self.lineHeight + p)
        tab.validate = Button(
                (x, y, self.buttonWidth, self.lineHeight),
                'validate',
                callback=self.validateSourcesCallback)

    # -------------
    # dynamic attrs
    # -------------

    # fontinfo

    @property
    def selectedFontAttr(self):
        tab = self._tabs['font info']
        selection = tab.fontAttrs.getSelection()
        fontAttrs = tab.fontAttrs.get()
        selectedFontAttrs = [fontinfo for i, fontinfo in enumerate(fontAttrs) if i in selection]
        if not len(selectedFontAttrs):
            return
        return selectedFontAttrs[0]

    # kerning

    @property
    def selectedKerningPair(self):
        tab = self._tabs['kerning']
        i = tab.pairs.getSelection()[0]
        return self._kerningPairsAll[i], i

    @property
    def selectedKerningValue(self):
        tab = self._tabs['kerning']
        group = tab._splitDescriptors[1]['view']
        selection = group.list.getSelection()
        if not len(selection):
            return
        i = selection[0]
        item = group.list.get()[i]
        return item

    @property
    def showMetrics(self):
        tab = self._tabs['kerning']
        group = tab._splitDescriptors[0]['view']
        return group.showMetrics.get()

    @property
    def showKerning(self):
        tab = self._tabs['kerning']
        group = tab._splitDescriptors[0]['view']
        return group.showKerning.get()

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
    def selectedMeasurement(self):
        tab = self._tabs['measurements']
        selection = tab.measurements.getSelection()
        measurements = tab.measurements.get()
        selectedMeasurements = [m for i, m in enumerate(measurements) if i in selection]
        if not len(selectedMeasurements):
            return
        return selectedMeasurements[0]

    # validation

    @property
    def selectedChecks(self):
        tab = self._tabs['validation']
        return [check for check in self._checks if getattr(tab, check).get()]

    # ---------
    # callbacks
    # ---------

    # font info

    def loadFontValuesCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['font info']

        if self.verbose:
            print('loading font info values for selected sources...')

        # empty list
        if not self.selectedDesignspace:
            tab.fontInfo.set([])
            return

        # collect fontinfo values into dict
        self._fontValues = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            info = f.info.asDict()
            self._fontValues[sourceFileName] = {}
            print(f'\tloading font info values for {sourceFileName}...')
            for attr, attrLabel in self._fontAttrs.items():
                self._fontValues[sourceFileName][attrLabel] = info.get(attr)
            f.close()

        if self.verbose:
            print('...done.\n')

        self.updateFontValuesCallback(None)

    def updateFontValuesCallback(self, sender):

        tab = self._tabs['font info']

        if not self.selectedSources or not self._fontValues:
            tab.fontValues.set([])
            return

        fontAttr = self.selectedFontAttr

        # if self.verbose:
        #     print('updating font info values...\n')

        # create list items
        # values = []
        fontInfoItems = []
        for fontName in self._fontValues.keys():
            value = self._fontValues[fontName][fontAttr]
            # if value is None:
            #     value = '—'
            listItem = {
                "file name" : fontName,
                "value"     : value,
            }
            # if value is not None:
            #     listItem["level"] = abs(value)
            #     values.append(value)
            
            fontInfoItems.append(listItem)

        # set glyph values in table
        fontInfoValuesPosSize = tab.fontValues.getPosSize()
        del tab.fontValues

        columnDescriptions = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName,
                'minWidth' : self._colFontName*0.9,
                'maxWidth' : self._colFontName*2,
            },
            {
                "title"    : 'value',
                # 'width'    : self._colValue,
            },
            # {
            #     "title"    : 'level',
            #     'width'    : self._colValue*1.5,
            #     'cell'     : LevelIndicatorListCell(style="continuous", minValue=min(values), maxValue=max(values)),
            # },
        ]
        tab.fontValues = List(
            fontInfoValuesPosSize,
            fontInfoItems,
            allowsMultipleSelection=False,
            allowsEmptySelection=False,
            columnDescriptions=columnDescriptions,
            allowsSorting=True,
            editCallback=self.editFontValueCallback,
            enableDelete=False)

    def visualizeFontValuesCallback(self, sender):
        print('visualize font infos')

    def editFontValueCallback(self, sender):
        '''
        Save the edited font value back to the dict, so we can load values for another attribute.

        '''
        tab = self._tabs['font info']
        selection = tab.fontValues.getSelection()
        if not len(selection):
            return

        i = selection[0]
        items = tab.fontValues.get()
        item = items[i]

        # save change to internal dict
        fontAttr = self.selectedFontAttr
        fontName = item['file name']
        newValue = item['value']
        oldValue = self._fontValues[fontName].get(fontAttr)
        if oldValue != newValue:
            if self.verbose:
                print(f'changed font value {fontAttr} in {fontName}: {oldValue} → {newValue}\n')
            self._fontValues[fontName][fontAttr] = int(newValue)

    def saveFontValuesCallback(self, sender):
        '''
        Save the edited font info back into their source fonts.

        '''
        tab = self._tabs['font info']
        fontAttrs = { v: k for k, v in self._fontAttrs.items() }

        if self.verbose:
            print('saving edited font info to sources...')

        for fontName in self._fontValues.keys():
            sourcePath = self._sources[fontName]
            f = OpenFont(sourcePath, showInterface=False)
            fontChanged = False

            # for attr in self._fontValues[fontName]:
            for attr, newValue in self._fontValues[fontName].items():
                fontAttr = fontAttrs[attr]
                if newValue is None:
                    continue
                if type(newValue) is str:
                    if not len(newValue.strip()):
                        continue
                newValue = float(newValue)
                if newValue.is_integer():
                    newValue = int(newValue)
                oldValue = getattr(f.info, fontAttr)
                if newValue != oldValue:
                    if self.verbose:
                        print(f'\twriting new value for {attr} in {fontName}: {oldValue} → {newValue}')
                    setattr(f.info, fontAttr, newValue)
                    if not fontChanged:
                        fontChanged = True
            if fontChanged:
                # if self.verbose:
                #     print(f'\tsaving {fontName}...')
                f.save()
            f.close()

        if self.verbose:
            print('...done.\n')

    # kerning

    def loadKerningPairsCallback(self, sender):
        '''
        Load kerning pairs and values from selected sources into the UI.

        '''
        if not self.selectedSources:
            return

        tab = self._tabs['kerning']
        
        # collect pairs and kerning values in selected sources
        allPairs = []
        self._kerning = {}
        for source in self.selectedSources:
            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]
            f = OpenFont(sourcePath, showInterface=False)
            allPairs += f.kerning.keys()
            self._kerning[sourceFileName] = {}
            for pair, value in f.kerning.items():
                g1, g2 = pair
                if g1 not in f and g1 not in f.groups:
                    continue
                if g2 not in f and g2 not in f.groups:
                    continue
                self._kerning[sourceFileName][pair] = value
        self._kerningPairsAll = list(set(allPairs))
        self._kerningPairsAll.sort()

        # update pairs column
        pairListItems = []
        for g1, g2 in sorted(self._kerningPairsAll):
            pairItem = {'1st': g1, '2nd': g2}
            pairListItems.append(pairItem)
        tab.pairs.set(pairListItems)

    def updateKerningValuesCallback(self, sender):
        '''
        Update table with sources and kerning values based on the currently selected kerning pair.

        '''
        tab = self._tabs['kerning']
        group = tab._splitDescriptors[1]['view']

        if not self.selectedSources:
            group.list.set([])
            return

        pair, pairIndex = self.selectedKerningPair

        # if self.verbose:
        #     print(f'updating kerning values for pair {pair} ({pairIndex})...\n')

        # create list items
        values = []
        for fontName in self._kerning.keys():
            value = self._kerning[fontName][pair] if pair in self._kerning[fontName] else 0
            values.append(value)
        valuesMax = max(values) - min(values)

        kerningListItems = []
        for i, fontName in enumerate(self._kerning.keys()):
            value = values[i]
            listItem = {
                "file name" : fontName,
                "value"     : value,
                "level"     : value-min(values),
            }
            kerningListItems.append(listItem)

        # set kerning values in table
        kerningValuesPosSize = group.list.getPosSize()
        del group.list

        columnDescriptions = [
            {
                'title'    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
                'maxWidth' : self._colFontName*3,
                'editable' : False,
            },
            {
                'title'    : 'value',
                'width'    : self._colValue,
            },
            {
                'title'    : 'level',
                'width'    : self._colValue*1.5,
                'cell'     : LevelIndicatorListCell(style="continuous", minValue=0, maxValue=valuesMax),
            },
        ]
        group.list = List(
                kerningValuesPosSize,
                kerningListItems,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                editCallback=self.editKerningCallback,
                enableDelete=False)

        # update kerning pair counter (current/total)
        tab.pairsCounter.set(f'{pairIndex+1} / {len(self._kerningPairsAll)}')

        self.updateKerningPreviewCallback(None)

    def updateKerningPreviewCallback(self, sender):
        tab = self._tabs['kerning']

        # groupValues  = tab._splitDescriptors[0]['view']

        sampleWidth  = self.settings['kerningSampleWidth']
        sampleHeight = self.settings['kerningSampleHeight']

        pair, pairIndex = self.selectedKerningPair

        DB.newDrawing()

        # draw kerning preview

        V = VariableKerningPreview(self.selectedDesignspacePath)
        V.selectedSources = [self._sources[fontName] for fontName in self._kerning.keys()] # proofs[proofLevel][proofGroup]
        V._kerning = self._kerning
        V._allPairs = [pair] # self._kerningPairsAll
        V.draw()

        # refresh PDF preview
        groupPreview = tab._splitDescriptors[0]['view']
        pdfData = DB.pdfImage()
        groupPreview.canvas.setPDFDocument(pdfData)

    def editKerningCallback(self, sender):
        '''
        Save the edited kerning pair back to the dict, so we can load values for another pair.

        '''
        tab = self._tabs['kerning']
        item = self.selectedKerningValue

        if not item:
            return

        # save change to internal dict
        pair, pairIndex = self.selectedKerningPair
        fontName = item['file name']
        newValue = item['value']
        oldValue = self._kerning[fontName].get(pair)
        if oldValue != newValue:
            if self.verbose:
                print(f'changed kerning pair {pair} in {fontName}: {oldValue} → {newValue}\n')
            self._kerning[fontName][pair] = int(newValue)

        # update level indicator
        ### this will crash RF3!!
        # kerningListItems = []
        # for fontName in self._kerning.keys():
        #     value = self._kerning[fontName][pair] if pair in self._kerning[fontName] else 0
        #     listItem = {
        #         "file name" : fontName,
        #         "value"     : value,
        #         "level"     : abs(value),
        #     }
        #     kerningListItems.append(listItem)
        # tab.kerningValues.set(kerningListItems)

        self.updateKerningPreviewCallback(None)

    def saveKerningCallback(self, sender):
        '''
        Save the edited kerning values back into their source fonts.

        '''
        tab = self._tabs['kerning']

        if self.verbose:
            print('saving edited kerning values to sources...')

        for fontName in self._kerning.keys():
            sourcePath = self._sources[fontName]
            f = OpenFont(sourcePath, showInterface=False)
            fontChanged = False
            for pair, newValue in self._kerning[fontName].items():
                if type(newValue) not in [int, float]:
                    if not len(newValue.strip()):
                        continue
                newValue = int(newValue)
                oldValue = f.kerning.get(pair)
                if newValue != oldValue:
                    if newValue == 0 and pair in f.kerning:
                        if self.verbose:
                            print(f"\tdeleting {pair} in '{fontName}'...")
                        del f.kerning[pair]
                    else:
                        if self.verbose:
                            print(f"\twriting new value for {pair} in '{fontName}': {oldValue} → {newValue}")
                        f.kerning[pair] = newValue
                    if not fontChanged:
                        fontChanged = True
            if fontChanged:
                # if self.verbose:
                #     print(f'\tsaving {fontName}...')
                f.save()
            f.close()

        if self.verbose:
            print('...done.\n')

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

    def loadMeasurementsCallback(self, sender):

        if not self.selectedSources:
            return

        tab = self._tabs['measurements']

        # empty list
        if not self.selectedDesignspace:
            tab.fontMeasurements.set([])
            return

        # no measurements file
        if not self.selectedMeasurementFile:
            print('please select a JSON file with measurement definitions.\n')
            return

        # collect measurements into dict
        measurementFilePath = self._measurementFiles[self.selectedMeasurementFile]
        measurements = readMeasurements(measurementFilePath)

        self._measurements = {}
        self._measurementsPermill = {}

        for source in self.selectedSources:

            sourceFileName = source['file name']
            sourcePath = self._sources[sourceFileName]

            f = OpenFont(sourcePath, showInterface=False)

            self._measurements[sourceFileName] = {}
            self._measurementsPermill[sourceFileName] = {}

            for key, attrs in measurements['font'].items():
                glyphName1 = attrs['glyph 1']
                glyphName2 = attrs['glyph 2']
                index1     = attrs['point 1']
                index2     = attrs['point 2']
                direction  = attrs['direction']

                try:
                    index1 = int(index1)
                except:
                    pass

                try:
                    index2 = int(index2)
                except:
                    pass

                M = Measurement(
                    key,
                    direction,
                    glyphName1, index1,
                    glyphName2, index2
                )
                distance = M.measure(f, roundToInt=True, absolute=False, verbose=False)

                if distance and f.info.unitsPerEm:
                    permill = round(float(distance) * 1000 / f.info.unitsPerEm)
                else:
                    permill = None

                self._measurements[sourceFileName][key] = distance
                self._measurementsPermill[sourceFileName][key] = permill

            f.close()

        self.updateMeasurementsCallback(None)

    def selectMeasurementFileCallback(self, sender):

        tab = self._tabs['measurements']

        if not self.selectedMeasurementFile:
            tab.measurements.set([])
            return

        measurementFilePath = self._measurementFiles[self.selectedMeasurementFile]
        measurements = readMeasurements(measurementFilePath)
        tab.measurements.set(measurements['font'].keys())

    def updateMeasurementsCallback(self, sender):

        tab = self._tabs['measurements']

        if not self.selectedSources or not self._measurements:
            tab.fontMeasurements.set([])
            return

        measurementName = self.selectedMeasurement

        # if self.verbose:
        #     print('updating font measurements...\n')

        # create list items
        values = []
        measurementItems = []
        for fontName in self._measurements.keys():
            value = self._measurements[fontName][measurementName]
            valuePermill = self._measurementsPermill[fontName][measurementName]
            if value is None:
                value = ''
            if valuePermill is None:
                valuePermill = ''
            listItem = {
                "file name" : fontName,
                "value"     : value,
                "permill"   : valuePermill,
            }
            measurementItems.append(listItem)
            values.append(value)

        # set measurement values in table
        fontMeasurementsPosSize = tab.fontMeasurements.getPosSize()
        del tab.fontMeasurements

        columnDescriptions  = [
            {
                "title"    : 'file name',
                'width'    : self._colFontName*1.5,
                'minWidth' : self._colFontName,
                'maxWidth' : self._colFontName*3,
            },
            {
                "title"    : 'value',
                'width'    : self._colValue,
            },
            {
                "title"    : 'permill',
                'width'    : self._colValue,
            },
        ]
        tab.fontMeasurements = List(
                fontMeasurementsPosSize,
                measurementItems,
                allowsMultipleSelection=False,
                allowsEmptySelection=False,
                columnDescriptions=columnDescriptions,
                allowsSorting=True,
                enableDelete=False)

    def exportMeasurementsCallback(self, sender):
        tab = self._tabs['measurements']

        # get CSV file path

        csvFileName = 'measurements.csv'
        csvPath = PutFile(message='Save measurements to CSV file:', fileName=csvFileName)

        if csvPath is None:
            if self.verbose:
                print('[cancelled]\n')
            return

        if os.path.exists(csvPath):
            os.remove(csvPath)

        if self.verbose:
            print(f'saving measurements to {csvPath}...', end=' ')

        items = tab.fontMeasurements.get()
        measurementNames = tab.measurements.get()

        with open(csvPath, 'w', newline='') as f:
            fieldnames  = ['font name']
            for measurementName in measurementNames:
                fieldnames.append(f'{measurementName} (units)')
                fieldnames.append(f'{measurementName} (permill)')

            csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
            # write header row
            csvWriter.writeheader()
            # write data rows
            for fontName in self._measurements.keys():
                row = { 'font name' : fontName }
                for measurementName in measurementNames:
                    row[f'{measurementName} (units)']   = self._measurements[fontName][measurementName]
                    row[f'{measurementName} (permill)'] = self._measurementsPermill[fontName][measurementName]
                csvWriter.writerow(row)

        if self.verbose:
            print('done.\n')

    # validation

    def validateSourcesCallback(self, sender):

        # print(self.selectedSources)

        if not self.selectedSources:
            return

        tab = self._tabs['validation']

        # --------------
        # batch validate
        # --------------

        options = { check: check in self.selectedChecks for check in self._checks.keys() }

        txt = 'validating selected sources...\n\n'
        for check in self.selectedChecks:
            txt += f'\t- {check}\n'
        txt += '\n'

        # get default font
        defaultPath = self.selectedDesignspacePlus.default.path
        defaultFont = OpenFont(defaultPath, showInterface=False)
        txt += f'\tdefault font: {defaultFont.info.familyName} {defaultFont.info.styleName}\n\n'

        # get target sources
        targetPaths = [self._sources[f['file name']] for f in self.selectedSources]
        if defaultPath in targetPaths:
            targetPaths.remove(defaultPath)
        targetFonts = [OpenFont(f, showInterface=False) for f in targetPaths]

        txt += validateFonts(targetFonts, defaultFont, options)
        txt += '...done!\n\n'

        tab.checkResults.set(txt)


# ----
# test
# ----

if __name__ == '__main__':

    OpenWindow(VarFontAssistant)
