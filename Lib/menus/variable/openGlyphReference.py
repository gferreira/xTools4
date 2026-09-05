# menuTitle: GlyphReference

from importlib import reload
import xTools4.dialogs.variable.GlyphReference
reload(xTools4.dialogs.variable.GlyphReference)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.variable.GlyphReference import GlyphReferenceController

OpenWindow(GlyphReferenceController)
