# menuTitle : scale

from importlib import reload
import xTools4.dialogs.glyphs.old.scale
reload(xTools4.dialogs.glyphs.old.scale)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.scale import ScaleGlyphsDialog

OpenWindow(ScaleGlyphsDialog)
