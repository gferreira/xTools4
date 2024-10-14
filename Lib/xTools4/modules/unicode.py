from collections import OrderedDict
from fontTools.agl import AGL2UV

'''
Tools to work with Unicode, convert glyph names to hex/unicode etc.

'''

# ---------------------------
# additional unicode mappings
# ---------------------------

#: A dict containing additional `glyphName` to `unicode` mappings.
unicodesExtra = {

    # extended latin lc
    'aemacron'        : '01E3',
    'dotlessj'        : '0237',
    'schwa'           : '0259',
    'ymacron'         : '0233',
    'eszett'          : '00DF',

    # extended latin uc
    'AEmacron'        : '01E2',
    'Schwa'           : '018F',
    'Uppercaseeszett' : '1E9E',

    # ligatures
    'fi'              : 'FB01',
    'fl'              : 'FB02',
    'f_f'             : 'FB00',
    'f_f_i'           : 'FB03',
    'f_f_l'           : 'FB04',

    # greek exceptions
    'Delta'           : '0394', # '2206'
    'Omega'           : '03A9', # '2126'
    'mu'              : '03BC', # '00B5'

    # superiors
    'zero.superior'   : '2070',
    'onesuperior'     : '00B9',
    'twosuperior'     : '00B2',
    'threesuperior'   : '00B3',
    'four.superior'   : '2074',
    'five.superior'   : '2075',
    'six.superior'    : '2076',
    'seven.superior'  : '2077',
    'eight.superior'  : '2078',
    'nine.superior'   : '2079',

    # inferiors
    'zeroinferior'    : '2080',
    'oneinferior'     : '2081',
    'twoinferior'     : '2082',
    'threeinferior'   : '2083',
    'fourinferior'    : '2084',
    'fiveinferior'    : '2085',
    'sixinferior'     : '2086',
    'seveninferior'   : '2087',
    'eightinferior'   : '2088',
    'nineinferior'    : '2089',

    # spaces
    'enspace'         : '2002',
    'emspace'         : '2003',
    'nbspace'         : '00A0',
    'hairspace'       : '200A',
    'thinspace'       : '2009',
    'thickspace'      : '2004',
    'figurespace'     : '2007',
    'zerowidthspace'  : '200B',

    # combining accents
    'gravecomb'       : '0300',
    'acutecomb'       : '0301',
    'circumflexcomb'  : '0302',
    'tildecomb'       : '0303',
    'dieresiscomb'    : '0308',
    'dotbelowcomb'    : '0323',
    'cedillacomb'     : '0327',

    # arrows
    'arrowleft'       : '2190',
    'arrowup'         : '2191',
    'arrowright'      : '2192',
    'arrowdown'       : '2193',
    'arrowleftright'  : '2194',
    'arrowupdown'     : '2195',
    'arrowupleft'     : '2196',
    'arrowupright'    : '2197',
    'arrowdownright'  : '2198',
    'arrowdownleft'   : '2199',

    # latin accented
    'Adotbelow'       : '1EA0',
    'adotbelow'       : '1EA1',
    'Aringacute'      : '01FA',
    'aringacute'      : '01FB',
    'Edotbelow'       : '1EB8',
    'edotbelow'       : '1EB9',
    'Etilde'          : '1EBC',
    'etilde'          : '1EBD',
    'Emacronacute'    : '1E16',
    'emacronacute'    : '1E17',
    'Gcaron'          : '01E6',
    'gcaron'          : '01E7',
    'Idotbelow'       : '1ECA',
    'idotbelow'       : '1ECB',
    'Ndotbelow'       : '1E46',
    'ndotbelow'       : '1E47',
    'Nhookleft'       : '019D',
    'nhookleft'       : '0272',
    'Odotbelow'       : '1ECC',
    'odotbelow'       : '1ECD',
    'Omacronacute'    : '1E52',
    'omacronacute'    : '1E53',
    'Oogonek'         : '01EA',
    'oogonek'         : '01EB',
    'Scedilla'        : '015E',
    'scedilla'        : '015F',
    'Scommaaccent'    : '0218',
    'scommaaccent'    : '0219',
    'Sdotbelow'       : '1E62',
    'sdotbelow'       : '1E63',
    'Tcedilla'        : '0162',
    'tcedilla'        : '0163',
    'Tcommaaccent'    : '021A',
    'tcommaaccent'    : '021B',
    'Udotbelow'       : '1EE4',
    'udotbelow'       : '1EE5',
    'Ymacron'         : '0232',
    'ymacron'         : '0233',
    'Ytilde'          : '1EF8',
    'ytilde'          : '1EF9',

    # symbols etc
    'bulletoperator'  : '2219',
    'florin'          : '0192',
    'apple'           : 'F8FF',
    'asteriskdbl'     : '2051',

}

