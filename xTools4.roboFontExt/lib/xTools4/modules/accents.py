'''
Tools to work with accented glyphs using `Glyph Construction`_ syntax.

.. _Glyph Construction: https://github.com/typemytype/GlyphConstruction

'''

try:
    from glyphConstruction import *
except:
    # add GlyphConstruction module
    import sys
    modulePath = '/_code/GlyphConstruction/Lib'
    if modulePath not in sys.path:
        print('installing glyphConstruction module…')
        sys.path.append(modulePath)

from hTools3.modules.unicode import autoUnicode

#: A basic default list of latin diacritics.
ACCENTS = ['acute', 'grave', 'circumflex', 'dieresis', 'tilde', 'macron', 'breve', 'dotaccent', 'ring', 'cedilla', 'hungarumlaut', 'ogonek', 'caron']

def buildConstructionGlyph(constructionGlyph, font, clear=True, autoUnicodes=True):
    '''
    Low-level function to build a ConstructionGlyph in a given font.

    Args:
        constructionGlyph: A `ConstructionGlyph` object.

    Returns:
        The newly constructed glyph.

    '''

    # create new glyph in the font
    if constructionGlyph.name not in font:
        glyph = font.newGlyph(constructionGlyph.name)
    else:
        glyph = font[constructionGlyph.name]

    # clear target glyph contents
    if clear:
        glyph.clear()

    ### HACK: check if all components are in the font, otherwise RF will freeze
    components = [c for c, m in constructionGlyph.components]
    canBuild = all([g in font for g in components])

    if not canBuild:
        return

    # copy construction glyph data to new glyph
    constructionGlyph.draw(glyph.getPen())

    # copy glyph attributes
    glyph.name    = constructionGlyph.name
    glyph.unicode = constructionGlyph.unicode
    glyph.note    = constructionGlyph.note
    glyph.width   = constructionGlyph.width

    # set unicode
    if autoUnicodes:
        autoUnicode(glyph)

    return glyph

def buildGlyphConstruction(font, construction, clear=True, verbose=False, indentLevel=0, autoUnicodes=True): # markColor=None

    '''
    Build glyph from Glyph Construction rule in the given font.

    Args:
        font (RFont): A font object.
        construction (str): A Glyph Construction rule.
        clear (bool): Clear glyph contents before constructing new glyph.
        verbose (bool): Turn text output on/off.
        indentLevel (int): Number of indents before text output lines.
        autoUnicodes (bool): Automatically set the unicode value for the constructed glyph.

    Returns:
        The newly constructed glyph.

    ::

        from hTools3.modules.accents import buildGlyphConstruction
        construction = "agrave = a + grave@center,`top+100`"
        f = CurrentFont()
        buildGlyphConstruction(f, construction, clear=True, verbose=False, indentLevel=0, autoUnicodes=True)

    '''

    # make construction glyph
    constructionGlyph = GlyphConstructionBuilder(construction, font)

    # print info
    if verbose:
        print('%sbuilding %s...' % ('\t' * indentLevel, constructionGlyph.name))

    # build construction glyph in the font
    glyph = buildConstructionGlyph(constructionGlyph, font, clear=clear, autoUnicodes=autoUnicodes)

    return glyph

def buildAccentedGlyphs(font, glyphNames, glyphConstructions, clear=True, markColor=None, verbose=False, indentLevel=0, autoUnicodes=True):
    '''
    Build accented glyphs in the current font using Glyph Construction rules.

    Args:
        font (RFont): A font object.
        glyphNames (list): A list of accented glyph names to build in the given font.
        glyphConstructions (str): A string of Glyph Construction definitions, one per line.
        clear (bool): Clear glyph contents before constructing new glyphs.
        markColor (tuple): Optional mark color for the constructed glyphs.
        verbose (bool): Turn text output on/off.
        indentLevel (int): Number of indents before text output lines.
        autoUnicodes (bool): Automatically set the unicode value for the constructed glyphs.

    ::

        from hTools3.modules.accents import buildAccentedGlyphs

        f = CurrentFont()

        constructions = """\
        agrave = a + grave@center,`top+100`
        aacute = a + acute@center,`top+100`
        """

        buildAccentedGlyphs(f, ['agrave'], constructions, verbose=True, indentLevel=0, markColor=(0, 1, 1, 0.5), clear=True)

    '''

    # parse glyph constructions
    constructions = ParseGlyphConstructionListFromString(glyphConstructions)

    for construction in constructions:
        if not len(construction):
            continue

        # build construction glyph
        cg = GlyphConstructionBuilder(construction, font)

        # only build glyphs names in the list
        if cg.name not in glyphNames:
            continue

        # print info
        if verbose:
            tab = '\t' * indentLevel
            print(f"{tab}building {cg.name}...")

        # build glyph in the font
        buildConstructionGlyph(cg, font, clear=clear, autoUnicodes=autoUnicodes)

