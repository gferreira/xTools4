# menuTitle : layers

from importlib import reload
import hTools4.dialogs.glyphs.modifiersLayers
reload(hTools4.dialogs.glyphs.modifiersLayers)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.modifiersLayers import SelectLayersDialog

OpenWindow(SelectLayersDialog)
