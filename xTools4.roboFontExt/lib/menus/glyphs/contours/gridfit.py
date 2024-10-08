# menuTitle : gridfit

from importlib import reload
import xTools4.dialogs.glyphs.gridfit
reload(xTools4.dialogs.glyphs.gridfit)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.gridfit import RoundToGridDialog

OpenWindow(RoundToGridDialog)
