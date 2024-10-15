# menuTitle : layers

from importlib import reload
import xTools4.dialogs.glyphs.old.modifiersLayers
reload(xTools4.dialogs.glyphs.old.modifiersLayers)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.modifiersLayers import SelectLayersDialog

OpenWindow(SelectLayersDialog)
