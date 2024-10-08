# menuTitle : set data

from importlib import reload
import xTools4.dialogs.batch.set
reload(xTools4.dialogs.batch.set)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.set import BatchSetDialog

OpenWindow(BatchSetDialog)
