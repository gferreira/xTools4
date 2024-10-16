# menuTitle : copy width

from importlib import reload
import xTools4.dialogs.glyphs.old.widthCopy
reload(xTools4.dialogs.glyphs.old.widthCopy)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.widthCopy import CopyWidthDialog

OpenWindow(CopyWidthDialog)
