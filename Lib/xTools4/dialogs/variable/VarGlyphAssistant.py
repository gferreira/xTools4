from importlib import reload
import xTools4.dialogs.variable.DesignSpaceSelector
reload(xTools4.dialogs.variable.DesignSpaceSelector)
import xTools4.dialogs.variable.Measurements
reload(xTools4.dialogs.variable.Measurements)

import os
import ezui
from defcon import Font
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont, CurrentFont, CurrentGlyph
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber # , registerSubscriberEvent, roboFontSubscriberEventRegistry
from xTools4.modules.linkPoints2 import readMeasurements, getPointAtIndex, getIndexForPoint, getAnchorPoint
from xTools4.dialogs.variable.DesignSpaceSelector import DesignSpaceSelector_EZUI, getSourceName
from xTools4.dialogs.variable.Measurements import *
from xTools4.dialogs.variable.GlyphValidator import checkResultsFactory, validationGroupFactory

DEBUG = False

# global variables

attributesWidth      = 0
attributesLeft       = 0
attributesRight      = 0
attributesContours   = 0
attributesSegments   = 0
attributesPoints     = 0
attributesComponents = 0
attributesAnchors    = 0

thresholdFont        = 0.1
thresholdDefault     = 0.1

# value converters

def intToCellConverter(value):
    if value is None:
        return ''
    else:
        return str(value)

def cellToIntConverter(value):
    if value == '':
        return None
    try:
        value = int(value)
        return value
    except ValueError:
        return None

def marginToCellConverter(value):
    if value is None:
        return ''
    else:
        places = 1
        s = "{value:." + str(places) + "f}"
        s = s.format(value=value, places=places)
        s = s.rstrip("0").rstrip(".")
        return s

def cellToMarginConverter(value):
    if value == '':
        return None
    try:
        v = float(value)
        if v == int(v):
            v = int(v)
        return v
    except ValueError:
        return None

# color formatters

def numberColorFormatter(attributes, otherValue):
    value = attributes['value']
    if value is None:
        attributes["fillColor"] = colorCheckNone
    elif value == otherValue:
        attributes["fillColor"] = colorCheckTrue
    else:
        attributes["fillColor"] = colorCheckFalse

def widthColorFormatter(attributes):
    numberColorFormatter(attributes, attributesWidth)

def leftColorFormatter(attributes):
    numberColorFormatter(attributes, attributesLeft)

def rightColorFormatter(attributes):
    numberColorFormatter(attributes, attributesRight)

def contoursColorFormatter(attributes):
    numberColorFormatter(attributes, attributesContours)

def segmentsColorFormatter(attributes):
    numberColorFormatter(attributes, attributesSegments)

def pointsColorFormatter(attributes):
    numberColorFormatter(attributes, attributesPoints)

def componentsColorFormatter(attributes):
    numberColorFormatter(attributes, attributesComponents)

def anchorsColorFormatter(attributes):
    numberColorFormatter(attributes, attributesAnchors)




