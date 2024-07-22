# menuTitle : print list

from importlib import reload
import hTools4.dialogs.glyphs.namesPrint
reload(hTools4.dialogs.glyphs.namesPrint)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.namesPrint import PrintGlyphNamesDialog

OpenWindow(PrintGlyphNamesDialog)
