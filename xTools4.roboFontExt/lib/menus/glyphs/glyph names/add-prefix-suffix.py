# menuTitle : add prefix / suffix

from importlib import reload
import xTools4.dialogs.glyphs.namesSuffix
reload(xTools4.dialogs.glyphs.namesSuffix)

from mojo.roboFont import OpenWindow
from xTools4.dialogs.glyphs.namesSuffix import PrefixSuffixGlyphNamesDialog

OpenWindow(PrefixSuffixGlyphNamesDialog)