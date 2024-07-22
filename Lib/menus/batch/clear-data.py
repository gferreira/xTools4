# menuTitle : clear data

from importlib import reload
import hTools4.dialogs.batch.clear
reload(hTools4.dialogs.batch.clear)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.clear import BatchClearDialog

OpenWindow(BatchClearDialog)
