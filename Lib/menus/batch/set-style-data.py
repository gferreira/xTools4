# menuTitle : set style data

from importlib import reload
import xTools4.dialogs.batch.setStyleData
reload(xTools4.dialogs.batch.setStyleData)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.setStyleData import BatchSetStyleDataDialog

OpenWindow(BatchSetStyleDataDialog)
