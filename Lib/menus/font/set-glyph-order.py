# menuTitle: set glyph order

from importlib import reload
import xTools4.dialogs.font.setGlyphOrder 
reload(xTools4.dialogs.font.setGlyphOrder)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.font.setGlyphOrder import SetGlyphOrderDialog

OpenWindow(SetGlyphOrderDialog)

