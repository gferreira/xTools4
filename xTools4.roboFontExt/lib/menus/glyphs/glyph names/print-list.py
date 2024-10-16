# menuTitle : print list

from importlib import reload
import xTools4.dialogs.glyphs.old.namesPrint
reload(xTools4.dialogs.glyphs.old.namesPrint)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.namesPrint import PrintGlyphNamesDialog

OpenWindow(PrintGlyphNamesDialog)
