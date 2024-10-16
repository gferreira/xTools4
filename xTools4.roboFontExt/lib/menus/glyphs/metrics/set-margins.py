# menuTitle : set margins

from importlib import reload
import xTools4.dialogs.glyphs.old.marginsSet
reload(xTools4.dialogs.glyphs.old.marginsSet)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.marginsSet import SetMarginsDialog

OpenWindow(SetMarginsDialog)
