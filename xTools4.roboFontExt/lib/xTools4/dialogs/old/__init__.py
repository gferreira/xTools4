import os
from AppKit import NSApp # NSWindow, NSWindowMiniaturizeButton, NSWindowZoomButton
from vanilla import FloatingWindow, HUDFloatingWindow, Window
from mojo.roboFont import CurrentGlyph, CurrentFont, AllFonts
from mojo.UI import PostBannerNotification, CurrentWindow
from mojo.extensions import getExtensionDefault, getExtensionDefaultColor, setExtensionDefault, setExtensionDefaultColor
from xTools4.modules.fontutils import getGlyphs2
from xTools4.modules.messages import *
from xTools4.modules.color import rgb2nscolor, nscolor2rgb


def getLayerNames():
    '''
    Get the current layer selection in the :doc:`glyphs/modifiersLayers` panel.
    
    If the :doc:`glyphs/modifiersLayers` panel is not open:
    
    - if the *Glyph Editor* is the main window, the current layer is returned
    - if the *Font Overview* is the main window, the default layer is returned

    Returns:
        A list of selected layer names.

    :: 

        >>> from xTools4.dialogs import getLayerNames
        >>> getLayerNames()
        ['foreground', 'background']

    '''
    app = NSApp()
    layers = []
    selection = []
    for window in app.windows():
        if window.title() == 'layers':
            delegate = window.delegate()
            if hasattr(delegate, "vanillaWrapper"):
                vanillaWrapper = delegate.vanillaWrapper
                layers.extend(vanillaWrapper.w.list.get())
                selection.extend(vanillaWrapper.w.list.getSelection())

    if not selection:
        currentWindow = CurrentWindow()
        if currentWindow is None:
            return []
        if currentWindow.doodleWindowName == 'GlyphWindow':
            return [CurrentGlyph().layer.name]
        else:
            return [CurrentFont().defaultLayer.name]
    else:
        return [layer for i, layer in enumerate(layers) if i in selection]


class hDialogBase:
    '''A base object with dimensions and settings for all xTools4 dialogs.'''
    pass


