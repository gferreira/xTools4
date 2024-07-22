# menuTitle : rotate

from importlib import reload
import hTools4.dialogs.glyphs.rotate
reload(hTools4.dialogs.glyphs.rotate)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.rotate import RotateGlyphsDialog

OpenWindow(RotateGlyphsDialog)
