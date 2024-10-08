'''
Some helper functions around Frederik Berlaen's `OutlinePen`_.

.. _OutlinePen: http://github.com/typemytype/outlinerRoboFontExtension

'''

from hTools3.extras.outline import *
from fontParts.world import NewFont

def makeOutline(glyph, distance, join, cap, inner=True, outer=True, miter=None):
    '''
    Calculate expanded outlines for a given glyph using the ``OutlinePen``.

    Args:
        distance (int or float): The amount of outline to apply.
        join (int): The type of linejoin.
        cap (int): The type of linecap.
        inner (bool): Include or not the inner outline contour.
        outer (bool): Include or not the outer outline contour.
        miter (float or None): The miter value. Used only if the linejoin style is *miter*.

    Returns:
        An ``OutlinePen`` which can draw the resulting outlined shape into a glyph.

    ::

        from hTools3.modules.outline import makeOutline
        sourceGlyph = CurrentGlyph()
        outlinePen = makeOutline(sourceGlyph, 20, 0, 0)
        targetGlyph = sourceGlyph.getLayer('outline')
        targetGlyph.clear()
        targetPen = targetGlyph.getPointPen()
        outlinePen.drawPoints(targetPen)

    '''
    # TODO: join options should be Square / Miter / Round ?
    optionsCap  = ['Square', 'Round', 'Butt']
    optionsJoin = ['Square', 'Round', 'Butt']
    pen = OutlinePen(glyph.font,
            distance,
            connection=optionsJoin[join],
            cap=optionsCap[cap],
            miterLimit=miter,
            closeOpenPaths=True)
    glyph.draw(pen)
    pen.drawSettings(drawOriginal=False, drawInner=inner, drawOuter=outer)
    return pen

def expandGlyph(sourceGlyph, targetGlyph, distance, join=1, cap=1, inner=True, outer=True, miter=None, round=False, clear=True):
    '''
    Expand glyph outlines by a given amount of units.

    Args:
        sourceGlyph (RGlyph): The input glyph with contours to be outlined.
        targetGlyph (RGlyph): The destination glyph where the output outlined shape will be drawn.
        distance (int): The amount of outline to apply.
        join (int): The type of linejoin.
        cap (int): The type of linecap.
        inner (bool): Include or not the inner outline contour.
        outer (bool): Include or not the outer outline contour.
        round (bool): Round or not glyph coordinates to integers.
        miter (float or None): The miter value. Used only if the linejoin style is *miter*.
        clear (bool): Clear the contents of the target glyph before drawing.

    ::

        from hTools3.modules.outline import expandGlyph
        f = CurrentFont()
        sourceGlyph = f['O']
        targetGlyph = f['space']
        distance = 20
        expandGlyph(sourceGlyph, targetGlyph, distance, join=0, cap=0, inner=True, outer=True, clear=True)

    '''
    # calculate outline shape
    outlinePen = makeOutline(sourceGlyph, distance, join, cap, inner=inner, outer=outer, miter=miter)

    # clear destination glyph
    if clear:
        targetGlyph.clear()

    # copy outline to glyph
    targetPen = targetGlyph.getPointPen()
    outlinePen.drawPoints(targetPen)

    # round point positions to integers
    if round:
        targetGlyph.round()

def expandFont(sourceFont, distance, join=1, cap=1):
    '''
    Expand outlines of all glyphs in a font into a new font.

    Args:
        sourceFont (RFont): The input font with glyph contours to be outlined.
        distance (int or float): The amount of outline to apply.
        join (int): The type of linejoin.
        cap (int): The type of linecap.

    Returns:
        A new font containing the outlined glyphs.

    ::

        from hTools3.modules.outline import expandFont
        f = CurrentFont()
        distance = 20
        expandFont(f, distance, join=1, cap=1).openInterface()

    '''
    # create a new empty font
    targetFont = NewFont(showInterface=False)

    # expand all glyphs
    for glyphName in sourceFont.keys():

        # get source glyph
        sourceGlyph = sourceFont[glyphName]

        # get dest glyph
        targetFont.newGlyph(glyphName)
        targetGlyph = targetFont[glyphName]

        # expand glyph into dest font
        try:
            outlinePen = makeOutline(sourceGlyph, distance, join, cap)
            targetPen = targetGlyph.getPointPen()
            outlinePen.drawPoints(targetPen)
        except:
            pass

        # copy width from source glyph
        targetGlyph.width = sourceGlyph.width

        # copy components
        if len(sourceGlyph.components):
            for component in sourceGlyph.components:
                targetGlyph.appendComponent(component.baseGlyph, component.offset, component.scale)

    # done
    return targetFont


