# menuTitle : actions

from importlib import reload
import hTools4.dialogs.glyphs.actions
reload(hTools4.dialogs.glyphs.actions)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.actions import GlyphActionsDialog

OpenWindow(GlyphActionsDialog)