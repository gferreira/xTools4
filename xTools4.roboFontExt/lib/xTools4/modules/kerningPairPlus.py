# http://www.unicode.org/reports/tr44/#General_Category_Values
CONTEXTS = {
    'Ll' : 'non', # lowercase letter
    'Lu' : 'HOH', # uppercase letter
    'Lo' : 'non', # other letter
    'Lm' : 'non', # modifier letter
    'Nd' : '080', # decimal number
    'No' : '080', # other number
    'Zs' : 'non', # space separator
    'Sm' : '080', # math symbol
    'Pd' : 'non', # dash punctuation
    'Pi' : 'non', # initial punctuation
    'Pf' : 'non', # final punctuation
    'Ps' : 'HOH', # open punctuation
    'Pe' : 'HOH', # close punctuation
    'Po' : 'non', # other punctuation
    'Sk' : 'non', # modifier symbol
    'Sc' : '080', # currency symbol
    'So' : 'non', # other symbol
    'Mn' : 'non', # non-spacing mark
}


class KerningPairPlus:
    
    '''
    A simple kerning pair which provides additional data about itself:

    - if a kerning pair item is a group, get a glyph of that group (for preview string)
    - get unicode glyph category for left/right pair items
    - get pre/after test strings based on glyph categories
    - get test string for kerning pair as a list of glyph names

    '''

    def __init__(self, font, pair):
        # TO-DO: try to use unicodeData directly without a font
        self.font = font # defcon font
        self.pair = pair

    @property
    def gName1(self):
        # glyph name or group name
        return self.pair[0]

    @property
    def gName2(self):
        # glyph name or group name
        return self.pair[1]

    @property
    def glyphName1(self):
        if self.gName1.startswith('public.kern') and self.gName1 in self.font.groups:
            return self.font.groups[self.gName1][0] 
        else:
            return self.gName1

    @property
    def glyphName2(self):
        if self.gName2.startswith('public.kern') and self.gName2 in self.font.groups:
            return self.font.groups[self.gName2][0] 
        else:
            return self.gName2

    @property
    def category1(self):
        return self.font.unicodeData.categoryForGlyphName(self.glyphName1)

    @property
    def category2(self):
        return self.font.unicodeData.categoryForGlyphName(self.glyphName2)

    @property
    def glyphsPre(self):
        L = list(CONTEXTS[self.category1] if self.category1 in CONTEXTS else 'HOH')
        return [self.font.unicodeData.glyphNameForUnicode(ord(char)) for char in L]

    @property    
    def glyphsAfter(self):
        L = list(CONTEXTS[self.category2] if self.category2 in CONTEXTS else 'HOH')
        return [self.font.unicodeData.glyphNameForUnicode(ord(char)) for char in L]

    @property
    def gNames(self):
        return self.glyphsPre + [self.gName1, self.gName2]+ self.glyphsAfter

    @property
    def glyphNames(self):
        return self.glyphsPre + [self.glyphName1, self.glyphName2] + self.glyphsAfter
