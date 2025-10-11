from importlib import reload
import xTools4.modules.rounding
reload(xTools4.modules.rounding)

import os, json
from random import random
import ezui
from defcon import Glyph, registerRepresentationFactory, unregisterRepresentationFactory
from merz import MerzView, MerzPen
from mojo import drawingTools as ctx
from mojo.UI import PutFile, GetFile, CurrentFontWindow
from mojo.roboFont import OpenFont, CurrentFont, CurrentGlyph, RGlyph
from xTools4.modules.linkPoints2 import getIndexForPoint
from xTools4.modules.rounding import applyRounding
from xTools4.modules.interpolation import getStem
from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
from mojo.events import postEvent, addObserver, removeObserver


KEY = 'com.xTools4.roundingTool'


def roundedGlyphFactory(glyph):

    roundCaps = glyph.lib[KEY].get('caps')
    roundCorners = glyph.lib[KEY].get('corners')
    radius = glyph.lib[KEY].get('radius')

    roundedGlyph = RGlyph()
    roundedGlyph.appendGlyph(RGlyph(glyph))
    applyRounding(roundedGlyph, roundCaps, roundCorners, mode=1, radius=radius)
    return roundedGlyph


class RoundingController(ezui.WindowController):

    title       = 'RoundingEdit'
    key         = KEY
    buttonWidth = 75

    verbose     = True
    messageMode = 1

    jsonPath = None

    roundingDict = {}

    font  = None
    glyph = None

    content = """
    = HorizontalStack

    * Group @roundCaps
    > Caps
    > |-----------------|
    > | point1 | point2 | @roundCapsTable
    > |--------|--------|
    > |        |        |
    > |-----------------|
    >> (+-) @roundCapsAddRemoveButton

    * Group @roundCorners
    > Corners
    > |-------|
    > | point | @roundCornersTable
    > |-------|
    > |       |
    > |-------|
    >> (+-) @roundCornersAddRemoveButton

    =============

    [X] preview @preview
    * ColorWell @colorButton

    ( load… ) @loadButton
    ( save  ) @saveButton

    """

    descriptionData = dict(
        roundCaps=dict(
            width=160,
        ),
        roundCorners=dict(
            width=160,
        ),
        roundCapsTable=dict(
            columnDescriptions=[
                dict(
                    identifier="point1",
                    title="point 1",
                    width=55,
                    editable=True,
                ),
                dict(
                    identifier="point2",
                    title="point 2",
                    width=55,
                    editable=True,
                ),
            ],
        ),
        roundCornersTable=dict(
            columnDescriptions=[
                dict(
                    identifier="point",
                    title="point",
                    width=55,
                    editable=True,
                ),
                dict(
                    identifier="scale",
                    title="scale",
                    width=55,
                    editable=True,
                    continuous=False,
                ),
            ],
        ),
        colorButton=dict(
            color=(1, 0, 0.5, 0.5),
            width=buttonWidth,
        ),
        loadButton=dict(
            width=buttonWidth,
        ),
        saveButton=dict(
            width=buttonWidth,
        ),
        preview=dict(
            width=buttonWidth,
        ),
    )

    def build(self):
        self.w = ezui.EZPanel(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            size=('auto', 300),
        )
        self.w.workspaceWindowIdentifier = self.title
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem("roundCapsTable").getNSTableView().setRowHeight_(17)
        self.w.getItem("roundCornersTable").getNSTableView().setRowHeight_(17)
        self.w.open()

    def started(self):
        RoundingSubscriberRoboFont.controller = self
        registerRoboFontSubscriber(RoundingSubscriberRoboFont)
        RoundingSubscriberGlyphEditor.controller = self
        registerGlyphEditorSubscriber(RoundingSubscriberGlyphEditor)
        addObserver(self, "drawLabelCell", "glyphCellDrawBackground")
        registerRepresentationFactory(Glyph, KEY, roundedGlyphFactory)
        self.font  = CurrentFont()
        self.glyph = CurrentGlyph()

    def destroy(self):
        unregisterRoboFontSubscriber(RoundingSubscriberRoboFont)
        RoundingSubscriberRoboFont.controller = None
        unregisterGlyphEditorSubscriber(RoundingSubscriberGlyphEditor)
        RoundingSubscriberGlyphEditor.controller = None
        removeObserver(self, "glyphCellDrawBackground")
        unregisterRepresentationFactory(Glyph, KEY)

    # ---------
    # callbacks
    # ---------

    def loadButtonCallback(self, sender):
        self.jsonPath = GetFile(message='Select JSON file with rounding data:')
        if self.jsonPath is None:
            return

        if self.verbose:
            print(f'loading data from {os.path.split(self.jsonPath)[-1]}... ', end='')

        with open(self.jsonPath, 'r', encoding='utf-8') as f:
            self.roundingDict = json.load(f)

        self._updateRoundingTables()

        if self.verbose:
            print('done.\n')

        postEvent(f"{self.key}.changed")

    def saveButtonCallback(self, sender):

        # get JSON file path
        jsonPath = self.jsonPath
        if not jsonPath:
            jsonFileName = 'rounding.json'
            jsonPath = PutFile(message='Save rounding data to JSON file:', fileName=jsonFileName)
            if jsonPath is None:
                if self.verbose:
                    print('[cancelled]\n')
                return

        self.jsonPath = jsonPath

        if os.path.exists(self.jsonPath):
            os.remove(self.jsonPath)

        if self.verbose:
            print(f'saving rounding data to {self.jsonPath}...', end=' ')

        with open(self.jsonPath, 'w', encoding='utf-8') as f:
            json.dump(self.roundingDict, f, indent=2)

        if self.verbose:
            print('done.\n')

    def roundCapsAddRemoveButtonAddCallback(self, sender):

        if not self.glyph:
            return

        if len(self.glyph.selectedPoints) != 2:
            return

        roundingDict = self.roundingDict.get(self.glyph.name) or {}
        roundCaps = roundingDict.get('caps') or []

        pt1 = self.glyph.selectedPoints[0]
        pt2 = self.glyph.selectedPoints[1]

        index1 = getIndexForPoint(self.glyph, pt1)
        index2 = getIndexForPoint(self.glyph, pt2)

        if (index1, index2) not in roundCaps:
            roundCaps.append([index1, index2])

        if self.glyph.name not in self.roundingDict:
            self.roundingDict[self.glyph.name] = {}

        self.roundingDict[self.glyph.name]['caps'] = sorted(roundCaps)

        self._updateRoundingTables()

        postEvent(f"{self.key}.changed")

        self.glyph.changed()

    def roundCapsAddRemoveButtonRemoveCallback(self, sender):
        table = self.w.getItem("roundCapsTable")
        selectedIndexes = table.getSelectedIndexes()

        roundCaps = self.roundingDict[self.glyph.name].get('caps')
        for i in sorted(selectedIndexes, reverse=True):
            del roundCaps[i]

        self._updateRoundingTables()

        postEvent(f"{self.key}.changed")

        self.glyph.changed()

    def roundCornersAddRemoveButtonAddCallback(self, sender):

        if not self.glyph:
            return

        if len(self.glyph.selectedPoints) != 1:
            return

        roundingDict = self.roundingDict.get(self.glyph.name) or {}
        roundCorners = roundingDict.get('corners') or []

        pt = self.glyph.selectedPoints[0]

        index = getIndexForPoint(self.glyph, pt)

        if index not in roundCorners:
            roundCorners.append(index)

        if self.glyph.name not in self.roundingDict:
            self.roundingDict[self.glyph.name] = {}

        self.roundingDict[self.glyph.name]['corners'] = sorted(roundCorners)

        self._updateRoundingTables()

        postEvent(f"{self.key}.changed")

        self.glyph.changed()

    def roundCornersAddRemoveButtonRemoveCallback(self, sender):
        table = self.w.getItem("roundCornersTable")
        selectedIndexes = table.getSelectedIndexes()

        roundCorners = self.roundingDict[self.glyph.name].get('corners')
        for i in sorted(selectedIndexes, reverse=True):
            del roundCorners[i]

        self._updateRoundingTables()

        postEvent(f"{self.key}.changed")

        self.glyph.changed()

    def previewCallback(self, sender):
        pass

    def colorButtonCallback(self, sender):
        postEvent(f"{self.key}.changed")

    def drawLabelCell(self, notification):

        glyph = notification['glyph']

        rounding = self.roundingDict.get(glyph.name)
        if not rounding:
            return

        w = CurrentFontWindow()
        cellSize = w.fontOverview.views.sizeSlider.get()
        x, y = 3, cellSize * 0.35

        color = self.w.getItem("colorButton").get()
        color = color[:-1] + (1,)

        ctx.save()
        ctx.font('LucidaGrande-Bold')
        ctx.fontSize(10)
        ctx.fill(*color)
        ctx.text('R', (x, y))
        ctx.restore()

    # -------
    # methods
    # -------

    def _updateRoundingTables(self):

        if not self.glyph:
            return

        roundCapsTable    = self.w.getItem("roundCapsTable")
        roundCornersTable = self.w.getItem("roundCornersTable")

        roundCapsTable.set([])
        roundCornersTable.set([])

        roundingDict = self.roundingDict.get(self.glyph.name)

        if roundingDict:

            roundCaps = roundingDict.get('caps')
            if roundCaps:
                roundCapsItems = []
                for pt1, pt2 in roundCaps:
                    roundCapsItem = roundCapsTable.makeItem()
                    roundCapsItem['point1'] = pt1
                    roundCapsItem['point2'] = pt2
                    roundCapsItems.append(roundCapsItem)
                roundCapsTable.set(roundCapsItems)

            roundCorners = roundingDict.get('corners')
            if roundCorners:
                roundCornersItems = []
                for pt in roundCorners:
                    roundCornersItem = roundCornersTable.makeItem()
                    roundCornersItem['point'] = pt
                    roundCornersItems.append(roundCornersItem)
                roundCornersTable.set(roundCornersItems)


