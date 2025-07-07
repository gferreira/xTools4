# menuTitle : build constructions

from importlib import reload
import xTools4.dialogs.glyphs.old.buildConstructions
reload(xTools4.dialogs.glyphs.old.buildConstructions)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.buildConstructions import BuildConstructionDialog

OpenWindow(BuildConstructionDialog)
