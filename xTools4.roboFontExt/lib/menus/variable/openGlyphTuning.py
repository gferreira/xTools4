# menuTitle: GlyphTuning

from importlib import reload
import xTools4.dialogs.variable.GlyphTuning
reload(xTools4.dialogs.variable.GlyphTuning)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphTuning import GlyphTuningController

OpenWindow(GlyphTuningController)
