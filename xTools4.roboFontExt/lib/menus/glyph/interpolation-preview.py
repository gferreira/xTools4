# menuTitle : interpolation preview

from importlib import reload
import xTools4.dialogs.glyph.interpolationPreview
reload(xTools4.dialogs.glyph.interpolationPreview)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyph.interpolationPreview import InterpolationPreviewController

OpenWindow(InterpolationPreviewController)
