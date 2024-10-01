# menuTitle : set width

from importlib import reload
import xTools4.dialogs.glyphs.widthSet
reload(xTools4.dialogs.glyphs.widthSet)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.widthSet import SetWidthDialog

OpenWindow(SetWidthDialog)
