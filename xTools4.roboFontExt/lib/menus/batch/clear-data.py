# menuTitle : clear data

from importlib import reload
import xTools4.dialogs.batch.clear
reload(xTools4.dialogs.batch.clear)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.clear import BatchClearDialog

OpenWindow(BatchClearDialog)
