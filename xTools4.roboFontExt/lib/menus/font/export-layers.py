# menuTitle: export layers

from importlib import reload
import xTools4.dialogs.font.exportLayers 
reload(xTools4.dialogs.font.exportLayers)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.font.exportLayers import ExportLayersDialog

OpenWindow(ExportLayersDialog)
