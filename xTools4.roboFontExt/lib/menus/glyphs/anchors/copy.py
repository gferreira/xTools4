# menuTitle : copy anchors

from importlib import reload
import xTools4.dialogs.glyphs.anchorsCopy
reload(xTools4.dialogs.glyphs.anchorsCopy)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.anchorsCopy import CopyAnchorsDialog

OpenWindow(CopyAnchorsDialog)
