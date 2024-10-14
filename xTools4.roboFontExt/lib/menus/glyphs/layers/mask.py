# menuTitle : mask

from importlib import reload
import xTools4.dialogs.glyphs.old.layersMask
reload(xTools4.dialogs.glyphs.old.layersMask)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.layersMask import MaskDialog

OpenWindow(MaskDialog)
