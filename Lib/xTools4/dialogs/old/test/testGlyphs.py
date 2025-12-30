# import xTools4.dialogs.glyphs
# for obj in dir(xTools4.dialogs.glyphs):
#     if not obj.startswith('_'):
#         moduleName = 'xTools4.dialogs.glyphs.%s\n' % obj
#         code  = 'import %s\n' % moduleName
#         code += 'for D in dir(%s):\n' % moduleName
#         code += '\tif D.endswith("Dialog") and D is not "hDialog":\n'
#         code += '\t\tprint(%s, D)\n' % moduleName
#         # code += '\t\tdialog = D()\n'
#         # code += '\t\tprint(dialog, dialog.title)\n'
#         exec(code)

from xTools4.dialogs import hDialog
from vanilla import SquareButton, List

class testAllGlyphsDialogs(hDialog):

    title = 'test glyphs'

    dialogs = {
        # TODO: build list of dialogs auomatically
        # title                  # module                 # dialog
        'create anchors'      : ('anchorsCreate',         'CreateAnchorsDialog'),
        'interpolate'         : ('interpolation',         'InterpolateGlyphsDialog'),
        'condense'            : ('interpolationCondense', 'CondenseGlyphsDialog'),
        'interpolate in font' : ('interpolationInFont',   'InterpolateGlyphsInFontDialog'),
        'copy margins'        : ('marginsCopy',           'CopyMarginsDialog'),
        'set margins'         : ('marginsSet',            'SetMarginsDialog'),
        'copy width'          : ('widthCopy',             'CopyWidthDialog'),
        'set width'           : ('widthSet',              'SetWidthDialog'),
        'move'                : ('move',                  'MoveGlyphsDialog'),
        'gridfit'             : ('gridfit',               'RoundToGridDialog'),
        'scale'               : ('scale',                 'ScaleGlyphsDialog'),
        'skew'                : ('skew',                  'SkewGlyphsDialog'),
        'mask'                : ('layersMask',            'MaskDialog'),
        'mark color'          : ('markSelect',            'MarkGlyphsDialog'),
        'copy layers'         : ('layersCopy',            'CopyToLayerDialog'),
        'outline'             : ('outline',               'OutlineGlyphsDialog'),
        'shift points'        : ('pointsShift ',          'ShiftPointsDialog'),
    }
    verbose = True
    windowType = 0

    def __init__(self):
        self.height  = 400
        self.w = self.window(
                (self.width * 2, self.height),
                self.title,
                minSize=(self.width, self.width * 2))

        x = y = p = self.padding
        self.w.dialogs = List(
                (x, y, -p, -self.buttonHeight - p * 2),
                sorted(self.dialogs.keys()),
                doubleClickCallback=self.openDialogCallback)

        y = -self.buttonHeight - p
        self.w.openAllDialogs = SquareButton(
                (x, y, -p, self.buttonHeight),
                'open all',
                sizeStyle=self.sizeStyle,
                callback=self.openAllDialogsCallback)

        self.w.open()

    def openDialog(self, dialogTitle):
        moduleName, dialogName = self.dialogs[dialogTitle]
        code  = 'import xTools4.dialogs.glyphs.%s\n' % moduleName
        code += 'reload(xTools4.dialogs.glyphs.%s)\n' % moduleName
        code += 'from xTools4.dialogs.glyphs.%s import %s as _%s\n' % (moduleName, dialogName, dialogName)
        if self.verbose:
            code += 'D = _%s()\n' % dialogName
            code += 'print(D)'
        exec(code)

    def openDialogCallback(self, sender):
        selection = sender.getSelection()[0]
        dialogTitle = sender.get()[selection]
        self.openDialog(dialogTitle)

    def openAllDialogsCallback(self, sender):
        for dialogTitle in self.dialogs.keys():
            self.openDialog(dialogTitle)

if __name__ == "__main__":

    testAllGlyphsDialogs()
