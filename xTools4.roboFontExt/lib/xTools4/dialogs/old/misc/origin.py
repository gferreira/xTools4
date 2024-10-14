from vanilla import Group, CheckBox


class OriginPoint(Group):

    allPositions = [
        'topLeft', 'topCenter', 'topRight',
        'middleLeft', 'middleCenter', 'middleRight',
        'bottomLeft', 'bottomCenter', 'bottomRight',
    ]

    def __init__(self, posSize, positions=None, allowEmpty=True, callback=None):

        x, y, w, h = posSize
        lineHeight = 20
        lineScale  = 2
        sizeStyle  = 'small'

        super(OriginPoint, self).__init__((0, 0, w, h))

        self.callback   = callback
        self.allowEmpty = allowEmpty

        col = int((w - 20) / 3)

        _y = y + 5
        _x = x + 10
        self.topLeft = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.topLeftCallback)

        _x += col
        self.topCenter = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.topCenterCallback)

        _x += col
        self.topRight = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.topRightCallback)

        _x = x + 10
        _y += lineHeight + 14
        self.middleLeft = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.middleLeftCallback)

        _x += col
        self.middleCenter = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=True,
                callback=self.middleCenterCallback)

        _x += col
        self.middleRight = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.middleRightCallback)

        _x = x + 10
        _y += lineHeight + 14
        self.bottomLeft = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.bottomLeftCallback)

        _x += col
        self.bottomCenter = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.bottomCenterCallback)

        _x += col
        self.bottomRight = CheckBox(
                (_x, _y, col, lineHeight),
                '',
                value=False,
                callback=self.bottomRightCallback)

    def setPosition(self, posName):
        # clear positions
        if posName is None:
            for p in self.allPositions:
                checkbox = getattr(self, p)
                checkbox.set(False)
        # named position
        elif posName in self.allPositions:
            for p in self.allPositions:
                checkbox = getattr(self, p)
                if p == posName:
                    checkbox.set(True)
                else:
                    checkbox.set(False)
        # position not valid
        else:
            return

    @property
    def selected(self):
        for pos in self.allPositions:
            checkbox = getattr(self, pos)
            if checkbox.get():
                return pos

    @property
    def height(self):
        return self.getPosSize()[3]

    @property
    def width(self):
        return self.getPosSize()[4]

    def _callback(self, sender):
        if self.callback:
            exec('self.callback(sender)')

    def selectPosition(self, position):
        for pos in self.allPositions:
            if pos != position:
                checkbox = getattr(self, pos)
                checkbox.set(False)

    def topLeftCallback(self, sender):
        if sender.get():
            self.selectPosition('topLeft')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def topCenterCallback(self, sender):
        if sender.get():
            self.selectPosition('topCenter')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def topRightCallback(self, sender):
        if sender.get():
            self.selectPosition('topRight')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def middleLeftCallback(self, sender):
        if sender.get():
            self.selectPosition('middleLeft')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def middleCenterCallback(self, sender):
        if sender.get():
            self.selectPosition('middleCenter')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def middleRightCallback(self, sender):
        if sender.get():
            self.selectPosition('middleRight')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def bottomLeftCallback(self, sender):
        if sender.get():
            self.selectPosition('bottomLeft')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def bottomCenterCallback(self, sender):
        if sender.get():
            self.selectPosition('bottomCenter')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

    def bottomRightCallback(self, sender):
        if sender.get():
            self.selectPosition('bottomRight')
        else:
            if not self.allowEmpty:
                sender.set(True)
        self._callback(sender)

if __name__ == '__main__':

    from hTools3.dialogs import hDialog

    class OriginPointDemo(hDialog):

        def __init__(self):
            self.height = self.width
            self.windowType = 0
            self.w = self.window((self.width, self.height), 'origin')
            x = y = p = self.padding
            self.w.origin = OriginPoint((x, y, self.width, self.height))
            self.w.open()

    OriginPointDemo()
