# menuTitle : outline

from importlib import reload
import xTools4.dialogs.glyphs.old.outline
reload(xTools4.dialogs.glyphs.old.outline)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.outline import OutlineGlyphsDialog

OpenWindow(OutlineGlyphsDialog)
