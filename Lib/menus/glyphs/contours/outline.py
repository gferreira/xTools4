# menuTitle : outline

from importlib import reload
import hTools4.dialogs.glyphs.outline
reload(hTools4.dialogs.glyphs.outline)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.outline import OutlineGlyphsDialog

OpenWindow(OutlineGlyphsDialog)
