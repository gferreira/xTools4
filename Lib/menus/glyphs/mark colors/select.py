# menuTitle : mark & select

from importlib import reload
import hTools4.dialogs.glyphs.markSelect
reload(hTools4.dialogs.glyphs.markSelect)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.markSelect import MarkGlyphsDialog

OpenWindow(MarkGlyphsDialog)
