# menuTitle : skew

from importlib import reload
import hTools4.dialogs.glyphs.skew
reload(hTools4.dialogs.glyphs.skew)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.skew import SkewGlyphsDialog

OpenWindow(SkewGlyphsDialog)
