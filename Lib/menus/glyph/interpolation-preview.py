# menuTitle : interpolation preview

from importlib import reload
import hTools4.dialogs.glyph.interpolationPreview
reload(hTools4.dialogs.glyph.interpolationPreview)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyph.interpolationPreview import InterpolationPreviewDialog

OpenWindow(InterpolationPreviewDialog)
