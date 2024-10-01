# menuTitle : mask

from importlib import reload
import xTools4.dialogs.glyphs.layersMask
reload(xTools4.dialogs.glyphs.layersMask)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.layersMask import MaskDialog

OpenWindow(MaskDialog)
