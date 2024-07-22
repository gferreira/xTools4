# menuTitle : find & replace components

from importlib import reload
import hTools4.dialogs.font.componentsFind
reload(hTools4.dialogs.font.componentsFind)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.font.componentsFind import FindGlyphComponentsDialog

OpenWindow(FindGlyphComponentsDialog)
