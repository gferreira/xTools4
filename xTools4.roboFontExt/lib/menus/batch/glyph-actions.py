# menuTitle : glyph actions

from importlib import reload
import xTools4.dialogs.batch.actions
reload(xTools4.dialogs.batch.actions)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.actions import BatchActionsDialog

OpenWindow(BatchActionsDialog)
