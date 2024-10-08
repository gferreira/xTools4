# menuTitle: VarGlyphViewer

from importlib import reload
import xTools4.dialogs.variable.VarGlyphViewer
reload(xTools4.dialogs.variable.VarGlyphViewer)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.VarGlyphViewer import VarGlyphViewer

OpenWindow(VarGlyphViewer)
