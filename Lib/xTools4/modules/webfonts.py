import os
import shutil
from base64 import b64encode
from fontTools import subset
from fontTools.ttLib import TTFont

try:
    from mojo.compile import executeCommand, hasTTFAutoHint
except ModuleNotFoundError:
    # print('mojo.compile is not available in this environment')
    pass

def subsetOTF(srcFontPath, dstFontPath, glyphNames=[], obfuscateNames=False, removeFeatures=False, removeKerning=False, removeHinting=False, verbose=True):
    '''
    Subset an OpenType font using the `FontTools subsetter`_.

    .. _FontTools subsetter: http://fonttools.readthedocs.io/en/latest/subset/

    Args:
        srcFontPath (str): The path to the source OpenType font.
        dstFontPath (str): The path to the target subsetted OpenType font.
        glyphNames (list): A list of glyph names to be included in the subsetted font.
        obfuscateNames (bool): Obfuscate font names.
        removeFeatures (bool): Remove all OpenType features.
        removeKerning (bool): Remove all kerning.
        removeHinting (bool): Remove hinting data.

    Returns:
        A boolean indicating if the subsetted font was generated successfully.

    ::

        from xTools4.modules.webfonts import subsetOTF

        srcFont = '/path/to/myFont.otf'
        dstFont = srcFont.replace('.otf', '_subset.otf')
        glyphNames = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()

        subsetOTF(srcFont, dstFont, glyphNames, obfuscateNames=False, removeFeatures=False, removeKerning=False, removeHinting=False, verbose=True)

    '''
    # input & output fonts
    command  = [srcFontPath]
    command += ["--output-file=%s" % dstFontPath]

    # glyph set
    if glyphNames:
        command += ["--glyphs=%s" % ','.join(glyphNames)]
        command += ["--ignore-missing-glyphs"]

    # name options
    command += ["--name-IDs=*"]
    command += ["--name-languages=0,1033"]
    command += ["--name-legacy"]
    if obfuscateNames:
        command += ["--obfuscate-names"]

    # features & kerning
    if removeKerning and removeFeatures:
        # kerning  NO  / features NO
        command += ["--layout-features=''"]
        command += ["--no-legacy-kern"]
    elif not removeKerning and removeFeatures:
        # kerning  YES / features NO
        command += ["--layout-features='kern'"]
        command += ["--legacy-kern"]
    elif removeKerning and not removeFeatures:
        # kerning  NO  / features YES
        command += ["--layout-features-='kern'"]
        command += ["--no-legacy-kern"]
    else:
        # kerning  YES / features YES
        command += ["--legacy-kern"]

    # hinting
    if removeHinting:
        command += ["--no-hinting"]
        command += ["--desubroutinize"]
        command += ["--hinting-tables=''"]

    if verbose:
        command += ["--verbose"]

    # run subset command
    subset.main(command)

    # done!
    return os.path.exists(dstFontPath)

# ------------
# base64 tools
# ------------

def encodeBase64(fontPath):
    '''
    Convert a font at a given path to base64 encoding.

    Args:
        fontPath (str): The path to the source OpenType font.

    Returns:
        A string of binary data encoded in the base64 format.

    ::
    
        from xTools4.modules.webfonts import encodeBase64

        ttfPath = '/path/to/myFont.ttf'
        fontData = encodeBase64(ttfPath)

        print(fontData)

    '''
    with open(fontPath,'rb') as f:
        fontData = f.read()
    return b64encode(fontData)

def fontFaceBase64Woff(fontName, fontData, fontWeight='normal', fontStyle='normal', fontFormat='woff', fontDisplay='auto', sass=False, variable=False):
    '''
    Generate a CSS or SASS ``@font-face`` declaration for a base64-encoded font.

    Args:
        fontName (str): The ``font-family`` of the font.
        fontData (str): The font data encoded in base64 format.
        fontWeight (str): The ``font-weight`` of the font. Options are `normal` and `bold`.
        fontStyle (str): The ``font-style`` of the font. Options are `normal` and `italic`.
        fontFormat (str): The format of the linked font file. Options are `woff`, `woff2`, `truetype`, `opentype`.
        sass (bool): Output code in `sass`_ format instead of plain CSS.

    .. _sass: http://sass-lang.com/

    ::
    
        from xTools4.modules.webfonts import encodeBase64, fontFaceBase64Woff

        fontPath = '/path/to/myFont.woff'
        fontData = encodeBase64(fontPath)
        fontFace = fontFaceBase64Woff('My Family', fontData, fontWeight='normal', fontStyle='normal', fontFormat='woff', sass=False)

        print(fontFace)

    '''
    varSuffix = '-variable' if variable else ''
    if sass:
        return f'''\
@font-face
    font-family: "{fontName}"
    src: url(data:application/x-font-woff;charset=utf-8;base64,{fontData.decode()}) format("{fontFormat}{varSuffix}")
    font-style: {fontStyle}
    font-weight: {fontWeight}
    font-display: {fontDisplay}
'''
    else: # plain CSS
        return f'''\
@font-face {{
    font-family: "{fontName}";
    src: url(data:application/x-font-woff;charset=utf-8;base64,{fontData.decode()}) format('{fontFormat}{varSuffix}');
    font-style: {fontStyle};
    font-weight: {fontWeight};
    font-display: {fontDisplay};
}}
'''

# ----------
# WOFF tools
# ----------

def sfnt2woff(fontPath, woffPath=None):
    '''
    Generate a .woff file from an .otf or .ttf font.

    ::

        from xTools4.modules.webfonts import sfnt2woff

        fontPath = '/path/to/myFont.ttf'
        woffPath = fontPath.replace('.ttf', '.woff')

        sfnt2woff(fontPath, woffPath)

    '''
    font = TTFont(fontPath)
    font.flavor = "woff"
    if not woffPath:
        woffPath = f'{os.path.splitext(fontPath)[0]}.woff'
    font.save(woffPath)

def sfnt2woff2(fontPath, woff2Path=None):
    '''
    Generate a .woff2 file from an .otf or .ttf font.

    ::

        from xTools4.modules.webfonts import sfnt2woff2

        fontPath = '/path/to/myFont.ttf'
        woff2Path = fontPath.replace('.ttf', '.woff2')

        sfnt2woff2(fontPath, woff2Path)

    '''
    font = TTFont(fontPath)
    font.flavor = "woff2"
    if not woff2Path:
        woff2Path = f'{os.path.splitext(fontPath)[0]}.woff2'
    font.save(woff2Path)
