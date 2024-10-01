# menuTitle : find & replace

from importlib import reload
import xTools4.dialogs.batch.findReplace
reload(xTools4.dialogs.batch.findReplace)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.findReplace import BatchFindReplaceDialog

OpenWindow(BatchFindReplaceDialog)
