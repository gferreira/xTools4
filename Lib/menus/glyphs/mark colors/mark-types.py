# menuTitle : mark glyph types

from importlib import reload
import xTools4.dialogs.glyphs.old.markTypes
reload(xTools4.dialogs.glyphs.old.markTypes)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.markTypes import MarkGlyphTypesDialog

OpenWindow(MarkGlyphTypesDialog)
