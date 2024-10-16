# menuTitle : interpolate

from importlib import reload
import xTools4.dialogs.glyphs.old.interpolationMasters
reload(xTools4.dialogs.glyphs.old.interpolationMasters)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.interpolationMasters import InterpolateGlyphsDialog

OpenWindow(InterpolateGlyphsDialog)
