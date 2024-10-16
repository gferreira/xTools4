# menuTitle: GlyphSetProofer

from importlib import reload
import xTools4.dialogs.variable.GlyphSetProofer
reload(xTools4.dialogs.variable.GlyphSetProofer)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphSetProofer import GlyphSetProoferUI

OpenWindow(GlyphSetProoferUI)
