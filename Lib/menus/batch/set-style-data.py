# menuTitle : set style data

from importlib import reload
import hTools4.dialogs.batch.setStyleData
reload(hTools4.dialogs.batch.setStyleData)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.setStyleData import BatchSetStyleDataDialog

OpenWindow(BatchSetStyleDataDialog)
