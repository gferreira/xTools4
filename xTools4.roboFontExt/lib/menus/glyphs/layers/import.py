# menuTitle : import

from importlib import reload
import xTools4.dialogs.glyphs.old.layersImport
reload(xTools4.dialogs.glyphs.old.layersImport)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.layersImport import ImportGlyphsIntoLayerDialog

OpenWindow(ImportGlyphsIntoLayerDialog)