# --------------
# unicode ranges
# --------------

# https://www.microsoft.com/typography/otspec/os2.htm
OS2UnicodeRangesSrc = '''\
0; Basic Latin; 0000; 007F;
1; Latin-1 Supplement; 0080; 00FF;
2; Latin Extended-A; 0100; 017F;
3; Latin Extended-B; 0180; 024F;
4; IPA Extensions; 0250; 02AF;
4; Phonetic Extensions; 1D00; 1D7F;
4; Phonetic Extensions Supplement; 1D80; 1DBF;
5; Spacing Modifier Letters; 02B0; 02FF;
5; Modifier Tone Letters; A700; A71F;
6; Combining Diacritical Marks; 0300; 036F;
6; Combining Diacritical Marks Supplement; 1DC0; 1DFF;
7; Greek and Coptic; 0370; 03FF;
8; Coptic; 2C80; 2CFF;
9; Cyrillic; 0400; 04FF;
9; Cyrillic Supplement; 0500; 052F;
9; Cyrillic Extended-A; 2DE0; 2DFF;
9; Cyrillic Extended-B; A640; A69F;
10; Armenian; 0530; 058F;
11; Hebrew; 0590; 05FF;
12; Vai; A500; A63F;
13; Arabic; 0600; 06FF;
13; Arabic Supplement; 0750; 077F;
14; NKo; 07C0; 07FF;
15; Devanagari; 0900; 097F;
16; Bengali; 0980; 09FF;
17; Gurmukhi; 0A00; 0A7F;
18; Gujarati; 0A80; 0AFF;
19; Oriya; 0B00; 0B7F;
20; Tamil; 0B80; 0BFF;
21; Telugu; 0C00; 0C7F;
22; Kannada; 0C80; 0CFF;
23; Malayalam; 0D00; 0D7F;
24; Thai; 0E00; 0E7F;
25; Lao; 0E80; 0EFF;
26; Georgian; 10A0; 10FF;
26; Georgian Supplement; 2D00; 2D2F;
27; Balinese; 1B00; 1B7F;
28; Hangul Jamo; 1100; 11FF;
29; Latin Extended Additional; 1E00; 1EFF;
29; Latin Extended-C; 2C60; 2C7F;
29; Latin Extended-D; A720; A7FF;
30; Greek Extended; 1F00; 1FFF;
31; General Punctuation; 2000; 206F;
31; Supplemental Punctuation; 2E00; 2E7F;
32; Superscripts And Subscripts; 2070; 209F;
33; Currency Symbols; 20A0; 20CF;
34; Combining Diacritical Marks For Symbols; 20D0; 20FF;
35; Letterlike Symbols; 2100; 214F;
36; Number Forms; 2150; 218F;
37; Arrows; 2190; 21FF;
37; Supplemental Arrows-A; 27F0; 27FF;
37; Supplemental Arrows-B; 2900; 297F;
37; Miscellaneous Symbols and Arrows; 2B00; 2BFF;
38; Mathematical Operators; 2200; 22FF;
38; Supplemental Mathematical Operators; 2A00; 2AFF;
38; Miscellaneous Mathematical Symbols-A; 27C0; 27EF;
38; Miscellaneous Mathematical Symbols-B; 2980; 29FF;
39; Miscellaneous Technical; 2300; 23FF;
40; Control Pictures; 2400; 243F;
41; Optical Character Recognition; 2440; 245F;
42; Enclosed Alphanumerics; 2460; 24FF;
43; Box Drawing; 2500; 257F;
44; Block Elements; 2580; 259F;
45; Geometric Shapes; 25A0; 25FF;
46; Miscellaneous Symbols; 2600; 26FF;
47; Dingbats; 2700; 27BF;
48; CJK Symbols And Punctuation; 3000; 303F;
49; Hiragana; 3040; 309F;
50; Katakana; 30A0; 30FF;
50; Katakana Phonetic Extensions; 31F0; 31FF;
51; Bopomofo; 3100; 312F;
51; Bopomofo Extended; 31A0; 31BF;
52; Hangul Compatibility Jamo; 3130; 318F;
53; Phags-pa; A840; A87F;
54; Enclosed CJK Letters And Months; 3200; 32FF;
55; CJK Compatibility; 3300; 33FF;
56; Hangul Syllables; AC00; D7AF;
57; Non-Plane 0 *; D800; DFFF;
58; Phoenician; 10900; 1091F;
59; CJK Unified Ideographs; 4E00; 9FFF;
59; CJK Radicals Supplement; 2E80; 2EFF;
59; Kangxi Radicals; 2F00; 2FDF;
59; Ideographic Description Characters; 2FF0; 2FFF;
59; CJK Unified Ideographs Extension A; 3400; 4DBF;
59; CJK Unified Ideographs Extension B; 20000; 2A6DF;
59; Kanbun; 3190; 319F;
60; Private Use Area; E000; F8FF;
61; CJK Strokes; 31C0; 31EF;
61; CJK Compatibility Ideographs; F900; FAFF;
61; CJK Compatibility Ideographs Supplement; 2F800; 2FA1F;
62; Alphabetic Presentation Forms; FB00; FB4F;
63; Arabic Presentation Forms-A; FB50; FDFF;
64; Combining Half Marks; FE20; FE2F;
65; Vertical Forms; FE10; FE1F;
65; CJK Compatibility Forms; FE30; FE4F;
66; Small Form Variants; FE50; FE6F;
67; Arabic Presentation Forms-B; FE70; FEFF;
68; Halfwidth And Fullwidth Forms; FF00; FFEF;
69; Specials; FFF0; FFFF;
70; Tibetan; 0F00; 0FFF;
71; Syriac; 0700; 074F;
72; Thaana; 0780; 07BF;
73; Sinhala; 0D80; 0DFF;
74; Myanmar; 1000; 109F;
75; Ethiopic; 1200; 137F;
75; Ethiopic Supplement; 1380; 139F;
75; Ethiopic Extended; 2D80; 2DDF;
76; Cherokee; 13A0; 13FF;
77; Unified Canadian Aboriginal Syllabics; 1400; 167F;
78; Ogham; 1680; 169F;
79; Runic; 16A0; 16FF;
80; Khmer; 1780; 17FF;
80; Khmer Symbols; 19E0; 19FF;
81; Mongolian; 1800; 18AF;
82; Braille Patterns; 2800; 28FF;
83; Yi Syllables; A000; A48F;
83; Yi Radicals; A490; A4CF;
84; Tagalog; 1700; 171F;
84; Hanunoo; 1720; 173F;
84; Buhid; 1740; 175F;
84; Tagbanwa; 1760; 177F;
85; Old Italic; 10300; 1032F;
86; Gothic; 10330; 1034F;
87; Deseret; 10400; 1044F;
88; Byzantine Musical Symbols; 1D000; 1D0FF;
88; Musical Symbols; 1D100; 1D1FF;
88; Ancient Greek Musical Notation; 1D200; 1D24F;
89; Mathematical Alphanumeric Symbols; 1D400; 1D7FF;
90; Private Use (plane 15); FF000; FFFFD;
90; Private Use (plane 16); 100000; 10FFFD;
91; Variation Selectors; FE00; FE0F;
91; Variation Selectors Supplement; E0100; E01EF;
92; Tags; E0000; E007F;
93; Limbu; 1900; 194F;
94; Tai Le; 1950; 197F;
95; New Tai Lue; 1980; 19DF;
96; Buginese; 1A00; 1A1F;
97; Glagolitic; 2C00; 2C5F;
98; Tifinagh; 2D30; 2D7F;
99; Yijing Hexagram Symbols; 4DC0; 4DFF;
100; Syloti Nagri; A800; A82F;
101; Linear B Syllabary; 10000; 1007F;
101; Linear B Ideograms; 10080; 100FF;
101; Aegean Numbers; 10100; 1013F;
102; Ancient Greek Numbers; 10140; 1018F;
103; Ugaritic; 10380; 1039F;
104; Old Persian; 103A0; 103DF;
105; Shavian; 10450; 1047F;
106; Osmanya; 10480; 104AF;
107; Cypriot Syllabary; 10800; 1083F;
108; Kharoshthi; 10A00; 10A5F;
109; Tai Xuan Jing Symbols; 1D300; 1D35F;
110; Cuneiform; 12000; 123FF;
110; Cuneiform Numbers and Punctuation; 12400; 1247F;
111; Counting Rod Numerals; 1D360; 1D37F;
112; Sundanese; 1B80; 1BBF;
113; Lepcha; 1C00; 1C4F;
114; Ol Chiki; 1C50; 1C7F;
115; Saurashtra; A880; A8DF;
116; Kayah Li; A900; A92F;
117; Rejang; A930; A95F;
118; Cham; AA00; AA5F;
119; Ancient Symbols; 10190; 101CF;
120; Phaistos Disc; 101D0; 101FF;
121; Carian; 102A0; 102DF;
121; Lycian; 10280; 1029F;
121; Lydian; 10920; 1093F;
122; Domino Tiles; 1F030; 1F09F;
122; Mahjong Tiles; 1F000; 1F02F;
'''

