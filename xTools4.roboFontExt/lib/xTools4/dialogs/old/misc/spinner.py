from vanilla import Group, TextBox, SquareButton, EditText


class Spinner(Group):

    buttonNudge = 18
    padding     = 10
    sizeStyle   = 'small'

    def __init__(self, pos, default=0, scale=1, integer=True, label=None, digits=2, isHorizontal=False, buttonPairs=3, col2=None, callback=None):

        x, y = pos
        p = self.padding
        w = self.buttonNudge * 6 - 5

        if not col2:
            col2 = w * 0.5

        if isHorizontal:
            h = self.buttonNudge
            w *= 2
            w += p
        else:
            h = self.buttonNudge * 2 + p

        super(Spinner, self).__init__((x, y, w, h))

        self.callback = callback
        self.scale    = scale
        self.integer  = integer
        self.digits   = digits

        x = y = 0
        if label is not None:
            self._label = TextBox(
                    (x, y, col2, self.buttonNudge),
                    label,
                    sizeStyle=self.sizeStyle)
            x += col2
            self._value = EditText(
                    (x, y, col2, self.buttonNudge),
                    default,
                    sizeStyle=self.sizeStyle)
            x += col2 + p
            # self._label.getNSTextField().setDrawsBackground_(False)
            # self._label.getNSTextField().setBordered_(False)

        else:
            self._value = EditText(
                    (x, y, w, self.buttonNudge),
                    default,
                    sizeStyle=self.sizeStyle)
            x += w + p

        if not isHorizontal:
            x = 0
            y += self.buttonNudge + p

        self.minus001 = SquareButton(
                (x, y, self.buttonNudge, self.buttonNudge),
                '-',
                sizeStyle=self.sizeStyle,
                callback=self.minus001Callback)

        x += self.buttonNudge - 1
        self.plus001 = SquareButton(
                (x, y, self.buttonNudge, self.buttonNudge),
                '+',
                sizeStyle=self.sizeStyle,
                callback=self.plus001Callback)

        if buttonPairs > 1:

            x += self.buttonNudge - 1
            self.minus010 = SquareButton(
                    (x, y, self.buttonNudge, self.buttonNudge),
                    '-',
                    sizeStyle=self.sizeStyle,
                    callback=self.minus010Callback)

            x += self.buttonNudge - 1
            self.plus010 = SquareButton(
                    (x, y, self.buttonNudge, self.buttonNudge),
                    '+',
                    sizeStyle=self.sizeStyle,
                    callback=self.plus010Callback)

            if buttonPairs > 2:

                x += self.buttonNudge - 1
                self.minus100 = SquareButton(
                        (x, y, self.buttonNudge, self.buttonNudge),
                        '-',
                        sizeStyle=self.sizeStyle,
                        callback=self.minus100Callback)

                x += self.buttonNudge - 1
                self.plus100 = SquareButton(
                        (x, y, self.buttonNudge, self.buttonNudge),
                        '+',
                        sizeStyle=self.sizeStyle,
                        callback=self.plus100Callback)

    @property
    def value(self):
        value = self._value.get()
        if self.integer:
            value = str(value).replace('.', '')
            return int(value)
        else:
            value = value.replace(',', '.')
            return float(value)

    @value.setter
    def value(self, inputValue):
        if self.integer:
            value = int(inputValue)
            value = str(value)
        else:
            value = float(inputValue)
            if self.digits == 4:
                value = '%.4f' % inputValue
            elif self.digits == 3:
                value = '%.3f' % inputValue
            else:
                value = '%.2f' % inputValue
        self._value.set(value)

    @property
    def height(self):
        return self.getPosSize()[3]

    @property
    def width(self):
        return self.getPosSize()[4]

    def _callback(self, sender):
        if self.callback:
            exec('self.callback(sender)')

    def minus001Callback(self, sender):
        value = self.value
        value -= 1 * self.scale
        self.value = value
        self._callback(sender)

    def plus001Callback(self, sender):
        value = self.value
        value += 1 * self.scale
        self.value = value
        self._callback(sender)

    def minus010Callback(self, sender):
        value = self.value
        value -= 10 * self.scale
        self.value = value
        self._callback(sender)

    def plus010Callback(self, sender):
        value = self.value
        value += 10 * self.scale
        self.value = value
        self._callback(sender)

    def minus100Callback(self, sender):
        value = self.value
        value -= 100 * self.scale
        self.value = value
        self._callback(sender)

    def plus100Callback(self, sender):
        value = self.value
        value += 100 * self.scale
        self.value = value
        self._callback(sender)

if __name__ == '__main__':

    from hTools3.dialogs import hDialog

    class SpinnerGroupDemo1(hDialog):

        def __init__(self):
            self.height = self.spinnerHeight + self.padding * 2
            self.windowType = 1
            self.w = self.window((self.width, self.height), 'spinner')
            x = y = p = self.padding
            self.w.spinner = Spinner(
                    (x, y),
                    default=20,
                    integer=True,
                    label='value')
            self.w.open()

    SpinnerGroupDemo1()

    class SpinnerGroupDemo2(hDialog):

        def __init__(self):
            self.width = self.width * 2 - self.padding
            self.height = self.buttonNudge + self.padding * 2
            self.windowType = 1
            self.w = self.window((self.width, self.height), 'spinner')
            x = y = p = self.padding
            self.w.spinner = Spinner(
                    (x, y),
                    default='%.2f'%50,
                    scale=0.1,
                    integer=False,
                    isHorizontal=True,
                    label='value')
            self.w.open()

    SpinnerGroupDemo2()
