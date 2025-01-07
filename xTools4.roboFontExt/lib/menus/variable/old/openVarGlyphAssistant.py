# menuTitle: VarGlyphAssistant

from importlib import reload
import xTools4.dialogs.variable.old.VarGlyphAssistant
reload(xTools4.dialogs.variable.old.VarGlyphAssistant)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.old.VarGlyphAssistant import VarGlyphAssistant

OpenWindow(VarGlyphAssistant)
