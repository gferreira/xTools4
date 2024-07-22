# menuTitle: set glyph order

from importlib import reload
import hTools4.dialogs.font.setGlyphOrder 
reload(hTools4.dialogs.font.setGlyphOrder)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.font.setGlyphOrder import SetGlyphOrderDialog

OpenWindow(SetGlyphOrderDialog)