OS2UnicodeRanges = OrderedDict()
for line in OS2UnicodeRangesSrc.split('\n'):
    if len(line.split(';')) == 5:
        bit, unicodeRange, blockStart, blockEnd = line.split(';')[:4]
        OS2UnicodeRanges[unicodeRange.strip()] = [int(bit), (blockStart.strip(), blockEnd.strip())]

# TODO: merge with encoding module??

def clearUnicodes(font):
    '''
    Clear unicodes from all glyphs in the font.

    ::
    
        from xTools4.modules.unicode import clearUnicodes
        f = CurrentFont()
        clearUnicodes(f)

    '''
    for g in font:
        g.unicodes = []
    font.changed()

def autoUnicodes(font, customUnicodes={}):
    '''
    Automatically set unicode values for all glyphs in the font.

    Args:
        font (RFont): A font object.
        customUnicodes (dict): A dictionary with additional glyph name to unicode mappings. (optional)

    ::

        from xTools4.modules.unicode import autoUnicodes
        uniExtras = {
            'uhornacute' : 7913,
            'uhorngrave' : 7915,
        }
        f = CurrentFont()
        autoUnicodes(f, customUnicodes=uniExtras)

    '''
    clearUnicodes(font)
    for g in font:
        if g is not None:
            autoUnicode(g, customUnicodes)
    font.changed()

