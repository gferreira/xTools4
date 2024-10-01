# menuTitle: GlyphSetProofer

from importlib import reload
import variableValues.dialogs.GlyphSetProofer
reload(variableValues.dialogs.GlyphSetProofer)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.GlyphSetProofer import GlyphSetProoferUI

OpenWindow(GlyphSetProoferUI)
