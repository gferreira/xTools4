from vanilla import SquareButton, Group


class Arrows(Group):

    allArrows = [
        'top', 'down', 'left', 'right', 'center',
        'leftUp', 'leftDown', 'rightUp', 'rightDown',
    ]

    largeButton = 35
    smallButton = largeButton - 9
    sizeStyle   = 'small'

    def __init__(self, posSize, callbacks=dict(), arrows=None):

        x0, y0, w, h = posSize

        super(Arrows, self).__init__((0, 0, w, h))

        d = self.largeButton - self.smallButton
        x1 = x0 + self.largeButton - 1
        y1 = y0 + self.largeButton - 1
        x2 = x1 + self.largeButton - 1
        y2 = y1 + self.largeButton - 1
        x3 = x2 + d
        y3 = y2 + d

        if arrows is None:
            arrows = self.allArrows

        for arrow in arrows:

            if arrow == 'center':
                xc = x1 + int(d * 0.5)
                yc = y1 + int(d * 0.5)
                self.center = SquareButton(
                    (xc, yc, self.smallButton, self.smallButton),
                    u'⦿',
                    callback=callbacks["center"])
                self.left.bind("left", [])

            if arrow == 'left':
                self.left = SquareButton(
                    (x0, y1, self.largeButton, self.largeButton),
                    u'←',
                    callback=callbacks["left"])
                self.left.bind("left", [])

            if arrow == 'down':
                self.down = SquareButton(
                    (x1, y2, self.largeButton, self.largeButton),
                    u'↓',
                    callback=callbacks["down"])
                self.down.bind("down", [])

            if arrow == 'right':
                self.right = SquareButton(
                    (x2, y1, self.largeButton, self.largeButton),
                    u'→',
                    callback=callbacks["right"])
                self.right.bind("right", [])

            if arrow == 'up':
                self.up = SquareButton(
                    (x1, y0, self.largeButton, self.largeButton),
                    u'↑',
                    callback=callbacks["up"])
                self.up.bind("up", [])

            if arrow == 'leftUp':
                self.leftUp = SquareButton(
                    (x0, y0, self.smallButton, self.smallButton),
                    u'↖',
                    sizeStyle=self.sizeStyle,
                    callback=callbacks["leftUp"])
                self.leftUp.bind("leftUp", [])

            if arrow == 'leftDown':
                self.leftDown = SquareButton(
                    (x0, y3, self.smallButton, self.smallButton),
                    u'↙',
                    sizeStyle=self.sizeStyle,
                    callback=callbacks["leftDown"])
                self.leftDown.bind("leftDown", [])

            if arrow == 'rightDown':
                self.rightUp = SquareButton(
                    (x3, y3, self.smallButton, self.smallButton),
                    u'↘',
                    sizeStyle=self.sizeStyle,
                    callback=callbacks["rightDown"])
                self.rightUp.bind("rightDown", [])

            if arrow == 'rightUp':
                self.rightDown = SquareButton(
                    (x3, y0, self.smallButton, self.smallButton),
                    u'↗',
                    sizeStyle=self.sizeStyle,
                    callback=callbacks["rightUp"])
                self.rightDown.bind("rightUp", [])

    @property
    def height(self):
        return self.getPosSize()[3]

    @property
    def width(self):
        return self.getPosSize()[4]

if __name__ == '__main__':

    from hTools3.dialogs import hDialog

    class ArrowsGroupDemo(hDialog):

        def __init__(self):
            self.height = self.width
            self.windowType = 1
            self.w = self.window((self.width, self.height), 'arrows')
            x = y = p = self.padding
            callbacksDict = {
                'center'    : self.centerCallback,
                'left'      : self.leftCallback,
                'right'     : self.rightCallback,
                'up'        : self.upCallback,
                'down'      : self.downCallback,
                'leftDown'  : self.downLeftCallback,
                'rightDown' : self.downRightCallback,
                'leftUp'    : self.upLeftCallback,
                'rightUp'   : self.upRightCallback,
            }
            self.w.arrows = Arrows(
                (x, y, self.width, self.height),
                callbacks=callbacksDict,
                arrows=[
                    'left', 'right', 'up', 'down', 'center',
                    'leftUp', 'leftDown', 'rightUp', 'rightDown',
                ],
            )
            self.w.open()

        def centerCallback(self, sender):
            print('OO (center)')

        def upLeftCallback(self, sender):
            print('NW (up left)')

        def upRightCallback(self, sender):
            print('NE (up right)')

        def downLeftCallback(self, sender):
            print('SW (down left)')

        def downRightCallback(self, sender):
            print('SE (down right)')

        def leftCallback(self, sender):
            print('WW (left)')

        def rightCallback(self, sender):
            print('EE (right)')

        def upCallback(self, sender):
            print('NN (up)')

        def downCallback(self, sender):
            print('SS (down)')

    ArrowsGroupDemo()
