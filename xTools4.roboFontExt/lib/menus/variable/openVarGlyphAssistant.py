# menuTitle: VarGlyphAssistant

from importlib import reload
import xTools4.dialogs.variable.VarGlyphAssistant
reload(xTools4.dialogs.variable.VarGlyphAssistant)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.VarGlyphAssistant import VarGlyphAssistantController

OpenWindow(VarGlyphAssistantController)
