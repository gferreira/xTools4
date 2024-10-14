'''
Tools to work with encoding files, glyph sets, groups of glyphs etc.

'''

import os
from fontParts.fontshell import RFont
from fontTools.agl import UV2AGL, AGL2UV
from xTools4.modules.fontutils import clearMarkColors
from xTools4.modules.unicode import unicodeIntToHex, unicodeHexToInt, unicodesExtra
from colorsys import hls_to_rgb


def importEncoding(encPath):
    '''
    Import encoding from file.

    Args:
        encPath (str): Path to the encoding file.

    Returns:
        A list of glyph names, or ``None`` if the encoding file does not exist.

    ::

        >>> from xTools4.modules.encoding import importEncoding
        >>> encPath = '/myFolder/example.enc'
        >>> enc = importEncoding(encPath)
        >>> print(enc)
        ['.notdef', 'space', 'a', 'b', 'c', 'd', ... ]

    '''
    if os.path.exists(encPath):
        with open(encPath, 'r') as encFile:
            lines = encFile.readlines()
        glyphNames = []
        for line in lines:
            if not line.startswith('%') and not line.startswith('#'):
                glyphNames.append(line.strip())
        return glyphNames
    else:
        print('Error, this file does not exist.')

def extractEncoding(ufoPath, encPath=None):
    '''
    Extract encoding from a UFO font.

    Args:
        ufoPath (str): Path to UFO source font.
        encPath (str): Path to output file for saving the extracted encoding. *(optional)*

    Returns:
        A string of glyph names (one per line).

    ::

        >>> from xTools4.modules.encoding import extractEncoding
        >>> ufoPath = '/myFolder/example.ufo'
        >>> enc = extractEncoding(ufoPath)
        >>> print(enc)
        .notdef
        space
        a
        b
        c
        ...

    '''
    ufo = RFont(ufoPath)
    enc = ''
    for glyphName in ufo.glyphOrder:
        enc += '%s\n' % glyphName
    ufo.close()

    if encPath is not None:
        with open(encPath, 'w') as encFile:
            encFile.write(enc)
            encFile.close()

    return enc

def importGroupsFromEncoding(encPath):
    '''
    Import groups and glyph names from a *structured encoding file*.

    Args:
        encPath (str): Path to the encoding file.

    Returns:
        A dictionary with group names (keys) and glyph names (values).

    ::

        >>> from xTools4.modules.encoding import importGroupsFromEncoding
        >>> encPath = '/myFolder/example.enc'
        >>> groups = importGroupsFromEncoding(encPath)
        >>> print(groups.keys())
        ['spaces', 'latin lc', 'latin uc', 'punctuation', ... ]
        >>> print(groups['punctuation'])
        ['comma', 'period', 'semicolon', 'colon', 'exclam', 'question', 'exclamdown', 'questiondown']

    '''
    if not os.path.exists(encPath):
        return

    with open(encPath, 'r') as f:
        lines = f.readlines()

    groups = {}
    count = 0
    for line in lines:
        if count == 0:
            pass
        elif line.startswith('#'):
            continue
        elif line.startswith('%'):
            groupName = line[18:-1]
            if len(groupName) > 0:
                groups[groupName] = []
        else:
            glyphName = line[:-1]
            groups[groupName].append(glyphName)

        count = count + 1

    return groups

def setGlyphOrder(font, encPath, verbose=False, createTemplates=True, createGlyphs=False):
    '''
    Sets the font's glyph order based on the given encoding file.

    Args:
        font (RFont): A font object.
        encPath (str): Path to encoding file.
        verbose (bool): Turn text output on/off.
        createTemplates (bool): Create template glyphs for glyphs which do not exist in the font.
        createGlyphs (bool): Create empty glyphs for glyphs which do not exist in the font.

    ::

        from xTools4.modules.encoding import setGlyphOrder
        encPath = '/myFolder/example.enc'
        font = CurrentFont()
        setGlyphOrder(font, encPath, verbose=True)

    '''
    if verbose:
        print('setting glyph order...')

    # import encoding from file
    glyphNames = importEncoding(encPath)

    # collect used glyph names
    glyphOrder = []

    for glyphName in glyphNames:

        # glyph already exists in font
        if glyphName in font.keys():
            glyphOrder.append(glyphName)

        else:
            # create glyph
            if createGlyphs:
                font.newGlyph(glyphName)
                glyphOrder.append(glyphName)
                if verbose:
                    print('\tcreating glyph: %s...' % glyphName)

            # create template glyph
            elif createTemplates:
                glyphOrder.append(glyphName)
                if verbose:
                    print('\tcreating template glyph: %s...' % glyphName)

            # glyph does not exist in font
            else:
                if verbose:
                    print('\t%s not in font' % glyphName)

    # set glyph order (excluding non-existing glyphs)
    font.glyphOrder = glyphOrder

    # done
    font.changed()
    if verbose:
        print('...done.\n')

