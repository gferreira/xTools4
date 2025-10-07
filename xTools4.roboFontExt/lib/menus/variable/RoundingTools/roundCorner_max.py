# menuTitle: round corner max

from importlib import reload
import xTools4.modules.rounding
reload(xTools4.modules.rounding)

from xTools4.modules.rounding import addRoundingCorner

glyph = CurrentGlyph()
addRoundingCorner(glyph, mode=1, radius=100)
