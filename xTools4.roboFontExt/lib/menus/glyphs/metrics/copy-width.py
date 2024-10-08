# menuTitle : copy width

from importlib import reload
import xTools4.dialogs.glyphs.widthCopy
reload(xTools4.dialogs.glyphs.widthCopy)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.widthCopy import CopyWidthDialog

OpenWindow(CopyWidthDialog)
