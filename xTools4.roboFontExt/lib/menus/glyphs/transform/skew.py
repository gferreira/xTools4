# menuTitle : skew

from importlib import reload
import xTools4.dialogs.glyphs.old.skew
reload(xTools4.dialogs.glyphs.old.skew)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.skew import SkewGlyphsDialog

OpenWindow(SkewGlyphsDialog)