class VarGlyphAssistantController(DesignSpaceSelector_EZUI):

    title = 'VarGlyph Assistant'
    key   = 'com.fontBureau.varGlyphAssistant'

    debug = DEBUG

    buttonWidth        = 75
    columnLeft         = 160
    columnFontName     = 240
    columnValue        = 40
    columnValueAttrs   = 40
    columnMeasurements = 55

    content = DesignSpaceSelector_EZUI.content
    content += '''
    * Tab: attributes                                @attributesTab
    > |-----------|---|---|---|---|---|---|---|---|
    > | file name | W | L | R | C | S | P | A | C |  @attributesValues
    > |-----------|---|---|---|---|---|---|---|---|

    # * Tab: points                      @pointsTab
    # > |-----------|---|---|---|-----|
    # > | file name | 0 | 1 | 2 | ... |  @pointsTable
    # > |-----------|---|---|---|-----|

    * Tab: measurements  @measurementsTab
    >= HorizontalStack

    >> |------------------|-----------|-----|-----|
    >> | measurement name | direction | pt1 | pt2 |  @measurements
    >> |------------------|-----------|-----|-----|

    >> |-----------|-------|---------|---------|---------|
    >> | file name | units | permill | f-scale | d-scale | @measurementValues
    >> |-----------|-------|---------|---------|---------|

    >= HorizontalStack
    >> ( load… )     @loadMeasurementsButton
    >> f-threshold
    >> [__](±)       @thresholdFont
    >> d-threshold
    >> [__](±)       @thresholdDefault
    '''

    buttonWidth = DesignSpaceSelector_EZUI.buttonWidth

    _tables  = DesignSpaceSelector_EZUI._tables.copy()
    _tables += [
        'attributesValues',
        # 'pointsTable',
        'measurements',
        'measurementValues'
    ]

    descriptionData = DesignSpaceSelector_EZUI.descriptionData.copy()
    descriptionData.update(dict(
        # attributes
        attributesGlyphs=dict(
            alternatingRowColors=True,
            allowsMultipleSelection=False,
            width=columnLeft,
        ),
        attributesValues=dict(
            alternatingRowColors=True,
            allowsSorting=True,
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
                    identifier="width",
                    title="W",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=intToCellConverter,
                        cellToValueConverter=cellToIntConverter,
                        stringFormatter=widthColorFormatter,
                    ),
                ),
                dict(
                    identifier="left",
                    title="L",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=marginToCellConverter,
                        cellToValueConverter=cellToMarginConverter,
                        stringFormatter=leftColorFormatter,
                    ),
                ),
                dict(
                    identifier="right",
                    title="R",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=marginToCellConverter,
                        cellToValueConverter=cellToMarginConverter,
                        stringFormatter=rightColorFormatter,
                    ),
                ),
                dict(
                    identifier="contours",
                    title="C",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=intToCellConverter,
                        cellToValueConverter=cellToIntConverter,
                        stringFormatter=contoursColorFormatter,
                    ),
                ),
                dict(
                    identifier="segments",
                    title="S",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=intToCellConverter,
                        cellToValueConverter=cellToIntConverter,
                        stringFormatter=segmentsColorFormatter,
                    ),
                ),
                dict(
                    identifier="points",
                    title="P",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=intToCellConverter,
                        cellToValueConverter=cellToIntConverter,
                        stringFormatter=pointsColorFormatter,
                    ),
                ),
                dict(
                    identifier="components",
                    title="C",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=intToCellConverter,
                        cellToValueConverter=cellToIntConverter,
                        stringFormatter=componentsColorFormatter,
                    ),
                ),
                dict(
                    identifier="anchors",
                    title="A",
                    width=columnValueAttrs,
                    sortable=True,
                    cellDescription=dict(
                        valueToCellConverter=intToCellConverter,
                        cellToValueConverter=cellToIntConverter,
                        stringFormatter=anchorsColorFormatter,
                    ),
                ),
            ]
        ),
        loadAttributesButton=dict(
            width=buttonWidth,
        ),
        # points
        # pointsGlyphs=dict(
        #     alternatingRowColors=True,
        #     width=columnLeft,
        # ),
        # pointsTable=dict(
        #     alternatingRowColors=True,
        #     showColumnTitles=True,
        #     columnDescriptions=[
        #         dict(
        #             identifier="fileName",
        #             title="file name",
        #             width=columnFontName,
        #             minWidth=columnFontName*0.9,
        #             maxWidth=columnFontName*2,
        #             sortable=True,
        #         ),
        #     ],
        # ),
        # loadPointsButton=dict(
        #     width=buttonWidth,
        # ),
        # measurements
        measurements=dict(
            alternatingRowColors=True,
            width=columnLeft*1.5,
            allowsEmptySelection=False,
            allowsMultipleSelection=False,
            columnDescriptions=[
                dict(
                    identifier="name",
                    title="name",
                    width=columnValue*1.2,
                ),
                dict(
                    identifier="direction",
                    title="dir",
                    width=columnValue*0.5,
                ),
                dict(
                    identifier="pt1",
                    title="pt1",
                    width=columnValue*0.6,
                ),
                dict(
                    identifier="pt2",
                    title="pt2",
                    width=columnValue*0.6,
                ),
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
                    identifier="scale_f",
                    title="f-scale",
                    width=columnMeasurements,
                    cellDescription=dict(
                        valueToCellConverter=scaleValueToCellConverter,
                        cellToValueConverter=scaleCellToValueConverter,
                        stringFormatter=fontScaleColorFormatter,
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
            ],
        ),
        loadMeasurementsButton=dict(
            width=buttonWidth,
        ),
        thresholdFont=dict(
            width=buttonWidth,
            valueType="float",
            value=thresholdFont,
            minValue=0.0,
            maxValue=10.0,
            valueIncrement=0.01,
        ),
        thresholdDefault=dict(
            width=buttonWidth,
            valueType="float",
            value=thresholdDefault,
            minValue=0.0,
            maxValue=10.0,
            valueIncrement=0.01,
        ),
    ))

    _glyphAttributes = {}

    # _glyphPoints = {} 
    # _pointCount  = 0

    _measurementsData    = {}
    _measurementsUnits   = {}
    _measurementsPermill = {}

    font  = None
    glyph = None

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
        VarGlyphAssistantSubscriberRoboFont.controller = self
        registerRoboFontSubscriber(VarGlyphAssistantSubscriberRoboFont)
        self.font  = CurrentFont()
        self.glyph = CurrentGlyph()
        self._updateGlobals()
        self._updateLists()

    def destroy(self):
        unregisterRoboFontSubscriber(VarGlyphAssistantSubscriberRoboFont)
        VarGlyphAssistantSubscriberRoboFont.controller = None

    # -------------
    # dynamic attrs
    # -------------

    @property
    def defaultGlyph(self):
        if self.defaultFont is None or self.glyph is None:
            return
        if self.glyph.name not in self.defaultFont:
            return
        return self.defaultFont[self.glyph.name]

    # ---------
    # callbacks
    # ---------

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

    def _updateLists(self):
        self._loadAttributes()
        # self._loadPoints()
        self._loadMeasurements()
        self._loadMeasurementValues()

    def _updateGlobals(self):
        g = self.defaultGlyph
        if g is None:
            return

        # store attributes of default glyph in global variables
        global attributesWidth
        global attributesLeft
        global attributesRight
        global attributesContours
        global attributesSegments
        global attributesPoints
        global attributesComponents
        global attributesAnchors

        attributesWidth      = g.width
        attributesLeft       = g.leftMargin
        attributesRight      = g.rightMargin
        attributesContours   = len(g)
        attributesSegments   = sum([len(c.segments) for c in g])
        attributesPoints     = sum([len(c) for c in g])
        attributesComponents = len(g.components)
        attributesAnchors    = len(g.anchors)

    # measurements

    def loadMeasurementsButtonCallback(self, sender):
        jsonPath = GetFile(message='Select JSON file with measurements:')
        if jsonPath is None:
            return

        if self.verbose:
            print(f'loading data from {os.path.split(jsonPath)[-1]}... ')

        self._measurementsData = readMeasurements(jsonPath)
        self._loadMeasurements()

    def measurementsSelectionCallback(self, sender):
        self._loadMeasurementValues()

    def _loadMeasurements(self):
        measurementsTable      = self.w.getItem('measurements')
        measurementValuesTable = self.w.getItem('measurementValues')

        if self.glyph is None or not self._measurementsData:
            measurementsTable.set([])
            measurementValuesTable.set([])
            return

        glyphName = self.glyph.name
        glyphMeasurements = self._measurementsData['glyphs'].get(glyphName)
        fontMeasurements  = self._measurementsData['font']

        if glyphMeasurements is None:
            measurementsTable.set([])
            measurementValuesTable.set([])
            return

        # make glyph measurements list
        measurementsItems = []
        for measurementID in glyphMeasurements.keys():
            pt1, pt2 = measurementID.split()
            listItem = {
                'name'      : glyphMeasurements[measurementID].get('name'),
                'direction' : glyphMeasurements[measurementID].get('direction'),
                'pt1'       : pt1,
                'pt2'       : pt2,
            }
            measurementsItems.append(listItem) 

        # store values for all glyph measurements 

        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        self._measurementsUnits        = {}
        self._measurementsPermill      = {}
        self._measurementsScaleFont    = {}
        self._measurementsScaleDefault = {}

        for srcName in selectedSourceNames:
            if srcName not in self.sources:
                continue

            # get defcon Font from designspace
            font = self.sources[srcName].font

            self._measurementsUnits[srcName]        = []
            self._measurementsPermill[srcName]      = []
            self._measurementsScaleFont[srcName]    = []
            self._measurementsScaleDefault[srcName] = []

            for key in glyphMeasurements.keys():
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
                measurementName = glyphMeasurements[key]['name']
                M = Measurement(measurementName,
                    glyphMeasurements[key]['direction'],
                    glyphName, index1, glyphName, index2)

                # measure glyph
                valueUnits = M.measure(font)
                if valueUnits is None:
                    valuePermill = None
                elif valueUnits == 0:
                    valuePermill = 0
                else:
                    valuePermill = round(valueUnits*1000 / font.info.unitsPerEm)

                # get font-level value
                scale_f = None
                if fontMeasurements is not None:
                    if measurementName in fontMeasurements:
                        measurement = fontMeasurements.get(measurementName)
                        M2 = Measurement(measurementName,
                            measurement['direction'],
                            measurement['glyph 1'], measurement['point 1'],
                            measurement['glyph 2'], measurement['point 2']
                        )
                        valueFont = M2.measure(font)
                        # calculate f-scale
                        if valueUnits and valueFont:
                            scale_f = valueUnits / valueFont

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
                self._measurementsScaleFont[srcName].append(scale_f)
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
                'scale_f'  : self._measurementsScaleFont[srcName][selectionIndex],
                'scale_d'  : self._measurementsScaleDefault[srcName][selectionIndex],
            }
            listItems.append(listItem)

        measurementValuesTable.set(listItems)

    # attributes

    def attributesValuesDoubleClickCallback(self, sender):
        self.openSourceCallback(sender)

    def _loadAttributes(self):
        attributesTable = self.w.getItem('attributesValues')

        if self.glyph is None:
            attributesTable.set([])
            return

        # load glyph attributes into dict

        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        glyphName = self.glyph.name
        glyphAttributeIDs = ['width', 'left', 'right', 'contours', 'segments', 'points', 'anchors', 'components']

        self._glyphAttributes = {}
        for srcName in selectedSourceNames:
            if srcName in self.sources.keys():
                # get defcon Font from designspace
                font = self.sources[srcName].font
                self._glyphAttributes[srcName] = {}
                glyph = font[glyphName]
                self._glyphAttributes[srcName][glyphName] = {}
                for attr in glyphAttributeIDs:
                    if attr == 'width':
                        value = glyph.width
                    elif attr == 'left':
                        value = glyph.leftMargin
                    elif attr == 'right':
                        value = glyph.rightMargin
                    elif attr == 'contours':
                        value = len(glyph)
                    elif attr == 'segments':
                        value = sum([len(c.segments) for c in glyph])
                    elif attr == 'points':
                        value = sum([len(c) for c in glyph])
                    elif attr == 'anchors':
                        value = len(glyph.anchors)
                    elif attr == 'components':
                        value = len(glyph.components)
                    self._glyphAttributes[srcName][glyphName][attr] = value
                # font.close()

        # display dict data in the UI
        listItems = []
        for srcName in self._glyphAttributes:
            listItem = { 'fileName' : srcName }
            if glyphName in self._glyphAttributes[srcName]:
                for attr in self._glyphAttributes[srcName][glyphName]:
                    listItem[attr] = self._glyphAttributes[srcName][glyphName][attr]
            else:
                for attr in self._glyphAttributesLabels:
                    listItem[attr] = ''
            listItems.append(listItem)

        attributesTable.set(listItems)

    # points

    def _loadPoints(self):
        pointsTable = self.w.getItem('pointsTable')

        if self.glyph is None:
            pointsTable.set([])
            return

        '''
        WAITING FOR ADDING/REMOVING COLUMNS TO ARRIVE IN EZUI

        # load glyph points into dict

        selectedSources = self.w.getItem('sources').getSelectedItems()
        selectedSourceNames = [src['name'] for src in selectedSources]

        glyphName = self.glyph.name

        self._glyphPoints = {}
        for srcName in selectedSourceNames:
            if srcName in self.sources:
                # get defcon Font from designspace
                font = self.sources[srcName].font

                self._glyphPoints[srcName] = {}
                # for glyphName in glyphNames:
                if glyphName not in font:
                    continue
                glyph = font[glyphName]
                points = [p.segmentType for c in glyph for p in c]
                self._glyphPoints[srcName][glyphName] = points
                font.close()

        # clear columns
        for i in range(self._pointCount):
            pointsTable.removeColumn(str(i))

        # add columns
        pointCount = 0
        for srcName in self._glyphPoints:
            pts = self._glyphPoints[srcName][glyphName]
            try:
                if len(pts) > pointCount:
                    pointCount = len(pts)
            except:
                pass

        for i in range(pointCount):
            pointsTable.appendColumn(
                dict(
                    identifier=str(i),
                    title=str(i),
                    width=self.columnValueAttrs,
                )
            )

        # make list items
        listItems = []
        for srcName in self._glyphPoints:
            listItem = { 'fileName' : srcName }
            if glyphName in self._glyphPoints[srcName]:
                points = self._glyphPoints[srcName][glyphName]
                for i, pt in enumerate(points):
                    listItem[str(i)] = pt[0].upper()
            listItems.append(listItem)

        # set list items
        self.w.getItem('attributesValues').set(listItems)

        '''


