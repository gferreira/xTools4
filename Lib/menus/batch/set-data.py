# menuTitle : set data

from importlib import reload
import hTools4.dialogs.batch.set
reload(hTools4.dialogs.batch.set)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.set import BatchSetDialog

OpenWindow(BatchSetDialog)
