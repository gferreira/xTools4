# menuTitle : mark & select

from importlib import reload
import xTools4.dialogs.glyphs.old.markSelect
reload(xTools4.dialogs.glyphs.old.markSelect)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.markSelect import MarkGlyphsDialog

OpenWindow(MarkGlyphsDialog)
