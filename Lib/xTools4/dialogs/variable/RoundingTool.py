from importlib import reload
import xTools4.modules.linkPoints2
reload(xTools4.modules.linkPoints2)
import xTools4.modules.measurements
reload(xTools4.modules.measurements)

import os, json
from random import random
import ezui
from merz import MerzView, MerzPen
from mojo import drawingTools as ctx
from mojo.UI import PutFile, GetFile, CurrentFontWindow
from mojo.roboFont import OpenFont, CurrentFont, CurrentGlyph
# from mojo.subscriber import Subscriber, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber, registerRoboFontSubscriber, unregisterRoboFontSubscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry
# from mojo.events import postEvent, addObserver, removeObserver


KEY = 'com.xTools4.roundingTool'


class RoundingController(ezui.WindowController):

    title       = 'RoundingTool'
    key         = KEY
    buttonWidth = 75
    verbose     = False
    messageMode = 1

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
    > |----------------|
    > | point | radius | @roundCornersTable
    > |-------|--------|
    > |       |        |
    > |----------------|
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
                    identifier="radius",
                    title="radius",
                    width=55,
                    editable=True,
                    continuous=False,
                ),
            ],
        ),
        colorButton=dict(
            color=(1, 0.3, 0, 0.8),
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
            size=('auto', 400),
            # minSize=('auto', 400),
        )
        self.w.workspaceWindowIdentifier = self.title
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.getItem("roundCapsTable").getNSTableView().setRowHeight_(17)
        self.w.getItem("roundCornersTable").getNSTableView().setRowHeight_(17)
        self.w.open()

    # def started(self):
    #     MeasurementsSubscriberRoboFont.controller = self
    #     registerRoboFontSubscriber(MeasurementsSubscriberRoboFont)
    #     MeasurementsSubscriberGlyphEditor.controller = self
    #     registerGlyphEditorSubscriber(MeasurementsSubscriberGlyphEditor)
    #     addObserver(self, "drawLabelCell", "glyphCellDrawBackground")
    #     self.font  = CurrentFont()
    #     self.glyph = CurrentGlyph()

    # def destroy(self):
    #     unregisterRoboFontSubscriber(MeasurementsSubscriberRoboFont)
    #     MeasurementsSubscriberRoboFont.controller = None
    #     unregisterGlyphEditorSubscriber(MeasurementsSubscriberGlyphEditor)
    #     MeasurementsSubscriberGlyphEditor.controller = None
    #     removeObserver(self, "glyphCellDrawBackground")

if __name__ == '__main__':

    OpenWindow(RoundingController)
