# menuTitle : create anchors

from importlib import reload
import hTools4.dialogs.glyphs.anchorsCreate
reload(hTools4.dialogs.glyphs.anchorsCreate)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.anchorsCreate import CreateAnchorsDialog

OpenWindow(CreateAnchorsDialog)
