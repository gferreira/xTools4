# menuTitle : layers

from importlib import reload
import xTools4.dialogs.glyphs.modifiersLayers
reload(xTools4.dialogs.glyphs.modifiersLayers)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.modifiersLayers import SelectLayersDialog

OpenWindow(SelectLayersDialog)
