# menuTitle: GlyphGauge

from importlib import reload
import xTools4.dialogs.variable.GlyphGauge
reload(xTools4.dialogs.variable.GlyphGauge)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphGauge import GlyphGauge_EZUI

OpenWindow(GlyphGauge_EZUI)
