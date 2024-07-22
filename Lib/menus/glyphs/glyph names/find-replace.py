# menuTitle : find & replace

from importlib import reload
import hTools4.dialogs.glyphs.namesFindReplace
reload(hTools4.dialogs.glyphs.namesFindReplace)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.namesFindReplace import FindReplaceGlyphNamesDialog

OpenWindow(FindReplaceGlyphNamesDialog)
