# menuTitle : measure handles

from importlib import reload
import xTools4.dialogs.glyph.measureHandles
reload(xTools4.dialogs.glyph.measureHandles)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyph.measureHandles import MeasureHandlesController

OpenWindow(MeasureHandlesController)
