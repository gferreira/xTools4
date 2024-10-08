# menuTitle : outline

from importlib import reload
import xTools4.dialogs.glyphs.outline
reload(xTools4.dialogs.glyphs.outline)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.outline import OutlineGlyphsDialog

OpenWindow(OutlineGlyphsDialog)
