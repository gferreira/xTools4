# menuTitle : condense

from importlib import reload
import xTools4.dialogs.glyphs.interpolationCondense
reload(xTools4.dialogs.glyphs.interpolationCondense)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.interpolationCondense import CondenseGlyphsDialog

OpenWindow(CondenseGlyphsDialog)
