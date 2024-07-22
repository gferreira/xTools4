# menuTitle : gridfit

from importlib import reload
import hTools4.dialogs.glyphs.gridfit
reload(hTools4.dialogs.glyphs.gridfit)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.gridfit import RoundToGridDialog

OpenWindow(RoundToGridDialog)
