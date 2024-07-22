# menuTitle : mask

from importlib import reload
import hTools4.dialogs.glyphs.layersMask
reload(hTools4.dialogs.glyphs.layersMask)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.layersMask import MaskDialog

OpenWindow(MaskDialog)
