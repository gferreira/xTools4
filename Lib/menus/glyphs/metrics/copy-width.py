# menuTitle : copy width

from importlib import reload
import hTools4.dialogs.glyphs.widthCopy
reload(hTools4.dialogs.glyphs.widthCopy)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.widthCopy import CopyWidthDialog

OpenWindow(CopyWidthDialog)
