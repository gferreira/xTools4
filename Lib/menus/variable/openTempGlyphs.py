# menuTitle: TempGlyphs

from importlib import reload
import variableValues.dialogs.TempGlyphs
reload(variableValues.dialogs.TempGlyphs)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.TempGlyphs import TempGlyphs

OpenWindow(TempGlyphs)
