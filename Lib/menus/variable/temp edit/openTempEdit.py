# menuTitle: TempEdit

from importlib import reload
import xTools4.dialogs.variable.old.TempEdit 
reload(xTools4.dialogs.variable.old.TempEdit)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.old.TempEdit import TempEdit

OpenWindow(TempEdit)
