# menuTitle : actions

from importlib import reload
import xTools4.dialogs.glyphs.old.actions
reload(xTools4.dialogs.glyphs.old.actions)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.actions import GlyphActionsDialog

OpenWindow(GlyphActionsDialog)