def paintGroups(font, groups, crop=False):
    '''
    Mark glyphs in the font according to their given groups.

    Args:
        font (RFont): A font object.
        groups (dict): A dictionary of group names (keys) and lists of glyph names (values).
        crop (bool): If ``True``, glyphs which are not in any group will be deleted.

    ::

        from xTools4.modules.encoding import importGroupsFromEncoding
        encPath = '/myFolder/example.enc'
        groups = importGroupsFromEncoding(encPath)
        font = CurrentFont()
        paintGroups(font, groups, crop=False)

    '''
    clearMarkColors(font)

    glyphOrder = []
    colorStep = 1.0 / len(groups)

    for i, group in enumerate(groups.keys()):
        color = colorStep * i
        R, G, B = hls_to_rgb(color, 0.5, 1.0)
        for glyphName in groups[group]:
            if not glyphName in font.keys():
                font.newGlyph(glyphName)
            glyphOrder.append(glyphName)
            font[glyphName].markColor = (R, G, B, 0.3)
            font[glyphName].changed()

    font.glyphOrder = glyphOrder
    font.changed()

    if crop:
        cropGlyphset(font, glyphOrder)

def cropGlyphset(font, glyphNames):
    '''
    Reduce the font's character set, keeping only glyphs with names in the given list.

    Args:
        font (RFont): A font object.
        glyphNames (list): A list of glyph names.

    ::

        from xTools4.modules.encoding import cropGlyphset
        font = CurrentFont()
        cropGlyphset(font, ['space', 'a', 'b', 'c'])

    '''
    allGlyphNames = list(font.keys())
    for glyphName in allGlyphNames:
        glyph = font[glyphName]
        if glyph.name not in glyphNames:
            if glyph.name is not None:
                font.removeGlyph(glyph.name)

    font.changed()

def allGlyphs(groupsDict):
    '''
    Make a list of all glyphs in all groups in the given groups dict.

    '''
    glyphs = []
    for groupName in groupsDict.keys():
        glyphs += groupsDict[groupName]

    return glyphs

def char2psname(char, unicodesExtra={}):
    '''
    Get the PostScript name for a given unicode character.

    Args:
        char (str): A unicode character.

    Returns:
        A PostScript glyph name.

    ::

        >>> from xTools4.modules.encoding import char2psname
        >>> char2psname('&')
        ampersand

    '''
    # get unicode value for char
    uni = ord(char)
    psname = None

    # get unicode from extra dict
    if len(unicodesExtra):
        uniExtra = {v: k for k, v in unicodesExtra.items()}
        uniHex = unicodeIntToHex(uni)
        psname = uniExtra.get(uniHex)

    # get unicode from fontTools
    if psname is None:
        psname = UV2AGL.get(uni)

    return psname

def psname2char(glyphName, unicodesExtra={}):
    '''
    Get the unicode character for a given PostScript name.

    Args:
        glyphName (str): A PostScript glyph name.
        unicodesExtra (dict): Additional mappings of glyph names to unicode charactars.

    Returns:
        A unicode character.

    ::

        >>> from xTools4.modules.encoding import psname2char
        >>> psname2char('seven')
        7
        >>> psname2char('uni013B')
        Ļ

    '''
    if glyphName in AGL2UV:
        uni = AGL2UV[glyphName]

    # check unicode extras
    elif glyphName in unicodesExtra:
        uni = unicodesExtra[glyphName]

    # check for uni names
    elif glyphName.startswith('uni'):
        uni = glyphName[3:]

    else:
        return

    # get character from unicode
    try:
        char = chr(uni)
    except:
        uniInt = unicodeHexToInt(str(uni))
        char = chr(uniInt)

    # done
    return char

def psname2unicode(glyphName, unicodesExtra={}):
    '''
    Get the unicode value for a given PostScript name.

    Args:
        glyphName (str): A PostScript glyph name.

    Returns:
        A unicode character or `None`.

    ::

        >>> from xTools4.modules.encoding import psname2unicode
        >>> psname2unicode('zero')
        0030

    '''
    if glyphName in AGL2UV:
        uni = AGL2UV[glyphName]

    # check unicode extras
    elif glyphName in unicodesExtra:
        uni = unicodesExtra[glyphName]

    # check for uni names
    elif glyphName.startswith('uni'):
        uni = glyphName[3:]

    else:
        return

    # convert hex to integer
    uni = str(unicodeIntToHex(uni))

    return uni

