# menuTitle : mark & select

from importlib import reload
import xTools4.dialogs.glyphs.markSelect
reload(xTools4.dialogs.glyphs.markSelect)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.markSelect import MarkGlyphsDialog

OpenWindow(MarkGlyphsDialog)
