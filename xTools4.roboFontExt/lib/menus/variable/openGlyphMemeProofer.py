# menuTitle: GlyphMemeProofer

from importlib import reload
import xTools4.dialogs.variable.GlyphMemeProofer
reload(xTools4.dialogs.variable.GlyphMemeProofer)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphMemeProofer import GlyphMemeProoferController

OpenWindow(GlyphMemeProoferController)
