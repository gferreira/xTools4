# menuTitle: VarFontAssistant

from importlib import reload
import xTools4.dialogs.variable.VarFontAssistant
reload(xTools4.dialogs.variable.VarFontAssistant)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.VarFontAssistant import VarFontAssistant_EZUI

OpenWindow(VarFontAssistant_EZUI)
