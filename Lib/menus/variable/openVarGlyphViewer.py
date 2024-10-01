# menuTitle: VarGlyphViewer

from importlib import reload
import variableValues.dialogs.RF4.VarGlyphViewer
reload(variableValues.dialogs.RF4.VarGlyphViewer)

from mojo.roboFont import OpenWindow
from variableValues.dialogs.RF4.VarGlyphViewer import VarGlyphViewer

OpenWindow(VarGlyphViewer)
