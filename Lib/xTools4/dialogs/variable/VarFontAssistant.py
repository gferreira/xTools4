from importlib import reload
import xTools4.dialogs.variable.DesignSpaceSelector
reload(xTools4.dialogs.variable.DesignSpaceSelector)

import ezui
from mojo.roboFont import OpenWindow, OpenFont
from xTools4.dialogs.variable.DesignSpaceSelector import DesignSpaceSelector_EZUI, getSourceName
from xTools4.dialogs.variable.Measurements import *

KEY = 'com.xTools4.VarFontAssistant'


thresholdDefault = 0.1

def defaultScaleColorFormatter(attributes):
    scaleColorFormatter(attributes, thresholdDefault)



class VarFontAssistant_EZUI(DesignSpaceSelector_EZUI):

    title = 'VarFont Assistant'
    key   = KEY

    columnLeft         = 160
    columnFontInfo     = 180
    columnKerningPairs = 180
    columnFontName     = 240
    columnValue        = 40
    columnKerningValue = 40
    columnMeasurements = 55

    _fontInfoAttrs = {
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
    _fontInfoValues = {}

    _kerningValues   = {}
    _kerningPairsAll = []

    _measurementsData = {}

    content = DesignSpaceSelector_EZUI.content
    content += '''
    * Tab: font info    @fontInfoTab
    >= HorizontalStack

    >> |-----------|
    >> |           |    @fontInfoAttributes
    >> |-----------|

    >> |-----------|--------|---------|
    >> | file name | value  | permill |  @fontInfoValues
    >> |-----------|--------|---------|

    * Tab: kerning       @kerningTab
    >= HorizontalStack

    >> |-----|-----|
    >> | 1st | 2nd |    @kerningPairs
    >> |-----|-----|

    >> |-----------|--------|---------|
    >> | file name | value  | permill |  @kerningValues
    >> |-----------|--------|---------|

    * Tab: measurements  @measurementsTab
    >= HorizontalStack

    >> |-------------|
    >> | measurement |  @measurements
    >> |-------------|

    >> |----------|-------|---------|---------|
    >> | filename | units | permill | d-scale |  @measurementValues
    >> |----------|-------|---------|---------|

    >= HorizontalStack
    >> ( load… )         @loadMeasurementsButton
    >> d-threshold
    >> [__](±)           @thresholdDefault

    * Tab: validation    @validationTab
    >= HorizontalStack
    
    >>= VerticalStack    @checksStack
    >>> checks
    >>> [ ] width        @widthCheckBox
    >>> [ ] left         @leftCheckBox
    >>> [ ] right        @rightCheckBox
    >>> [X] points       @pointsCheckBox
    >>> [X] components   @componentsCheckBox
    >>> [X] anchors      @anchorsCheckBox
    >>> [X] unicodes     @unicodesCheckBox

    >>= VerticalStack
    >>> result
    >>> *EZOutputEditor  @checkResults

    > ( validate )       @validateButton
    '''

    buttonWidth = DesignSpaceSelector_EZUI.buttonWidth

    _tables  = DesignSpaceSelector_EZUI._tables.copy()
    _tables += [
        'fontInfoAttributes',
        'fontInfoValues',
        'kerningPairs',
        'kerningValues',
        # 'measurementFiles',
        'measurements',
        'measurementValues',
    ]

    descriptionData = DesignSpaceSelector_EZUI.descriptionData.copy()
    descriptionData.update(dict(
        # font info
        fontInfoAttributes=dict(
            items=_fontInfoAttrs.values(),
            width=columnFontInfo,
            alternatingRowColors=True,
            allowsEmptySelection=False,
            allowsMultipleSelection=False,
        ),
        fontInfoValues=dict(
            alternatingRowColors=True,
            width='auto',
            columnDescriptions=[
                dict(
                    identifier="fileName",
                    title="file name",
                    width=columnFontName,
                    minWidth=columnFontName*0.9,
                    maxWidth=columnFontName*2,
                    sortable=True,
                ),
                dict(
                    identifier="value",
                    title="value",
                    sortable=True,
                ),
            ]
        ),
        loadFontInfoButton=dict(
            width=buttonWidth,
        ),
        saveFontInfoButton=dict(
            width=buttonWidth,
        ),
        # kerning
        kerningPreviewStack=dict(
            distribution="fill",
        ),
        kerningPairs=dict(
            alternatingRowColors=True,
            width=columnKerningPairs*2,
            allowsEmptySelection=False,
            allowsMultipleSelection=False,
            columnDescriptions=[
                dict(
                    identifier="first",
                    title="1st",
                    width=columnKerningPairs*0.8,
                ),
                dict(
                    identifier="second",
                    title="2nd",
                    width=columnKerningPairs*0.9,
                ),
            ]
        ),
        # kerningPreview=dict(
        #     width='auto',
        #     height=200,
        # ),
        kerningValues=dict(
            alternatingRowColors=True,
            width='auto',
            columnDescriptions=[
                dict(
                    identifier="fileName",
                    title="file name",
                    width=columnFontName,
                    minWidth=columnFontName*0.9,
                    maxWidth=columnFontName*2,
                    sortable=True,
                ),
                dict(
                    identifier="value",
                    title="value",
                    width=columnKerningValue,
                    sortable=True,
                ),
            ]
        ),
        loadKerningButton=dict(
            width=buttonWidth,
        ),
        saveKerningButton=dict(
            width=buttonWidth,
        ),
        # measurements
        measurements=dict(
            alternatingRowColors=True,
            width=columnLeft,
            allowsEmptySelection=False,
            allowsMultipleSelection=False,
            columnDescriptions=[
                dict(
                    identifier="name",
                    title="name",
                    # width=columnValue*1.2,
                ),
                # dict(
                #     identifier="direction",
                #     title="dir",
                #     width=columnValue*0.5,
                # ),
                # dict(
                #     identifier="pt1",
                #     title="pt1",
                #     width=columnValue*0.6,
                # ),
                # dict(
                #     identifier="pt2",
                #     title="pt2",
                #     width=columnValue*0.6,
                # ),
            ],
        ),
        measurementValuesStack=dict(
            distribution="fill",
        ),
        measurementValues=dict(
            alternatingRowColors=True,
            allowsSorting=True,
            columnDescriptions=[
                dict(
                    identifier="fileName",
                    title="file name",
                    width=columnFontName,
                    minWidth=columnFontName*0.9,
                    maxWidth=columnFontName*2,
                ),
                dict(
                    identifier="units",
                    title="units",
                    width=columnMeasurements,
                    cellDescription=dict(
                        cellType='TextField',
                        valueType='integer',
                    ),
                ),
                dict(
                    identifier="permill",
                    title="permill",
                    width=columnMeasurements,
                    cellDescription=dict(
                        cellType='TextField',
                        valueType='integer',
                    ),

                ),
                dict(
                    identifier="scale_d",
                    title="d-scale",
                    width=columnMeasurements,
                    cellDescription=dict(
                        valueToCellConverter=scaleValueToCellConverter,
                        cellToValueConverter=scaleCellToValueConverter,
                        stringFormatter=defaultScaleColorFormatter,
                    ),
                ),
            ]
        ),
        loadMeasurementsButton=dict(
            width=buttonWidth,
        ),
        thresholdDefault=dict(
            width=buttonWidth,
            valueType="float",
            value=thresholdDefault,
            minValue=0.0,
            maxValue=10.0,
            valueIncrement=0.01,
        ),
        # validation
        widthCheckBox=dict(
            width=columnLeft,
        ),
        validateButton=dict(
            width=buttonWidth,
        ),
    ))

    def build(self):
        self.w = ezui.EZWindow(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            size=(self.width, self.height),
            minSize=(self.width, 360),
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        for itemName in self._tables:
            self.w.getItem(itemName).getNSTableView().setRowHeight_(self.rowHeight)
        self.w.open()

    def started(self):
        # VarGlyphAssistantSubscriberRoboFont.controller = self
        # registerRoboFontSubscriber(VarGlyphAssistantSubscriberRoboFont)
        # self.font = CurrentFont()
        # if self.font:
        #     glyphs = getGlyphs2(self.font, glyphNames=False)
        #     self.glyph = glyphs[0] if glyphs else None
        # else:
        #     self.glyph = None
        # self._updateGlobals()
        # self._updateLists()
        pass

    def destroy(self):
        # unregisterRoboFontSubscriber(VarGlyphAssistantSubscriberRoboFont)
        # VarGlyphAssistantSubscriberRoboFont.controller = None
        pass

    # ---------
    # callbacks
    # ---------

    def _updateLists(self):
        self._loadFontInfo()
        self._loadKerning()
        self._loadMeasurements()

    def _updateGlobals(self):
        pass

    # font info

    def _loadFontInfo(self):
        # # not sure why we need this ??
        # if not hasattr(self, 'w'):
        #     return


        # load font info values into dict
        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        self._fontInfoValues = {}
        for srcName in selectedSourceNames:
            if srcName in self.sources.keys():
                # get defcon Font from designspace
                font = self.sources[srcName].font
                self._fontInfoValues[srcName] = {}
                for attr, attrLabel in self._fontInfoAttrs.items():
                    value = getattr(font.info, attr)
                    self._fontInfoValues[srcName][attrLabel] = value

    def fontInfoAttributesSelectionCallback(self, sender):
        if not hasattr(self, 'w'): # why is this needed ??
            return

        fontInfoValues = self.w.getItem('fontInfoValues')
        selectedFontInfoAttr = self.w.getItem('fontInfoAttributes').getSelectedItems()[0]

        # display dict data in the UI
        listItems = []
        for srcName in self._fontInfoValues:
            listItem = { 'fileName' : srcName }
            listItem['value'] = self._fontInfoValues[srcName][selectedFontInfoAttr]
            listItems.append(listItem)

        fontInfoValues.set(listItems)

    # kerning

    def _loadKerning(self):

        kerningPairs = self.w.getItem('kerningPairs')

        # load kerning values into dict
        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        # collect pairs and kerning values in selected sources
        allPairs = []
        self._kerningValues = {}
        for srcName in selectedSourceNames:
            if srcName in self.sources.keys():
                # get defcon Font from designspace
                font = self.sources[srcName].font
                allPairs += font.kerning.keys()
                self._kerningValues[srcName] = {}
                for pair, value in font.kerning.items():
                    g1, g2 = pair
                    if g1 not in font and g1 not in font.groups:
                        continue
                    if g2 not in font and g2 not in font.groups:
                        continue
                    self._kerningValues[srcName][pair] = value
        self._kerningPairsAll = list(set(allPairs))
        self._kerningPairsAll.sort()

        # display kerning pairs in the UI
        listItems = []
        for g1, g2 in sorted(self._kerningPairsAll):
            listItems.append({ 'first': g1, 'second': g2 })

        kerningPairs.set(listItems)

    def kerningPairsSelectionCallback(self, sender):

        kerningValues = self.w.getItem('kerningValues')
        selectedKerningPairItem = self.w.getItem('kerningPairs').getSelectedItems()[0]
        selectedKerningPair = selectedKerningPairItem['first'], selectedKerningPairItem['second']

        # display dict data in the UI
        listItems = []
        for srcName in self._kerningValues:
            listItem = { 'fileName' : srcName }
            value = self._kerningValues[srcName].get(selectedKerningPair)
            listItem['value'] = value
            listItems.append(listItem)

        kerningValues.set(listItems)

    # measurements

    def measurementsSelectionCallback(self, sender):
        self._loadMeasurementValues()

    def thresholdDefaultCallback(self, sender):
        global thresholdDefault
        thresholdDefault = self.w.getItem('thresholdDefault').get()
        self._loadMeasurementValues()

    def _loadMeasurements(self):

        measurementsTable      = self.w.getItem('measurements')
        measurementValuesTable = self.w.getItem('measurementValues')

        if not self._measurementsData or not self._measurementsData.get('font'):
            measurementsTable.set([])
            measurementValuesTable.set([])
            return

        fontMeasurements = self._measurementsData['font']

        # make font measurements list
        measurementsItems = []
        for measurementName in fontMeasurements.keys():
            listItem = {
                'name'      : measurementName,
                # 'direction' : fontMeasurements[measurementName].get('direction'),
                # 'pt1'       : fontMeasurements[measurementName].get('point 1'),
                # 'pt2'       : fontMeasurements[measurementName].get('point 2'),
            }
            measurementsItems.append(listItem) 

        # store values for all font measurements 

        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        self._measurementsUnits        = {}
        self._measurementsPermill      = {}
        self._measurementsScaleDefault = {}

        for srcName in selectedSourceNames:
            if srcName not in self.sources:
                continue

            # get defcon Font from designspace
            font = self.sources[srcName].font

            self._measurementsUnits[srcName]        = []
            self._measurementsPermill[srcName]      = []
            self._measurementsScaleDefault[srcName] = []

            for measurementName in fontMeasurements.keys():
                direction  = fontMeasurements[measurementName].get('direction')
                glyphName1 = fontMeasurements[measurementName].get('glyph 1')
                glyphName2 = fontMeasurements[measurementName].get('glyph 2')
                index1     = fontMeasurements[measurementName].get('point 1')
                index2     = fontMeasurements[measurementName].get('point 2')

                # setup measurement
                M = Measurement(
                    measurementName,
                    direction,
                    glyphName1, index1,
                    glyphName2, index2
                )

                # measure glyph
                valueUnits = M.measure(font)
                if valueUnits is None:
                    valuePermill = None
                elif valueUnits == 0:
                    valuePermill = 0
                else:
                    valuePermill = round(valueUnits*1000 / font.info.unitsPerEm)

                # get default value
                scale_d = None
                if self.designspace.default is not None:
                    defaultName = getSourceName(self.designspace.default)
                    defaultFont = self.sources[defaultName].font
                    valueDefault = M.measure(defaultFont)
                    # calculate d-scale
                    if valueUnits and valueDefault:
                        scale_d = valueUnits / valueDefault

                self._measurementsUnits[srcName].append(valueUnits)
                self._measurementsPermill[srcName].append(valuePermill)
                self._measurementsScaleDefault[srcName].append(scale_d)

        measurementsTable.set(measurementsItems)

    def _loadMeasurementValues(self):

        measurementsTable      = self.w.getItem('measurements')
        measurementValuesTable = self.w.getItem('measurementValues')

        selectedMeasurements = measurementsTable.getSelectedIndexes()
        if not selectedMeasurements:
            return

        selectionIndex = selectedMeasurements[0]
        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        listItems = []
        for srcName in selectedSourceNames:
            if srcName not in self.sources:
                continue
            listItem = {
                'fileName' : srcName,
                'units'    : self._measurementsUnits[srcName][selectionIndex],
                'permill'  : self._measurementsPermill[srcName][selectionIndex],
                'scale_d'  : self._measurementsScaleDefault[srcName][selectionIndex],
            }
            listItems.append(listItem)

        measurementValuesTable.set(listItems)


if __name__ == '__main__':

    OpenWindow(VarFontAssistant_EZUI)
