# menuTitle: RoundingEdit

from importlib import reload
import xTools4.dialogs.variable.RoundingTool
reload(xTools4.dialogs.variable.RoundingTool)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.RoundingTool import RoundingController

OpenWindow(RoundingController)
