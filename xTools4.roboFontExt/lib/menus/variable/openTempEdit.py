# menuTitle: TempEdit

from importlib import reload
import variableValues.dialogs.TempEdit 
reload(variableValues.dialogs.TempEdit)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.TempEdit import TempEdit

OpenWindow(TempEdit)