class hDialog:

    '''
    A base object which provides generic attributes and functionality for all xTools4 dialogs.

    '''

    key      = 'com.hipertipo.xTools4.dialogs'
    prefsKey = 'com.hipertipo.xTools4.preferences'
    prefsDefaults = {
        'previewFillColor'    : (0, 1, 0, 0.35),
        'previewStrokeColor'  : (0, 1, 0),
        'previewStrokeWidth'  : 2,
        'previewOriginRadius' : 10,
        'verbose'             : True,
    }

    # settings = {}
    # settingsSave = False
    # verbose  = True
    # readOnly = False

    #: Default space between UI elements in dialogs.
    padding = 10

    #: Default size of text elements.
    sizeStyle = 'small'
    
    #: Height of text elements (labels, input fields, buttons, etc).
    textHeight = 20
    
    #: Height of text input fields. 
    textInput = 18  ### deprecated ??

    #: Height of progress bars. 
    progressBar = 6

    #: Default width of palette dialogs.
    width = 123

    #: *deprecated*
    buttonHeight  = 25

    #: *deprecated*
    buttonNudge   = 18

    #: *deprecated*
    buttonSquare  = 35

    #: *deprecated*
    stepperHeight = 22

    #: The mode of the output messages.
    #: 
    #: - ``0``: print
    #: - ``1``: notification
    messageMode = 1

    #: The type of the window.
    #: 
    #: - ``0``: FloatingWindow
    #: - ``1``: HUDFloatingWindow
    #: - ``2``: Window.
    windowType = 0

    #: A list of available base classes for subclassing windows.
    windowTypes = [FloatingWindow, HUDFloatingWindow, Window]

    # -------------
    # dynamic attrs
    # -------------

    @property
    def spinnerHeight(self):
        '''*deprecated*'''
        return self.buttonNudge * 2 + self.padding

    @property
    def spinnerSliderHeight(self):
        '''*deprecated*'''
        return self.stepperHeight + self.textHeight + self.padding * 0.5

    @property
    def arrowsHeight(self):
        return self.width

    # preview fill color

    @property
    def previewFillColorKey(self):
        return '%s.previewFillColor' % self.prefsKey

    @property
    def previewFillColor(self):
        '''The fill color of Glyph Editor previews.'''
        color = getExtensionDefaultColor(self.previewFillColorKey, fallback=self.prefsDefaults['previewFillColor'])
        if type(color) is not tuple:
            color = nscolor2rgb(color)
        return color

    @previewFillColor.setter
    def previewFillColor(self, color):
        if type(color) is tuple:
            color = rgbsToNSColor(color)
        setExtensionDefaultColor(self.previewFillColorKey, color)

    # preview stroke color

    @property
    def previewStrokeColorKey(self):
        return '%s.previewStrokeColor' % self.prefsKey

    @property
    def previewStrokeColor(self):
        '''The stroke color of Glyph Editor previews.'''
        color = getExtensionDefaultColor(self.previewStrokeColorKey, fallback=self.prefsDefaults['previewStrokeColor'])
        if type(color) is not tuple:
            color = nscolor2rgb(color)
        return color

    @previewStrokeColor.setter
    def previewStrokeColor(self, color):
        if type(color) is tuple:
            color = rgb2nscolor(color)
        setExtensionDefaultColor(self.previewStrokeColorKey, color)

    # preview stroke width

    @property
    def previewStrokeWidthKey(self):
        return '%s.previewStrokeWidth' % self.prefsKey

    @property
    def previewStrokeWidth(self):
        '''The stroke width of Glyph Editor previews.'''
        return getExtensionDefault(self.previewStrokeWidthKey, fallback=self.prefsDefaults['previewStrokeWidth'])

    @previewStrokeWidth.setter
    def previewStrokeWidth(self, value):
        setExtensionDefault(self.previewStrokeWidthKey, value)

    # preview origin radius

    @property
    def previewOriginRadiusKey(self):
        return '%s.previewOriginRadius' % self.prefsKey

    @property
    def previewOriginRadius(self):
        '''The radius of origin points in Glyph Editor previews.'''
        return getExtensionDefault(self.previewOriginRadiusKey, fallback=self.prefsDefaults['previewOriginRadius'])

    @previewOriginRadius.setter
    def previewOriginRadius(self, value):
        setExtensionDefault(self.previewOriginRadiusKey, value)

    # verbose mode

    @property
    def verboseKey(self):
        return '%s.verbose' % self.prefsKey

    @property
    def verbose(self):
        '''Toggle output messages.'''
        return getExtensionDefault(self.verboseKey, fallback=self.prefsDefaults['verbose'])

    @verbose.setter
    def verbose(self, value):
        setExtensionDefault(self.verboseKey, value)

    @property
    def window(self):
        '''
        Return the vanilla window object for the dialog.

        '''
        w = self.windowTypes[self.windowType]
        # if self.windowType == 0:
        #     w.getNSWindow().setTitlebarAppearsTransparent_(True)
        #     # w.getNSWindow().standardWindowButton_(NSWindowMiniaturizeButton).setHidden_(True)
        #     # w.getNSWindow().standardWindowButton_(NSWindowZoomButton).setHidden_(True)
        return w

    # -------
    # methods
    # -------

    def loadSettings(self):
        '''*Not implemented yet.*'''
        print('load_settings')
        # TODO:
        # read extension settings for tool
        # save it as a hSettings object
        # self.settings = hSettings(settingsDict)
        pass

    def saveSettings(self):
        '''*Not implemented yet.*'''
        # TODO:
        print('save_settings')
        pass

    def getCurrentFont(self):
        '''
        Get the current font. Print a message if there is no current font.

        Returns:
            A font object (RFont).

        '''
        font = CurrentFont()
        if not font:
            showMessage(noFontOpen, self.messageMode)
        return font

    def getCurrentGlyph(self):
        '''
        Get the current glyph. Print a message if there is no current glyph.

        Returns:
            A glyph object (RGlyph).

        '''
        glyph = CurrentGlyph()
        if not glyph:
            showMessage(noGlyphOpen, self.messageMode)
        return glyph

    def getLayerNames(self):
        '''
        Get the current layer selection in the 'layers' panel.

        Returns:
            A list of layer names.

        '''
        return getLayerNames()

    def getGlyphNames(self, template=False):
        '''
        Get the current glyph selection in the current font.

        Returns:
            A list of glyph names.

        '''
        font = self.getCurrentFont()

        if not font:
            return

        glyphNames = getGlyphs2(font, template=template)

        if not len(glyphNames):
            showMessage(noGlyphSelected, self.messageMode)

        return glyphNames

    def getAllFonts(self):
        '''
        Get all open fonts. Print a message if no font is open.

        Returns:
            A list of font objects (RFont).

        '''
        allFonts = AllFonts()

        if not len(allFonts):
            showMessage(noFontOpen, self.messageMode)

        return allFonts

    def getFontsFolder(self, folder):
        '''
        Get the paths of all fonts in a folder. Print a message if the folder contains no fonts.

        Returns:
            A list of font objects (RFont).

        '''
        fontPaths = []
        for f in os.listdir(folder):
            if not os.path.splitext(f)[-1] == '.ufo':
                continue
            fontPath = os.path.join(folder, f)
            fontPaths.append(fontPath)

        if not len(fontPaths):
            showMessage(noFontInFolder, self.messageMode)

        return fontPaths

    def openWindow(self):
        '''
        Open the dialog window.
        
        '''
        if not hasattr(self, 'w'):
            return
        if self.windowType == 0:
            self.w.getNSWindow().setTitlebarAppearsTransparent_(True)
            # w.getNSWindow().standardWindowButton_(NSWindowMiniaturizeButton).setHidden_(True)
            # w.getNSWindow().standardWindowButton_(NSWindowZoomButton).setHidden_(True)
        self.w.open()


class hSettings:

    # TODO: implement reading & writing settings

    plistPath = None

    def __init__(self, settingsDict={}):
        for key, value in settingsDict.items():
            setattr(self, key, value)

    def read(self, plistPath):
        # 1. read plist
        # 2. map values to hSettings attributes
        pass

    def write(self, plistPath=None):
        # 1. make a dict of all attributes/values
        # 2. save dict to plist
        pass
