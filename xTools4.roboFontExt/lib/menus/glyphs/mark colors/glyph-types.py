# menuTitle : mark glyph types

from importlib import reload
import xTools4.dialogs.glyphs.markTypes
reload(xTools4.dialogs.glyphs.markTypes)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.markTypes import MarkGlyphTypesDialog

OpenWindow(MarkGlyphTypesDialog)
