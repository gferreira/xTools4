# menuTitle : clear font data

from importlib import reload
import xTools4.dialogs.font.clearData
reload(xTools4.dialogs.font.clearData)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.font.clearData import ClearFontDataDialog

OpenWindow(ClearFontDataDialog)
