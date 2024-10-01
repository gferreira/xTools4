# menuTitle: GlyphValidator

from importlib import reload
import variableValues.dialogs.RF4.GlyphValidator
reload(variableValues.dialogs.RF4.GlyphValidator)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.RF4.GlyphValidator import GlyphValidatorController

OpenWindow(GlyphValidatorController)
