# menuTitle : find & replace

from importlib import reload
import hTools4.dialogs.batch.findReplace
reload(hTools4.dialogs.batch.findReplace)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.findReplace import BatchFindReplaceDialog

OpenWindow(BatchFindReplaceDialog)
