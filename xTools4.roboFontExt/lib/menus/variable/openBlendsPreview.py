# menuTitle: BlendsPreview

from importlib import reload
import xTools4.dialogs.variable.BlendsPreview
reload(xTools4.dialogs.variable.BlendsPreview)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.BlendsPreview import BlendsPreviewController

OpenWindow(BlendsPreviewController)
