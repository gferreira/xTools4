import ezui
from merz import MerzView
from mojo.UI import GetFile
from mojo.roboFont import OpenWindow, OpenFont
from mojo.subscriber import Subscriber, registerSubscriberEvent, roboFontSubscriberEventRegistry, registerGlyphEditorSubscriber, unregisterGlyphEditorSubscriber
from mojo.events import postEvent
from variableValues.linkPoints import readMeasurements
from variableValues.measurements import Measurement


class GlyphGauge_EZUI(ezui.WindowController):

    title   = 'gauge'
    key     = 'com.fontBureau.glyphGauge'
    width   = 123
    margins = 10

    defaultPath = None
    defaultFont = None

    measurementsPath = None
    measurementsData = None

    content = """
    ( measurements… )  @getMeasurementsButton
    ( reload ↺ )       @reloadMeasurementsButton

    ( get default… )   @getDefaultButton
    ( reload ↺ )       @reloadDefaultButton

    (X) font value     @parent
    ( ) default value  

    font tolerance
    [__](±)            @toleranceFont

    default tolerance
    [__](±)            @toleranceDefault

    (X) em units       @permille
    ( ) per mille      

    [X] display        @display
    """

    colorCheckTrue  = 0.00, 0.85, 0.00, 1.00
    colorCheckFalse = 1.00, 0.00, 0.00, 1.00
    colorCheckEqual = 0.00, 0.33, 1.00, 1.00

    descriptionData = dict(
        content=dict(
            sizeStyle="small",
        ),
        getDefaultButton=dict(
            width='fill',
        ),
        reloadDefaultButton=dict(
            width='fill',
        ),
        getMeasurementsButton=dict(
            width='fill',
        ),
        reloadMeasurementsButton=dict(
            width='fill',
        ),
        toleranceFont=dict(
            callback='settingsChangedCallback',
            valueType="float",
            value=0.10,
            minValue=0.0,
            maxValue=5.0,
            valueIncrement=0.01,
        ),
        toleranceDefault=dict(
            callback='settingsChangedCallback',
            valueType="float",
            value=0.10,
            minValue=0.0,
            maxValue=5.0,
            valueIncrement=0.01,
        ),
        display=dict(
            callback='settingsChangedCallback',
        ),
    )

    def build(self):
        self.w = ezui.EZPanel(
            title=self.title,
            content=self.content,
            descriptionData=self.descriptionData,
            controller=self,
            margins=self.margins,
            size=(self.width, 'auto'),
        )
        self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
        self.w.open()

    def started(self):
        GlyphGaugeSubscriberGlyphEditor.controller = self
        registerGlyphEditorSubscriber(GlyphGaugeSubscriberGlyphEditor)
        self.settingsChangedCallback(None)

    def destroy(self):
        unregisterGlyphEditorSubscriber(GlyphGaugeSubscriberGlyphEditor)
        GlyphGaugeSubscriberGlyphEditor.controller = None

    # callbacks

    def getDefaultButtonCallback(self, sender):
        self.defaultPath = GetFile(message='Get default source…', title=self.title)
        self.defaultFont = OpenFont(self.defaultPath, showInterface=False)
        self.settingsChangedCallback(None)

    def reloadButtonCallback(self, sender):
        if self.defaultFont is None:
            return
        self.defaultFont = OpenFont(self.defaultPath, showInterface=False)
        self.settingsChangedCallback(None)

    def getMeasurementsButtonCallback(self, sender):
        self.measurementsPath = GetFile(message='Get measurements file…', title=self.title)
        self.measurementsData = readMeasurements(self.measurementsPath)
        self.settingsChangedCallback(None)

    def reloadMeasurementsButtonCallback(self, sender):
        if self.measurementsPath is None:
            return
        self.measurementsData = readMeasurements(self.measurementsPath)
        self.settingsChangedCallback(None)

    def parentCallback(self, sender):
        self.settingsChangedCallback(None)

    def permilleCallback(self, sender):
        self.settingsChangedCallback(None)

    def settingsChangedCallback(self, sender):
        postEvent(f"{self.key}.changed")