def autoUnicode(glyph, customUnicodes=unicodesExtra, verbose=False, indent=0):
    '''
    Automatically set unicode value(s) for the specified glyph.

    This function uses RoboFont's ``glyph.autoUnicodes()`` first, and complements it with values from ``customUnicodes``.

    Args:
        glyph (RGlyph): A glyph object.
        customUnicodes (dict): A dictionary with additional glyphname to unicode mappings. (optional)

    ::

        from xTools4.modules.unicode import autoUnicode
        uniExtras = {
            'uhornacute' : 7913,
            'uhorngrave' : 7915,
        }
        g = CurrentGlyph()
        autoUnicode(g, customUnicodes=uniExtras)

    '''
    if glyph.name is not None:

        # uni-names
        if glyph.name[:3] == "uni" and len(glyph.name) in [7, 8]:
            uniSrc = 'uni-name'
            uniInt = int(glyph.name.split('uni')[1], 16)
            uniHex = unicodeIntToHex(uniInt)

        # extra unicodes
        elif glyph.name in unicodesExtra.keys():
            uniSrc = 'extra'
            uniHex = unicodesExtra[glyph.name]
            uniInt = unicodeHexToInt(uniHex)

        # custom unicodes
        elif customUnicodes.get(glyph.name) is not None:
            uniSrc = 'custom'
            uniInt = customUnicodes[glyph.name]
            uniHex = unicodeIntToHex(uniInt)

        # auto unicodes
        else:
            uniSrc = 'auto'
            # glyph.autoUnicodes() # this works only inside a font editor!
            glyph.unicode = AGL2UV.get(glyph.name)
            if glyph.unicode:
                uniInt = glyph.unicode
                uniHex = unicodeIntToHex(uniInt)
            else:
                uniInt = uniHex = None

        # set unicode
        glyph.unicode = uniInt
        if verbose:
            tabs = '\t' * indent
            if uniInt:
                print(f"{tabs}setting unicode for {glyph.name} ({glyph.layer.name}): {uniHex} ({uniInt}) [{uniSrc}]...")
            else:
                print(f"{tabs}no unicode for {glyph.name} ({glyph.layer.name}).")

        # done
        glyph.changed()

# ----------------------------
# unicode-to-string conversion
# ----------------------------

def unicodeIntToHex(intUnicode):
    '''
    Converts unicode integer to hexadecimal string.

    Args:
        intUnicode (int): A unicode value as an integer.

    ::

        from xTools4.modules.unicode import unicodeIntToHex
        >>> glyph = CurrentGlyph()
        >>> unicodeIntToHex(glyph.unicode)
        0061

    See also the reverse function :func:`unicodeHexToInt`.

    '''

    hexUnicode = "%X" % intUnicode
    hexUnicode = hexUnicode.zfill(4)

    return hexUnicode

def unicodeHexToInt(hexUnicode, stripUni=False):
    '''
    Converts unicode hexadecimal to integer.

    Args:
        hexUnicode (str): The hexadecimal unicode value as a string.
        stripUni (bool): An optional toggle to allow ``uniXXXX`` names.

    ::

        from xTools4.modules.unicode import unicodeHexToInt
        glyph = CurrentGlyph()
        glyph.unicode = unicodeHexToInt('0061')

    See also the reverse function :func:`unicodeIntToHex`.

    '''

    if stripUni:
        return int(hexUnicode.replace("uni", ""), 16)

    return int(hexUnicode.lstrip("x"), 16)

