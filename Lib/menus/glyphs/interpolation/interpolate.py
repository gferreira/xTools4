# menuTitle : interpolate

from importlib import reload
import hTools4.dialogs.glyphs.interpolationMasters
reload(hTools4.dialogs.glyphs.interpolationMasters)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.interpolationMasters import InterpolateGlyphsDialog

OpenWindow(InterpolateGlyphsDialog)
