# menuTitle : set width

from importlib import reload
import xTools4.dialogs.glyphs.old.widthSet
reload(xTools4.dialogs.glyphs.old.widthSet)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.widthSet import SetWidthDialog

OpenWindow(SetWidthDialog)
