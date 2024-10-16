# menuTitle : move

from importlib import reload
import xTools4.dialogs.glyphs.old.move
reload(xTools4.dialogs.glyphs.old.move)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.move import MoveGlyphsDialog

OpenWindow(MoveGlyphsDialog)