class VarGlyphAssistantSubscriberRoboFont(Subscriber):

    controller = None

    def fontDocumentDidBecomeCurrent(self, info):
        # print('fontDocumentDidBecomeCurrent')
        self.controller.font = info['font']
        self.controller._updateLists()

    def fontDocumentDidOpen(self, info):
        # print('fontDocumentDidOpen')
        self.controller.font = info['font']
        self.controller._updateLists()

    def roboFontDidSwitchCurrentGlyph(self, info):
        # print('roboFontDidSwitchCurrentGlyph')
        self.controller.glyph = info["glyph"]
        self.controller._updateGlobals()
        self.controller._updateLists()

    # def settingsDidChange(self, info):
    #     print('settingsDidChange')


# varGlyphAssistantEventName = f"{VarGlyphAssistantController.key}.changed"

# if varGlyphAssistantEventName not in roboFontSubscriberEventRegistry:
#     registerSubscriberEvent(
#         subscriberEventName=varGlyphAssistantEventName,
#         methodName="settingsDidChange",
#         lowLevelEventNames=[varGlyphAssistantEventName],
#         documentation="Send when the VarGlyphAssistant window changes its parameters.",
#         dispatcher="roboFont",
#         delay=0,
#         debug=True
#     )


if __name__ == '__main__':

    OpenWindow(VarGlyphAssistant_EZUI)

