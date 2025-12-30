from vanilla import CheckBox, Button, ColorWell
from mojo.roboFont import CurrentFont
from xTools4.dialogs.old import hDialog
from xTools4.modules.color import rgb2nscolor, nscolor2rgb
from xTools4.modules.fontutils import markGlyphs, findMarkColor


KEY = f'{hDialog.key}.font.markTypes'


def markGlyphType(g, colorsDict):
    # contours only
    if len(g.contours) and not len(g.components):
        g.markColor = colorsDict['contours']
    # components only
    elif not len(g.contours) and len(g.components):
        g.markColor = colorsDict['components']
    # contours and components
    elif len(g.contours) and len(g.components):
        g.markColor = colorsDict['contoursComponents']
    # empty
    else:
        g.markColor = colorsDict['empty']


class MarkGlyphTypesDialog(hDialog):

    title = 'mark'
    key   = KEY

    settings = {
        'contours'           : (0, 1, 0, 0.5), # green
        'components'         : (0, 0, 1, 0.5), # blue
        'contoursComponents' : (1, 0, 0, 0.5), # red
        'empty'              : (1, 1, 0, 0.5), # yellow
    }

    def __init__(self):
        self.height  = self.buttonHeight * 4
        self.height += self.textHeight * 5
        self.height += self.padding * 8
        self.w = self.window((self.width, self.height), self.title)

        x = y = p = self.padding
        self.w.labelContours = CheckBox(
                (x, y, -p, self.textHeight),
                'contours',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorContours = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.settings['contours']))

        y += self.buttonHeight + self.padding
        self.w.labelComponents = CheckBox(
                (x, y, -p, self.textHeight),
                'components',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorComponents = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.settings['components']))

        y += self.buttonHeight + self.padding
        self.w.labelContoursComponents = CheckBox(
                (x, y, -p, self.textHeight),
                'mixed',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorContoursComponents = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.settings['contoursComponents']))

        y += self.buttonHeight + self.padding
        self.w.labelEmpty = CheckBox(
                (x, y, -self.padding, self.textHeight),
                'empty',
                value=True,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p * .5
        self.w.colorEmpty = ColorWell(
                (x, y, -p, self.buttonHeight),
                color=rgb2nscolor(self.settings['empty']))

        y += self.buttonHeight + self.padding
        self.w.applyButton = Button(
                (x, y, -p, self.textHeight),
                "apply",
                callback=self.markGlyphsCallback,
                sizeStyle=self.sizeStyle)

        self.w.workspaceWindowIdentifier = KEY

        self.openWindow()

    def markGlyphsCallback(self, sender):

        font = self.getCurrentFont()
        if not font:
            return

        colorsDict = {
            'contours'           : nscolor2rgb(self.w.colorContours.get()),
            'components'         : nscolor2rgb(self.w.colorComponents.get()),
            'contoursComponents' : nscolor2rgb(self.w.colorContoursComponents.get()),
            'empty'              : nscolor2rgb(self.w.colorEmpty.get()),
        }

        print('marking glyph types in font %s %s...' % (font.info.familyName, font.info.styleName))

        ## TODO: add support for layers

        for g in font:
            markGlyphType(g, colorsDict)

        print('...done.\n')


if __name__ == '__main__':

    MarkGlyphTypesDialog()
