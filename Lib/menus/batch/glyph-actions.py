# menuTitle : glyph actions

from importlib import reload
import hTools4.dialogs.batch.actions
reload(hTools4.dialogs.batch.actions)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.actions import BatchActionsDialog

OpenWindow(BatchActionsDialog)
