# menuTitle : actions

from importlib import reload
import xTools4.dialogs.glyphs.actions
reload(xTools4.dialogs.glyphs.actions)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.actions import GlyphActionsDialog

OpenWindow(GlyphActionsDialog)