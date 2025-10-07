# menuTitle: round cap min

from importlib import reload
import xTools4.modules.rounding
reload(xTools4.modules.rounding)

from xTools4.modules.rounding import addRoundingCap

glyph = CurrentGlyph()
addRoundingCap(glyph, mode=0)
