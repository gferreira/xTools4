# menuTitle : import

from importlib import reload
import hTools4.dialogs.glyphs.layersImport
reload(hTools4.dialogs.glyphs.layersImport)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.layersImport import ImportGlyphsIntoLayerDialog

OpenWindow(ImportGlyphsIntoLayerDialog)
