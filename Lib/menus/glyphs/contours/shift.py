# menuTitle : shift

from importlib import reload
import hTools4.dialogs.glyphs.shiftPoints
reload(hTools4.dialogs.glyphs.shiftPoints)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.shiftPoints import ShiftPointsDialog

OpenWindow(ShiftPointsDialog)
