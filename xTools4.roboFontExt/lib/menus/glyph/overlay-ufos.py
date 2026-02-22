# menuTitle : overlay UFOs

from importlib import reload
import xTools4.dialogs.glyph.overlayUFOs
reload(xTools4.dialogs.glyph.overlayUFOs)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyph.overlayUFOs import OverlayUFOsController

OpenWindow(OverlayUFOsController)
