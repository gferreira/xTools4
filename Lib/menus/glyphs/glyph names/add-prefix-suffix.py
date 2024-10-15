# menuTitle : add prefix / suffix

from importlib import reload
import xTools4.dialogs.glyphs.old.namesSuffix
reload(xTools4.dialogs.glyphs.old.namesSuffix)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.old.namesSuffix import PrefixSuffixGlyphNamesDialog

OpenWindow(PrefixSuffixGlyphNamesDialog)
