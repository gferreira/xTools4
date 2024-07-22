# menuTitle : build glyphs

from importlib import reload
import hTools4.dialogs.batch.build
reload(hTools4.dialogs.batch.build)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.batch.build import BatchBuildGlyphsDialog

OpenWindow(BatchBuildGlyphsDialog)
