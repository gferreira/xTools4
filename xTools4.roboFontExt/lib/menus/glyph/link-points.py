# menuTitle : link points

from importlib import reload
import xTools4.dialogs.glyph.linkPoints
reload(xTools4.dialogs.glyph.linkPoints)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyph.linkPoints import LinkPointsController

OpenWindow(LinkPointsController)
