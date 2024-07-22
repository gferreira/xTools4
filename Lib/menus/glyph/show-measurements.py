# menuTitle : show measurements

from importlib import reload
import hTools4.dialogs.glyph.measureHandles
reload(hTools4.dialogs.glyph.measureHandles)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyph.measureHandles import MeasureHandlesTool

OpenWindow(MeasureHandlesTool)