class GlyphGaugeSubscriberGlyphEditor(Subscriber):

    controller = None

    def build(self):
        sizeX, sizeY = 250, 1000
        glyphEditor = self.getGlyphEditor()
        self.merzView = MerzView((-sizeX, 0, sizeX, sizeY))
        merzContainer = self.merzView.getMerzContainer()
        self.gaugeLayer = merzContainer.appendTextBoxSublayer(
            name=f'{self.controller.key}.gauge',
            position=(0, 0),
            size=(sizeX, sizeY),
            padding=(10, 10),
            font='Menlo-Bold',
            fillColor=self.controller.colorCheckEqual,
            pointSize=13,
            horizontalAlignment="left",
            verticalAlignment="top",
        )
        glyphEditor.addGlyphEditorSubview(self.merzView)
        self._drawGlyphGauge()

    def destroy(self):
        glyphEditor = self.getGlyphEditor()
        glyphEditor.removeGlyphEditorSubview(self.merzView)

    def glyphEditorDidSetGlyph(self, info):
        self.glyph = info["glyph"]
        self._drawGlyphGauge()

    def glyphEditorGlyphDidChange(self, info):
        self._drawGlyphGauge()

    def glyphGaugeDidChange(self, info):
        self._drawGlyphGauge()

    def _drawGlyphGauge(self):

        if not self.controller.w.getItem('display').get():
            self.gaugeLayer.setVisible(False)
            return
        else:
            self.gaugeLayer.setVisible(True)

        if self.controller.defaultFont is None:
            return

        if not self.controller.measurementsData:
            return

        if self.glyph.name not in self.controller.defaultFont:
            return

        glyphsMeasurements = self.controller.measurementsData['glyphs']

        if not glyphsMeasurements.get(self.glyph.name):
            return

        parent = not self.controller.w.getItem('parent').get()

        if not parent:
            self._drawTable1(self.glyph.font, self.glyph)
        else:
            self._drawTable2(self.glyph.font, self.glyph)

    def _drawTable1(self, font, glyph):

        permille  = self.controller.w.getItem('permille').get()
        tolerance = self.controller.w.getItem('toleranceDefault').get()

        txt = []

        if not permille:
            txt.append(
                dict(
                    text=f"{'name'.ljust(4, ' ')} {'units'.rjust(5, ' ')} {'deflt'.rjust(5, ' ')} {'scale'.rjust(5, ' ')}\n",
                    fillColor=self.controller.colorCheckEqual,
                ),
            )
        else:
            txt.append(
                dict(
                    text=f"{'name'.ljust(4, ' ')} {'perml'.rjust(5, ' ')} {'deflt'.rjust(5, ' ')} {'scale'.rjust(5, ' ')}\n",
                    fillColor=self.controller.colorCheckEqual,
                ),
            )

        txt.append(
            dict(
                text=f"{'-' * (len(txt[0]['text'])-1)}\n",
                fillColor=self.controller.colorCheckEqual,
            ),
        )

        glyphMeasurements = self.controller.measurementsData['glyphs'].get(glyph.name)

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
            measurementName = glyphMeasurements[key].get('name')
            M = Measurement(
                measurementName,
                glyphMeasurements[key].get('direction'),
                glyph.name, index1,
                glyph.name, index2,
                glyphMeasurements[key].get('parent'))

            # measure font
            valueUnits = M.measure(font)
            if valueUnits is None:
                valueUnits = valuePermill = '-'
            elif valueUnits == 0:
                valuePermill = 0
            else:
                valuePermill = round(valueUnits*1000 / font.info.unitsPerEm)

            # measure default
            defaultUnits = M.measure(self.controller.defaultFont)
            if defaultUnits is None:
                defaultUnits = defaultPermille = '-'
            elif defaultUnits == 0:
                defaultPermille = 0
            else:
                defaultPermille = round(defaultUnits*1000 / self.controller.defaultFont.info.unitsPerEm)

            # draw table item
            color = self.controller.colorCheckEqual

            # calculate scale factor
            if valueUnits == defaultUnits:
                scaleValue = 1.0
            elif valueUnits == 0 or defaultUnits == 0:
                scaleValue = '-'
            else:
                scaleValue = valueUnits / defaultUnits
                if (1.0 - tolerance) < scaleValue < (1.0 + tolerance):
                    color = self.controller.colorCheckTrue
                else:
                    color = self.controller.colorCheckFalse
            if not isinstance(scaleValue, str):
                scaleValue = f"{scaleValue:.2f}"

            if not permille:
                txt.append(
                    dict(
                        text=f"{measurementName.ljust(4, ' ')} {str(valueUnits).rjust(5, ' ')} {str(defaultUnits).rjust(5, ' ')} {scaleValue.rjust(5, ' ')}\n",
                        fillColor=color,
                    ),
                )
            else:
                txt.append(
                    dict(
                        text=f"{measurementName.ljust(4, ' ')} {str(valuePermill).rjust(5, ' ')} {str(defaultPermille).rjust(5, ' ')} {scaleValue.rjust(5, ' ')}\n",
                        fillColor=color,
                    ),
                )

        with self.gaugeLayer.propertyGroup():
            self.gaugeLayer.setFillColor(color)
            self.gaugeLayer.setText(txt)

    def _drawTable2(self, font, glyph):

        permille  = self.controller.w.getItem('permille').get()
        tolerance = self.controller.w.getItem('toleranceFont').get()

        txt = []

        if not permille:
            txt.append(
                dict(
                    text=f"{'name'.ljust(4, ' ')} {'units'.rjust(5, ' ')} {'font'.rjust(5, ' ')} {'scale'.rjust(5, ' ')}  {'glyph'.rjust(5, ' ')}\n",
                    fillColor=self.controller.colorCheckEqual,
                ),
            )
        else:
            txt.append(
                dict(
                    text=f"{'name'.ljust(4, ' ')} {'perml'.rjust(5, ' ')} {'font'.rjust(5, ' ')} {'scale'.rjust(5, ' ')}  {'glyph'.rjust(5, ' ')}\n",
                    fillColor=self.controller.colorCheckEqual,
                ),
            )

        txt.append(
            dict(
                text=f"{'-' * (len(txt[0]['text'])-1)}\n",
                fillColor=self.controller.colorCheckEqual,
            ),
        )

        glyphMeasurements = self.controller.measurementsData['glyphs'].get(glyph.name)
        fontMeasurements  = self.controller.measurementsData['font']

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
            measurementName = glyphMeasurements[key].get('name')
            M = Measurement(measurementName,
                glyphMeasurements[key].get('direction'),
                glyph.name, index1,
                glyph.name, index2,
                glyphMeasurements[key].get('parent'))

            # measure font
            valueUnits = M.measure(font)
            if valueUnits is None:
                valueUnits = valuePermill = '-'
            elif valueUnits == 0:
                valuePermill = 0
            else:
                valuePermill = round(valueUnits*1000 / font.info.unitsPerEm)

            # measure parent value
            if measurementName in fontMeasurements:
                fontMeasurement = fontMeasurements[measurementName]
                index1 = fontMeasurement.get('point 1')
                index2 = fontMeasurement.get('point 2')

                try:
                    index1 = int(index1)
                except:
                    pass
                try:
                    index2 = int(index2)
                except:
                    pass

                glyph1 = fontMeasurement.get('glyph 1')
                glyph2 = fontMeasurement.get('glyph 2')

                M2 = Measurement(measurementName,
                    fontMeasurement.get('direction'),
                    glyph1, index1, glyph2, index2)

                parentUnits = M2.measure(font)

                if parentUnits is None:
                    parentUnits = parentPermille = '-'
                elif parentUnits == 0:
                    parentPermille = 0
                else:
                    parentPermille = round(parentUnits*1000 / self.controller.defaultFont.info.unitsPerEm)

                # calculate scale factor and assign colors
                color = self.controller.colorCheckEqual

                if valueUnits == parentUnits:
                    scaleValue = 1.0
                elif valueUnits == 0 or parentUnits == 0:
                    scaleValue = '-'
                else:
                    scaleValue = valueUnits / parentUnits
                    # use absolute value when comparing to parent measurement
                    # disregard direction is needed to check overshoots, serifs, etc.
                    if (1.0 - tolerance) < scaleValue < (1.0 + tolerance):
                        color = self.controller.colorCheckTrue
                    else:
                        color = self.controller.colorCheckFalse
                if not isinstance(scaleValue, str):
                    scaleValue = f"{scaleValue:.2f}"

            else:
                parentUnits = '-'
                scaleValue  = '-'

            if not permille:
                txt.append(
                    dict(
                        text=f"{measurementName.ljust(4, ' ')} {str(valueUnits).rjust(5, ' ')} {str(parentUnits).rjust(5, ' ')} {scaleValue.rjust(5, ' ')}  {glyph1.ljust(5, ' ')}\n",
                        fillColor=color,
                    ),
                )
            else:
                txt.append(
                    dict(
                        text=f"{measurementName.ljust(4, ' ')} {str(valuePermill).rjust(5, ' ')} {str(parentPermille).rjust(5, ' ')} {scaleValue.rjust(5, ' ')}  {glyph1.ljust(5, ' ')}\n",
                        fillColor=color,
                    ),
                )

        with self.gaugeLayer.propertyGroup():
            self.gaugeLayer.setFillColor(color)
            self.gaugeLayer.setText(txt)


eventName = f"{GlyphGauge_EZUI.key}.changed"

if eventName not in roboFontSubscriberEventRegistry:
    registerSubscriberEvent(
        subscriberEventName=eventName,
        methodName="glyphGaugeDidChange",
        lowLevelEventNames=[eventName],
        documentation="Send when the GlyphGauge window changes its parameters.",
        dispatcher="roboFont",
        delay=0,
        debug=True
    )


if __name__ == '__main__':

    OpenWindow(GlyphGauge_EZUI)
