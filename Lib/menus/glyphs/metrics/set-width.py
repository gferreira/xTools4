# menuTitle : set width

from importlib import reload
import hTools4.dialogs.glyphs.widthSet
reload(hTools4.dialogs.glyphs.widthSet)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.widthSet import SetWidthDialog

OpenWindow(SetWidthDialog)
