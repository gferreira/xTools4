# menuTitle : link points

from importlib import reload
import hTools4.dialogs.glyph.linkPoints
reload(hTools4.dialogs.glyph.linkPoints)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyph.linkPoints import LinkPointsController

OpenWindow(LinkPointsController)
