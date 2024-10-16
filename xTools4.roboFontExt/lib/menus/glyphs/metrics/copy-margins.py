# menuTitle : copy margins

from importlib import reload
import xTools4.dialogs.glyphs.old.marginsCopy
reload(xTools4.dialogs.glyphs.old.marginsCopy)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.marginsCopy import CopyMarginsDialog

OpenWindow(CopyMarginsDialog)
