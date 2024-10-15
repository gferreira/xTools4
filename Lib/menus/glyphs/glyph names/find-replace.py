# menuTitle : find & replace

from importlib import reload
import xTools4.dialogs.glyphs.old.namesFindReplace
reload(xTools4.dialogs.glyphs.old.namesFindReplace)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.namesFindReplace import FindReplaceGlyphNamesDialog

OpenWindow(FindReplaceGlyphNamesDialog)
