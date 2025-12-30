# menuTitle: swap glyphs

from xTools4.modules.fontutils import swapGlyphs

font = CurrentFont()

if len(font.selectedGlyphNames) != 2:
    print('please select two glyphs to swap')

else:
    glyphName1, glyphName2 = font.selectedGlyphNames
    swapGlyphs(font, glyphName1, glyphName2)
