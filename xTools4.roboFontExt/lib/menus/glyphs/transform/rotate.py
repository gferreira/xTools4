# menuTitle : rotate

from importlib import reload
import xTools4.dialogs.glyphs.rotate
reload(xTools4.dialogs.glyphs.rotate)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.rotate import RotateGlyphsDialog

OpenWindow(RotateGlyphsDialog)
