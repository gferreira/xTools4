# menuTitle : move

from importlib import reload
import hTools4.dialogs.glyphs.move
reload(hTools4.dialogs.glyphs.move)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.move import MoveGlyphsDialog

OpenWindow(MoveGlyphsDialog)
