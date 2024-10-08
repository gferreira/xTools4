# menuTitle: Measurements

from importlib import reload
import xTools4.dialogs.variable.Measurements
reload(xTools4.dialogs.variable.Measurements)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.Measurements import MeasurementsController

OpenWindow(MeasurementsController)
