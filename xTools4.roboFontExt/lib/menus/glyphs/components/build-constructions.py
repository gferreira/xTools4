# menuTitle : build constructions

from importlib import reload
import xTools4.dialogs.glyphs.buildConstructions
reload(xTools4.dialogs.glyphs.buildConstructions)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.buildConstructions import BuildConstructionDialog

OpenWindow(BuildConstructionDialog)
