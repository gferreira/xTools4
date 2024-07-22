# menuTitle: export layers

from importlib import reload
import hTools4.dialogs.font.exportLayers 
reload(hTools4.dialogs.font.exportLayers)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.font.exportLayers import ExportLayersDialog

OpenWindow(ExportLayersDialog)
