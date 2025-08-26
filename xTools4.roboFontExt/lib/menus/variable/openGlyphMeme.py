# menuTitle: GlyphMeme

from importlib import reload
import xTools4.dialogs.variable.GlyphMeme
reload(xTools4.dialogs.variable.GlyphMeme)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphMeme import GlyphMemeController

OpenWindow(GlyphMemeController)
