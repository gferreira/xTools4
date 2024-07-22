# menuTitle : condense

from importlib import reload
import hTools4.dialogs.glyphs.interpolationCondense
reload(hTools4.dialogs.glyphs.interpolationCondense)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.interpolationCondense import CondenseGlyphsDialog

OpenWindow(CondenseGlyphsDialog)
