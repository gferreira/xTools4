# menuTitle : interpolate

from importlib import reload
import xTools4.dialogs.glyphs.interpolationMasters
reload(xTools4.dialogs.glyphs.interpolationMasters)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.interpolationMasters import InterpolateGlyphsDialog

OpenWindow(InterpolateGlyphsDialog)
