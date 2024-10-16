# menuTitle: TempEdit

from importlib import reload
import xTools4.dialogs.variable.TempEdit 
reload(xTools4.dialogs.variable.TempEdit)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.TempEdit import TempEdit

OpenWindow(TempEdit)
