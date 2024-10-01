from importlib import reload

from vanilla import *
from mojo import drawingTools as ctx
from mojo.UI import UpdateCurrentGlyphView, getDefault
from mojo.events import addObserver, removeObserver
from hTools3.dialogs.glyphs.base import GlyphsDialogBase
from hTools3.modules.color import rgb2nscolor, nscolor2rgb


class BoxMarginsTool(GlyphsDialogBase):

    title = 'cast'
    key   = f'{GlyphsDialogBase.key}.boxMargins'
    settings = {
        'captionFontSize' : 13,
        'marginsColor' : (1, 0, 0.5, 0.25),
    }

    # read some user settings for use later
    glyphViewColor  = getDefault("glyphViewMarginColor")
    glyphViewHeight = getDefault("glyphViewDefaultHeight") / 2.0
    useItalicAngle  = getDefault("glyphViewShouldUseItalicAngleForDisplay")

    def __init__(self):
        self.height  = self.textHeight * 5
        self.height += self.buttonHeight
        self.height += self.padding * 5
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.drawBox = CheckBox(
            (x, y, -p, self.textHeight),
            'box',
            value=True,
            sizeStyle=self.sizeStyle,
            callback=self.updateViewCallback)

        y += self.textHeight
        self.w.drawMargins = CheckBox(
            (x, y, -p, self.textHeight),
            'margins',
            value=True,
            sizeStyle=self.sizeStyle,
            callback=self.updateViewCallback)

        y += self.textHeight + p
        self.w.marginsColor = ColorWell(
                (x, y, -p, self.buttonHeight),
                callback=self.updatePreviewCallback,
                color=rgb2nscolor(self.settings['marginsColor']))

        y += self.buttonHeight + p # * 0.75
        self.w.captionFontSizeLabel = TextBox(
                (x, y, -p, self.textHeight),
                "caption size",
                sizeStyle=self.sizeStyle)

        y += self.textHeight
        valueMin  = 11
        valueMax  = 20
        tickCount = valueMax - valueMin
        self.w.captionFontSize = Slider(
                (x, y, -p, self.textHeight),
                value=self.settings['captionFontSize'],
                minValue=valueMin,
                maxValue=valueMax,
                tickMarkCount=tickCount,
                stopOnTickMarks=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        self.w.preview = CheckBox(
                (x, y, -p, self.textHeight),
                "preview",
                value=True,
                callback=self.updatePreviewCallback,
                sizeStyle=self.sizeStyle)

        self.setUpBaseWindowBehavior()
        addObserver(self, "draw", "drawBackground")
        UpdateCurrentGlyphView()
        self.openWindow()

    # -------------
    # dynamic attrs
    # -------------

    @property
    def marginsColor(self):
        r, g, b, a = nscolor2rgb(self.w.marginsColor.get())
        return r, g, b, a

    @property
    def captionFontSize(self):
        return int(self.w.captionFontSize.get())

    # ---------
    # callbacks
    # ---------

    def windowCloseCallback(self, sender):
        super().windowCloseCallback(sender)
        removeObserver(self, 'drawBackground')

    def updateViewCallback(self, sender):
        UpdateCurrentGlyphView()

    # ---------
    # observers
    # ---------

    def draw(self, notification):

        if not self.w.preview.get():
            return

        # get glyph
        glyph = notification["glyph"]
        if glyph is None:
            return

        # get font
        font = glyph.font
        if font is None:
            return

        scale = notification['scale']

        if self.w.drawBox.get():
            self.drawBox(glyph, font, scale)

        if self.w.drawMargins.get():
            self.drawMargins(glyph, font, scale)

    def drawMargins(self, glyph, font, scale):

        L, B, R, T = glyph.bounds
        rightWidth = glyph.width - R
        yMin   = font.info.descender
        yMax   = font.info.unitsPerEm
        xMiddle = L + ((R - L) / 2)
        yMiddle = font.info.xHeight / 2 

        w, h = self.captionFontSize * scale * 3, 20 * scale
        m = 12
        xLeft  = -m -w
        xRight = glyph.width + m
        if glyph.leftMargin < 0:
            xLeft -= abs(glyph.leftMargin) # - m

        ctx.save()
        ctx.stroke(None)

        # draw margins
        ctx.fill(*self.marginsColor)
        ctx.rect(0, yMin, L, yMax)
        ctx.rect(R, yMin, rightWidth, yMax)

        # draw captions
        ctx.fill(*self.marginsColor[:-1])
        ctx.fontSize(self.captionFontSize * scale)
        ctx.textBox(str(int(glyph.leftMargin)), (xLeft, yMiddle, w, h), align='right')
        ctx.textBox(str(int(glyph.rightMargin)), (xRight, yMiddle, w, h))

        ctx.restore()

    def drawBox(self, glyph, font, scale):

        # get box top/bottom
        descender = font.info.descender
        upm = font.info.unitsPerEm

        ctx.save()

        # use italic angle
        if self.useItalicAngle:
            angle = font.info.italicAngle
            if angle is not None:
                ctx.skew(-angle, 0)

        # use slant offset
        slantOffset = font.lib.get("com.typemytype.robofont.italicSlantOffset", 0)

        # draw top/bottom boxes
        ctx.fill(*self.glyphViewColor)
        ctx.rect(slantOffset, descender, glyph.width, -self.glyphViewHeight)
        ctx.rect(slantOffset, descender + upm, glyph.width, self.glyphViewHeight)

        ctx.restore()

        # done
        UpdateCurrentGlyphView()


# # open tool
# DrawBox()