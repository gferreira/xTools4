# menuTitle: round corner min

from importlib import reload
import xTools4.modules.rounding
reload(xTools4.modules.rounding)

from xTools4.modules.rounding import addRoundingCorner

glyph = CurrentGlyph()
addRoundingCorner(glyph, mode=0)
