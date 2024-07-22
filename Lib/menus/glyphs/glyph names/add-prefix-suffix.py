# menuTitle : add prefix / suffix

from importlib import reload
import hTools4.dialogs.glyphs.namesSuffix
reload(hTools4.dialogs.glyphs.namesSuffix)

from mojo.roboFont import OpenWindow
from hTools4.dialogs.glyphs.namesSuffix import PrefixSuffixGlyphNamesDialog

OpenWindow(PrefixSuffixGlyphNamesDialog)
