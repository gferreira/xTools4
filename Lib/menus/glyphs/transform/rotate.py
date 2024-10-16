# menuTitle : rotate

from importlib import reload
import xTools4.dialogs.glyphs.old.rotate
reload(xTools4.dialogs.glyphs.old.rotate)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.rotate import RotateGlyphsDialog

OpenWindow(RotateGlyphsDialog)
