# menuTitle: Measurements

from importlib import reload
import variableValues.dialogs.RF4.Measurements
reload(variableValues.dialogs.RF4.Measurements)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.RF4.Measurements import MeasurementsController

OpenWindow(MeasurementsController)
