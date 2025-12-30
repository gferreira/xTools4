import os
import json
from vanilla import Button, CheckBox, Group
from mojo.UI import AccordionView, PutFile, GetFile, CodeEditor
from xTools4.dialogs.batch.base import BatchDialogBase


KEY = f'{BatchDialogBase.key}.style'


def getStyleMapStyle(isBold, isItalic):
    if isBold and isItalic:
        return 'bold italic'
    elif isBold and not isItalic:
        return 'bold'
    elif not isBold and isItalic:
        return 'italic'
    else:
        return 'regular'

def buildStyleDataDict(ufos, styleData):

    styleDataDict = {}

    for ufoPath in ufos:

        ufoName = os.path.split(ufoPath)[-1]
        styleDataDict[ufoName] = {}

        # features

        fontFeatures = []

        if styleData.get('features'):
            fontFeatures.extend(styleData['features'])

        if styleData.get(ufoName) and styleData[ufoName].get('features'):
            fontFeatures.extend(styleData[ufoName]['features'])

        if styleData.get('featuresDir'):
            folder = styleData['featuresDir']
            fontFeatures = [os.path.join(folder, f) for f in fontFeatures]

        styleDataDict[ufoName]['features'] = fontFeatures

        # blue zones

        fontBlueZones = []

        if styleData.get('blue zones'):
            fontBlueZones.extend(styleData.get('blue zones'))

        if styleData.get(ufoName) and styleData[ufoName].get('blue zones'):
            fontBlueZones.extend(styleData[ufoName].get('blue zones'))

        fontBlueZones.sort()
        styleDataDict[ufoName]['postscriptBlueValues'] = fontBlueZones

        # stems vertical horizontal

        if styleData[ufoName].get('stems vertical'):
            stemsVertical = styleData[ufoName].get('stems vertical')
        else:
            stemsVertical = []

        if styleData[ufoName].get('stems horizontal'):
            stemsHorizontal = styleData[ufoName].get('stems horizontal')
        else:
            stemsHorizontal = []

        styleDataDict[ufoName]['postscriptStemSnapV'] = stemsVertical
        styleDataDict[ufoName]['postscriptStemSnapH'] = stemsHorizontal

        # OS/2 weight width

        weight = styleData.get('weight')
        width = styleData.get('width')

        if styleData.get(ufoName):
            if styleData[ufoName].get('weight'):
                weight = styleData[ufoName].get('weight')
            if styleData[ufoName].get('width'):
                width = styleData[ufoName].get('width')

        styleDataDict[ufoName]['openTypeOS2WeightClass'] = weight
        styleDataDict[ufoName]['openTypeOS2WidthClass'] = width

        # bold italic

        bold = styleData.get('bold')
        italic = styleData.get('italic')

        if styleData.get(ufoName):
            if styleData[ufoName].get('bold'):
                bold = styleData[ufoName].get('bold')
            if styleData[ufoName].get('italic'):
                italic = styleData[ufoName].get('italic')

        styleDataDict[ufoName]['styleMapStyleName'] = getStyleMapStyle(bold, italic)

    return styleDataDict


