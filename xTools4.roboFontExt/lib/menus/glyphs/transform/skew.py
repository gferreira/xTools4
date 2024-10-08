# menuTitle : skew

from importlib import reload
import xTools4.dialogs.glyphs.skew
reload(xTools4.dialogs.glyphs.skew)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.skew import SkewGlyphsDialog

OpenWindow(SkewGlyphsDialog)
