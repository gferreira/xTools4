# menuTitle : shift

from importlib import reload
import xTools4.dialogs.glyphs.shiftPoints
reload(xTools4.dialogs.glyphs.shiftPoints)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.shiftPoints import ShiftPointsDialog

OpenWindow(ShiftPointsDialog)
