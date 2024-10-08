# menuTitle : copy margins

from importlib import reload
import xTools4.dialogs.glyphs.marginsCopy
reload(xTools4.dialogs.glyphs.marginsCopy)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.marginsCopy import CopyMarginsDialog

OpenWindow(CopyMarginsDialog)
