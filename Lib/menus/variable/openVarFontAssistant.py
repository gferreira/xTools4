# menuTitle: VarFontAssistant

from importlib import reload
import variableValues.dialogs.RF4.VarFontAssistant
reload(variableValues.dialogs.RF4.VarFontAssistant)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.RF4.VarFontAssistant import VarFontAssistant_EZUI

OpenWindow(VarFontAssistant_EZUI)
