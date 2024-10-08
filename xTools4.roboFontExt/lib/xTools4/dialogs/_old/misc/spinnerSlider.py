import AppKit
from vanilla import Group, TextBox, Slider, HorizontalLine
from hTools3.dialogs import hDialog
from mojo.UI import EditStepper


class SpinnerSlider(Group):

    width         = hDialog.width
    padding       = hDialog.padding
    textHeight    = hDialog.textHeight
    stepperHeight = 22
    sizeStyle     = 'small'

    def __init__(self, posSize, value, label='value', minValue=0, maxValue=999, increment=None, autoRepeat=False, callback=None, sizeStyle="regular", inputWidth=80, sliderStyle="slider"):

        super(SpinnerSlider, self).__init__(posSize)
        self._callback = callback

        x = y = 0
        p = self.padding
        inputWidth = ((self.width - p*2) / 2) + 2

        self.label = TextBox(
                (x, y, inputWidth, hDialog.textHeight),
                label,
                sizeStyle=sizeStyle)

        self.stepper = EditStepper(
                (x + inputWidth, y, inputWidth, self.stepperHeight),
                value=value,
                minValue=minValue,
                maxValue=maxValue,
                increment=increment,
                autoRepeat=autoRepeat,
                sizeStyle=sizeStyle,
                callback=self._stepperCallback)

        y += self.stepperHeight + p * 0.5
        self.slider = Slider(
                (x, y, -0, self.textHeight),
                callback=self._sliderCallback,
                minValue=minValue,
                maxValue=maxValue,
                value=value,
                sizeStyle=self.sizeStyle)

    # dynamic attrs.

    @property
    def value(self):
        return self.slider.get()

    @value.setter
    def value(self, value):
        self.slider.set(value)
        self.stepper.set(value)

    @property
    def height(self):
        return self.stepperHeight + hDialog.textHeight + hDialog.padding * 0.5

    # callbacks

    def _sliderCallback(self, sender):
        value = float(sender.get())
        self.stepper.set(value)
        if self._callback is not None:
            self._callback(self)

    def _stepperCallback(self, sender):
        value = sender.get()

        # modifiers  = AppKit.NSEvent.modifierFlags()
        # cmdDown    = modifiers & AppKit.NSEventModifierFlagCommand
        # shiftDown  = modifiers & AppKit.NSEventModifierFlagShift
        # optionDown = modifiers & AppKit.NSEventModifierFlagOption

        # if cmdDown:
        #     value *= 10
        # elif shiftDown:
        #     value *= 100
        # elif optionDown:
        #     value *= 0.1

        self.slider.set(value)
        if self._callback is not None:
            self._callback(self)

    # methods

    def enable(self, value):
        self.slider.enable(value)
        self.stepper.enable(value)

# -------
# testing
# -------

if __name__ == '__main__':

    class SpinnerSliderDemo(hDialog):

        def __init__(self):
            self.height = 300
            self.windowType = 1
            self.w = self.window((self.width, self.height), "test")
            x = y = p = self.padding
            self.w.stepper = SpinnerSlider(
                    (x, y, -p, 333),
                    value=1.25,
                    minValue=0.01,
                    maxValue=10.0,
                    increment=0.1,
                    label='test',
                    sizeStyle='small',
                    callback=self.stepperCallback)
            y += self.w.stepper.height + p
            self.w.line = HorizontalLine((x, y, -p, 1))
            self.w.open()

        def stepperCallback(self, sender):
            print(self.w.stepper.value)

    SpinnerSliderDemo()
