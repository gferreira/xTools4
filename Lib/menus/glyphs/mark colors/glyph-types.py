# menuTitle : mark glyph types

from importlib import reload
import hTools4.dialogs.glyphs.markTypes
reload(hTools4.dialogs.glyphs.markTypes)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.markTypes import MarkGlyphTypesDialog

OpenWindow(MarkGlyphTypesDialog)
