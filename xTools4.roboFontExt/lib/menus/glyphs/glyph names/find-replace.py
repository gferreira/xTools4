# menuTitle : find & replace

from importlib import reload
import xTools4.dialogs.glyphs.namesFindReplace
reload(xTools4.dialogs.glyphs.namesFindReplace)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.namesFindReplace import FindReplaceGlyphNamesDialog

OpenWindow(FindReplaceGlyphNamesDialog)
