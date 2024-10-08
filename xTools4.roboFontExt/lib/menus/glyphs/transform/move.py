# menuTitle : move

from importlib import reload
import xTools4.dialogs.glyphs.move
reload(xTools4.dialogs.glyphs.move)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.move import MoveGlyphsDialog

OpenWindow(MoveGlyphsDialog)
