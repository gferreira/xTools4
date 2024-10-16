# menuTitle : lock widths

from importlib import reload
import xTools4.dialogs.glyphs.old.layersLock
reload(xTools4.dialogs.glyphs.old.layersLock)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.layersLock import LockLayerWidthsDialog

OpenWindow(LockLayerWidthsDialog)
