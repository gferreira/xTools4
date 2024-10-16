# menuTitle : shift

from importlib import reload
import xTools4.dialogs.glyphs.old.shiftPoints
reload(xTools4.dialogs.glyphs.old.shiftPoints)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.shiftPoints import ShiftPointsDialog

OpenWindow(ShiftPointsDialog)