# -------------------
# auto unicode ranges
# -------------------

def _getUnicodeBlocksFromFile(blocksFilePath):
    '''
    Import unicode blocks data from file.

    '''
    with open(blocksFilePath, mode='r') as blocksFile:
        lines = blocksFile.readlines()

    blocks = {}
    for line in lines:
        if not line.startswith('#') and not len(line.split()) == 0:
            blockRange, blockName = line.split(';')
            blockName = blockName.strip()
            blockStartHex, blockEndHex = blockRange.split('..')
            blocks[blockName] = (blockStartHex, blockEndHex)

    return blocks

def _checkUnicodeCoverage(font, blocks):

    # build unicodes / gnames dict for font
    unicodes = {}
    for g in font:
        if len(g.unicodes) > 0:
            unicodes[g.unicodes[0]] = g.name

    blocksCodepoints = {}
    for block in blocks.keys():
        blocksCodepoints[block] = []
        startHex, endHex = blocks[block]
        startInt = unicodeHexToInt(startHex)
        endInt   = unicodeHexToInt(endHex)
        # expand codepoints for unicode blocks
        for i in range(startInt, endInt + 1):
            blocksCodepoints[block].append((i, i in unicodes))

    return blocksCodepoints

def _getUnicodeBlocks(font, blocksCodepoints):

    # check font support in each block
    blocksSupport = {}
    for block in blocksCodepoints.keys():
        supported    = 0
        notSupported = 0
        for codepoint, support in blocksCodepoints[block]:
            if support:
                supported += 1
            else:
                notSupported += 1
        blocksSupport[block] = [supported, notSupported]

    # map unicode blocks to OS/2 range numbers
    unicodeBlocks = []
    for block in blocksSupport.keys():
        if blocksSupport[block][0] > 0:
            unicodeBlocks.append(block)

    return unicodeBlocks

def _getOS2unicodeRangesFromFile(OS2unicodeRangesFilePath):

    with open(OS2unicodeRangesFilePath, mode='r') as OS2unicodeRangesFile:
        lines = OS2unicodeRangesFile.readlines()

    OS2unicodeRanges = {}
    for line in lines:
        if len(line.split(';')) == 5:
            bit, unicodeRange, blockStart, blockEnd = line.split(';')[:4]
            OS2unicodeRanges[unicodeRange.strip()] = [int(bit), (blockStart.strip(), blockEnd.strip())]

    return OS2unicodeRanges

def _getOS2unicodeRanges(unicodeBlocks, OS2unicodeRanges):

    bits = []
    for block in unicodeBlocks:
        bits.append(OS2unicodeRanges[block][0])

    return bits

def _setOS2unicodeRanges(ufo, blocks, OS2ranges):
    blocksCoverage = _checkUnicodeCoverage(ufo, blocks)
    unicodeBlocks  = _getUnicodeBlocks(ufo, blocksCoverage)
    unicodeRanges  = _getOS2unicodeRanges(unicodeBlocks, OS2ranges)
    ufo.info.openTypeOS2UnicodeRanges = unicodeRanges

def autoOS2unicodeRanges(ufo):
    '''
    Automatically set `OS/2 Unicode Ranges`_ in the given font.

    .. _OS/2 Unicode Ranges: http://docs.microsoft.com/en-us/typography/opentype/spec/os2#ur

    ::

        >>> from xTools4.modules.encoding import autoOS2unicodeRanges
        >>> f = CurrentFont()
        >>> print(f.info.openTypeOS2UnicodeRanges)
        None
        >>> autoOS2unicodeRanges(f)
        >>> print(f.info.openTypeOS2UnicodeRanges)
        [0, 1, 2, 3, 5, 6, 29, 31, 33, 35, 38]

    '''
    modulesDir = os.path.dirname(__file__)
    baseDir    = os.path.dirname(modulesDir)
    extrasDir  = os.path.join(baseDir, 'extras')

    blocksFilePath           = os.path.join(extrasDir, 'unicode-blocks.txt')
    OS2unicodeRangesFilePath = os.path.join(extrasDir, 'unicode-ranges.txt')

    blocks = _getUnicodeBlocksFromFile(blocksFilePath)
    ranges = _getOS2unicodeRangesFromFile(OS2unicodeRangesFilePath)

    _setOS2unicodeRanges(ufo, blocks, ranges)

