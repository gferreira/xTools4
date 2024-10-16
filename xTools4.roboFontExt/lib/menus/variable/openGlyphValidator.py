# menuTitle: GlyphValidator

from importlib import reload
import xTools4.dialogs.variable.GlyphValidator
reload(xTools4.dialogs.variable.GlyphValidator)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphValidator import GlyphValidatorController

OpenWindow(GlyphValidatorController)
