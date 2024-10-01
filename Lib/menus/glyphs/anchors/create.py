# menuTitle : create anchors

from importlib import reload
import xTools4.dialogs.glyphs.anchorsCreate
reload(xTools4.dialogs.glyphs.anchorsCreate)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.anchorsCreate import CreateAnchorsDialog

OpenWindow(CreateAnchorsDialog)
