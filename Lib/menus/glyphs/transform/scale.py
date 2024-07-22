# menuTitle : scale

from importlib import reload
import hTools4.dialogs.glyphs.scale
reload(hTools4.dialogs.glyphs.scale)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.scale import ScaleGlyphsDialog

OpenWindow(ScaleGlyphsDialog)
