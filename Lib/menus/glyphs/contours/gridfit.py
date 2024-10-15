# menuTitle : gridfit

from importlib import reload
import xTools4.dialogs.glyphs.old.gridfit
reload(xTools4.dialogs.glyphs.old.gridfit)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.gridfit import RoundToGridDialog

OpenWindow(RoundToGridDialog)
