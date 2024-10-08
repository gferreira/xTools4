# menuTitle : print list

from importlib import reload
import xTools4.dialogs.glyphs.namesPrint
reload(xTools4.dialogs.glyphs.namesPrint)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.namesPrint import PrintGlyphNamesDialog

OpenWindow(PrintGlyphNamesDialog)
