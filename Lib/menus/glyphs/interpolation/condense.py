# menuTitle : condense

from importlib import reload
import xTools4.dialogs.glyphs.old.interpolationCondense
reload(xTools4.dialogs.glyphs.old.interpolationCondense)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.interpolationCondense import CondenseGlyphsDialog

OpenWindow(CondenseGlyphsDialog)
