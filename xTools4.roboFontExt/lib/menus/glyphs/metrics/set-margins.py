# menuTitle : set margins

from importlib import reload
import xTools4.dialogs.glyphs.marginsSet
reload(xTools4.dialogs.glyphs.marginsSet)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.marginsSet import SetMarginsDialog

OpenWindow(SetMarginsDialog)
