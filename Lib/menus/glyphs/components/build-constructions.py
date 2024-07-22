# menuTitle : build constructions

from importlib import reload
import hTools4.dialogs.glyphs.buildConstructions
reload(hTools4.dialogs.glyphs.buildConstructions)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.buildConstructions import BuildConstructionDialog

OpenWindow(BuildConstructionDialog)
