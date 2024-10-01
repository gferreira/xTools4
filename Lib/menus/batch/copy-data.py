# menuTitle : copy data

from importlib import reload
import xTools4.dialogs.batch.copy
reload(xTools4.dialogs.batch.copy)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.copy import BatchCopyDialog

OpenWindow(BatchCopyDialog)
