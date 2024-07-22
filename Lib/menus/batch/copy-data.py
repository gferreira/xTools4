# menuTitle : copy data

from importlib import reload
import hTools4.dialogs.batch.copy
reload(hTools4.dialogs.batch.copy)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.copy import BatchCopyDialog

OpenWindow(BatchCopyDialog)
