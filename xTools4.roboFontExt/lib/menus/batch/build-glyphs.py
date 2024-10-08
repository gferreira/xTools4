# menuTitle : build glyphs

from importlib import reload
import xTools4.dialogs.batch.build
reload(xTools4.dialogs.batch.build)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.batch.build import BatchBuildGlyphsDialog

OpenWindow(BatchBuildGlyphsDialog)
