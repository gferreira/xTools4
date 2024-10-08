# menuTitle: GlyphGauge

from importlib import reload
import variableValues.dialogs.RF4.GlyphGauge
reload(variableValues.dialogs.RF4.GlyphGauge)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.RF4.GlyphGauge import GlyphGauge_EZUI

OpenWindow(GlyphGauge_EZUI)
