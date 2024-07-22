# menuTitle : copy anchors

from importlib import reload
import hTools4.dialogs.glyphs.anchorsCopy
reload(hTools4.dialogs.glyphs.anchorsCopy)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.anchorsCopy import CopyAnchorsDialog

OpenWindow(CopyAnchorsDialog)