def buildGlyphConstructions(font, glyphConstructions, clear=True, markColor=None, verbose=False, indentLevel=0, autoUnicodes=True):
    r'''
    Build new glyphs in a font from a string of Glyph Construction definitions.

    Args:
        font (RFont): A font object.
        glyphConstructions (str): A string of Glyph Construction definitions, one per line.
        clear (bool): Clear glyph contents before constructing new glyph.
        markColor (tuple): Optional mark color for the constructed glyphs.
        verbose (bool): Turn text output on/off.
        indentLevel (int): Number of indents before text output lines.
        autoUnicodes (bool): Automatically set the unicode value for the constructed glyphs.
        glyphNames (list): A list of glyph names to restrict the output. If the list is empty, all glyph construction definitions are built.

    Returns:
        A list with the names of all built glyphs.

    ::

        from hTools3.modules.accents import buildGlyphConstructions

        f = CurrentFont()

        constructions = """\
        agrave = a + grave@center,`top+100`
        aacute = a + acute@center,`top+100`
        """

        buildGlyphConstructions(f, constructions, verbose=True, indentLevel=0, markColor=(0, 1, 1, 0.5), clear=True)

    '''
    builtGlyphs = []

    # parse glyph construction text
    constructions = ParseGlyphConstructionListFromString(glyphConstructions)

    # build new glyphs
    for construction in constructions:
        if not len(construction):
            continue

        glyph = buildGlyphConstruction(font, construction, clear=clear, markColor=markColor, verbose=verbose, indentLevel=indentLevel, autoUnicodes=autoUnicodes)

        # set mark color
        if markColor:
            glyph.markColor = markColor

        glyph.changed()
        builtGlyphs.append(glyph.name)

    return builtGlyphs

def extractGlyphConstructions(font, glyphNames=None, accents=ACCENTS):
    '''
    Extract Glyph Construction rules from components in glyphs.

    Args:
        font (RFont): A font object.
        glyphNames (list): A list with names of glyphs from which to extract glyph constructions.
        accents (list): A list with names of glyphs which are not base glyphs. *(optional)*

    Returns:
        A string of Glyph Construction definitions, one per line.

    ::

        >>> from hTools3.modules.accents import buildGlyphConstructions
        >>> f = CurrentFont()
        >>> constructions = extractGlyphConstructions(f, glyphNames=['agrave', 'aacute'])
        >>> print(constructions)
        agrave = a + grave
        aacute = a + acute

    .. note:: The extracted glyph construction definitions are very basic. You’ll probably want to refine them with positioning instructions. See the `Glyph Construction`_ documentation for syntax examples.

    '''
    # get selected glyph names
    if not glyphNames:
        glyphNames = font.glyphOrder

    # collect extracted constructions
    constructions = []
    for glyphName in glyphNames:
        g = font[glyphName]
        if not len(g.components):
            continue
        constructions.append(extractGlyphConstruction(g, accents))

    # join constructions as multi-line string
    return '\n'.join(constructions)

def extractGlyphConstruction(glyph, accents=ACCENTS):
    '''
    Extract Glyph Construction rule from a glyph with components.

    Args:
        glyph (RGlyph): A glyph object.
        accents (list): A list with names of glyphs which are not base glyphs. *(optional)*

    Returns:
        A string of Glyph Construction definitions, one per line.

    ::

        >>> from hTools3.modules.accents import extractGlyphConstruction
        >>> g = CurrentGlyph()
        >>> construction = extractGlyphConstruction(g)
        >>> print(construction)
        agrave = a + grave

    '''

    # collect base glyphs & accents separately
    baseGlyphs = []
    accentGlyphs = []
    for c in glyph.components:
        if c.baseGlyph in accents:
            accentGlyphs.append(c.baseGlyph)
        else:
            baseGlyphs.append(c.baseGlyph)

    # join components in the right order (base + accents)
    components = baseGlyphs + accentGlyphs

    # make glyph construction
    construction = '%s = ' % glyph.name
    for i, gName in enumerate(components):
        construction += gName
        if i < len(components) - 1:
            construction += ' + '

    # done
    return construction