class RoundingSubscriberRoboFont(Subscriber):

    controller = None

    def fontDocumentDidBecomeCurrent(self, info):
        self.controller.font = info['font']
        self.controller._updateRoundingTables()

    def fontDocumentDidOpen(self, info):
        self.controller.font = info['font']
        self.controller._updateRoundingTables()

    def roboFontDidSwitchCurrentGlyph(self, info):
        glyph = info["glyph"]
        if self.controller.glyph is not None and glyph is not None:
            if glyph.name == self.controller.glyph.name:
                return

        # self.controller._updateRoundingDict()
        self.controller.glyph = info["glyph"]
        self.controller._updateRoundingTables()

        postEvent(f"{self.controller.key}.changed")

    def roundingDidChange(self, info):
        self.controller._updateRoundingTables()


class RoundingSubscriberGlyphEditor(Subscriber):

    controller  = None
    strokeWidth = 2

    def build(self):
        glyphEditor = self.getGlyphEditor()

        containerForeground = glyphEditor.extensionContainer(
            identifier=f"{self.controller.key}.foreground",
            location="foreground",
        )
        self.roundingLayer = containerForeground.appendBaseSublayer()

        containerPreview = glyphEditor.extensionContainer(
            identifier=f"{self.controller.key}.preview",
            location="preview",
            clear=True,
        )
        self.roundingLayerPreview = containerPreview.appendBaseSublayer()

        self._drawGlyphRounding()

    def destroy(self):
        self.roundingLayer.clearSublayers()

    def glyphEditorGlyphDidChange(self, info):
        self._drawGlyphRounding()

    def roundingDidChange(self, info):
        self._drawGlyphRounding()

    def _drawGlyphRounding(self):

        preview = self.controller.w.getItem("preview").get()
        color   = self.controller.w.getItem("colorButton").get()

        if not preview:
            return

        glyph = self.controller.glyph
        if glyph is None:
            return

        self.roundingLayer.clearSublayers()
        self.roundingLayerPreview.clearSublayers()

        roundingDict = self.controller.roundingDict.get(glyph.name)

        if not roundingDict:
            return

        roundCaps    = roundingDict.get('caps', [])
        roundCorners = roundingDict.get('corners', [])

        xStem  = getStem(self.controller.font['I'], self.controller.font.info.xHeight / 2)
        radius = xStem / 2

        glyph.lib[KEY] = {
            'caps'    : roundCaps,
            'corners' : [(pt,) for pt in roundCorners],
            'radius'  : radius,
        }
        # get rounded glyph
        roundedGlyph = glyph.getRepresentation(KEY)

        # draw rounded glyph
        glyphPaths = roundedGlyph.getRepresentation(
            "merz.CGPath",
            contours=True,
            components=True
        )

        roundedGlyphLayer = self.roundingLayer.appendPathSublayer()
        roundedGlyphLayer.setPath(glyphPaths)
        roundedGlyphLayer.setFillColor(color)

        roundedGlyphLayerPreview = self.roundingLayerPreview.appendPathSublayer()
        roundedGlyphLayerPreview.setBackgroundColor((1, 1, 0, 1))
        roundedGlyphLayerPreview.setPath(glyphPaths)
        roundedGlyphLayerPreview.setFillColor((0, 0, 1, 1))



roundingEventName = f"{RoundingController.key}.changed"


if roundingEventName not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=roundingEventName,
        methodName="roundingDidChange",
        lowLevelEventNames=[roundingEventName],
        documentation="Send when the rounding tool changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(RoundingController)


