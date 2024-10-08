# menuTitle: ProjectController

from importlib import reload
import variableValues.dialogs.VarProject
reload(variableValues.dialogs.VarProject)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.VarProject import VarProjectController

OpenWindow(VarProjectController)
