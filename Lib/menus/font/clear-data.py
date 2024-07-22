# menuTitle : clear font data

from importlib import reload
import hTools4.dialogs.font.clearData
reload(hTools4.dialogs.font.clearData)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.font.clearData import ClearFontDataDialog

OpenWindow(ClearFontDataDialog)
