# menuTitle: VarFontAssistant

from importlib import reload
import xTools4.dialogs.variable.old.VarFontAssistant
reload(xTools4.dialogs.variable.old.VarFontAssistant)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.old.VarFontAssistant import VarFontAssistant

OpenWindow(VarFontAssistant)
