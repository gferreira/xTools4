# menuTitle : import

from importlib import reload
import xTools4.dialogs.glyphs.layersImport
reload(xTools4.dialogs.glyphs.layersImport)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.layersImport import ImportGlyphsIntoLayerDialog

OpenWindow(ImportGlyphsIntoLayerDialog)
