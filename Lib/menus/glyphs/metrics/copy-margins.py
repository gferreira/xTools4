# menuTitle : copy margins

from importlib import reload
import hTools4.dialogs.glyphs.marginsCopy
reload(hTools4.dialogs.glyphs.marginsCopy)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.marginsCopy import CopyMarginsDialog

OpenWindow(CopyMarginsDialog)
