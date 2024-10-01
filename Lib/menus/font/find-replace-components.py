# menuTitle : find & replace components

from importlib import reload
import xTools4.dialogs.font.componentsFind
reload(xTools4.dialogs.font.componentsFind)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.font.componentsFind import FindGlyphComponentsDialog

OpenWindow(FindGlyphComponentsDialog)
