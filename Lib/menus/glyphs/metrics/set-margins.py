# menuTitle : set margins

from importlib import reload
import hTools4.dialogs.glyphs.marginsSet
reload(hTools4.dialogs.glyphs.marginsSet)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.marginsSet import SetMarginsDialog

OpenWindow(SetMarginsDialog)