class BatchSetStyleDataDialog(BatchDialogBase):

    title = 'batch style'
    key = KEY

    def __init__(self):
        self.height = 400
        self.w = self.window(
                (self.width * 3, self.height),
                self.title,
                minSize=(self.width * 2, self.height))

        # build groups

        self.initFontSelectorGroup()
        self.initStyleDataSelector()

        # build accordion

        descriptions = [
            dict(label="fonts",
                view=self.fontSelector,
                size=self.fontSelectorHeight,
                collapsed=False,
                canResize=True),
            dict(label="style data",
                view=self.styleDataSelector,
                size=self.styleDataSelectorHeight,
                collapsed=True,
                canResize=True),
        ]
        self.w.accordionView = AccordionView((0, 0, -0, -0), descriptions)

        # setup window

        self.initBatchWindowBehaviour()
        self.openWindow()

    # ------------
    # initializers
    # ------------

    def initStyleDataSelector(self):

        self.styleDataSelector = Group((0, 0, -0, -0))

        x = y = p = self.padding

        self.styleDataSelector.importData = Button(
                (x, y, -p, self.textHeight),
                "import style data…",
                callback=self.importStyleDataCallback,
                sizeStyle=self.sizeStyle)

        y += self.textHeight + p
        textBoxHeight = -self.textHeight - p * 3 - self.textHeight
        self.styleDataSelector.codeEditor = CodeEditor(
                (x, y, -p, textBoxHeight),
                '',
                showLineNumbers=False)

        y = -(self.textHeight + p) * 2
        self.styleDataSelector.applyButton = Button(
                (x, y, -p, self.textHeight),
                "set data",
                callback=self.batchSetStyleDataCallback,
                sizeStyle=self.sizeStyle)

        y = -self.textHeight - p
        self.styleDataSelector.preflight = CheckBox(
                (x, y, -p, self.textHeight),
                "preflight",
                sizeStyle=self.sizeStyle)

        self.styleDataSelectorHeight = 280

    # -------------
    # dynamic attrs
    # -------------

    @property
    def styleData(self):
        styleDataSrc  = json.loads(self.styleDataSelector.codeEditor.get())
        styleDataDict = buildStyleDataDict(self.targetFontPaths, styleDataSrc)
        return styleDataDict

    # ---------
    # callbacks
    # ---------

    def importStyleDataCallback(self, sender):
        msg = 'import style data from .json file'
        filePath = GetFile(message=msg, title=self.title, fileTypes=['json'])
        if not filePath:
            print('no .json file selected.\n')
            return
        self.importStyleData(filePath)

    def batchSetStyleDataCallback(self, sender):
        if self.styleDataSelector.preflight.get():
            self.preflight()
        else:
            self.batchSetStyleData()

    # -------
    # methods
    # -------

    def importStyleData(self, filePath):
        print('importing style data from file…')
        # read data from file
        with open(filePath, 'r', encoding='utf-8') as inputFile:
            styleData = inputFile.read()
        # update UI
        self.styleDataSelector.codeEditor.set(styleData)
        # done
        print('…done.\n')

    def preflightStyleData(self):
        styleData = self.styleData
        print('style data:\n')
        for ufoPath in self.targetFontPaths:
            ufoName = os.path.split(ufoPath)[-1]
            print(ufoName)
            print('- features: %s'               % styleData[ufoName]['features'])
            print('- openTypeOS2WeightClass: %s' % styleData[ufoName]['openTypeOS2WeightClass'])
            print('- openTypeOS2WidthClass: %s'  % styleData[ufoName]['openTypeOS2WidthClass'])
            print('- styleMapStyleName: %s'      % styleData[ufoName]['styleMapStyleName'])
            print('- postscriptBlueValues: %s'   % styleData[ufoName]['postscriptBlueValues'])
            print('- postscriptStemSnapV: %s'    % styleData[ufoName]['postscriptStemSnapV'])
            print('- postscriptStemSnapH: %s'    % styleData[ufoName]['postscriptStemSnapH'])
            print()

    def preflight(self):
        self.preflightTargetFonts()
        self.preflightStyleData()

    def batchSetStyleData(self):

        # -----------------
        # assert conditions
        # -----------------

        # no target fonts selected
        targetFonts = self.targetFonts
        if not len(targetFonts):
            print('no target fonts selected.\n')
            return

        # get style data
        styleData = self.styleData
        if not len(styleData):
            print('no style data.\n')
            return

        # --------------------
        # batch set style data
        # --------------------

        print('batch setting style data...\n')

        for targetFontName, targetFont in targetFonts:

            print('\tsetting style data in %s...\n' % targetFontName)
            ufoName = os.path.split(targetFont.path)[-1]

            # set features
            print('\t\tsetting features...')
            featuresText = ''
            for fea in styleData[ufoName]['features']:
                featuresText += 'include(%s);\n' % fea
            targetFont.features.text = featuresText

            # set font info
            attrs = [
                'openTypeOS2WeightClass',
                'openTypeOS2WidthClass',
                'styleMapStyleName',
                'postscriptBlueValues',
                'postscriptStemSnapV',
                'postscriptStemSnapH',
            ]
            for attr in attrs:
                print('\t\tsetting %s...' % attr)
                setattr(targetFont.info, attr, styleData[ufoName][attr])

            # save fonts without UI
            if not targetFont.hasInterface():
                print()
                print('\tsaving %s...' % targetFontName)
                targetFont.save()
                targetFont.close()
            else:
                targetFont.changed()

            # done with font
            print()

        # done
        print('...done.\n')

# -------
# testing
# -------

if __name__ == '__main__':

    BatchSetStyleDataDialog()
