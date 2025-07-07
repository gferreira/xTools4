'''
Tools to work with anchors.

'''

def copyAnchors(sourceGlyph, targetGlyph, clear=True, proportional=False):
    '''
    Copy all anchors from one glyph to another glyph.

    Args:
        sourceGlyph (RGlyph): A glyph object with anchors to copy from.
        targetGlyph (RGlyph): A glyph object to copy the anchors to.
        proportional (bool): Scale the target anchors’ horizontal position based on the target glyph’s width.
        clear (bool): Delete all anchors in target glyph before copying.

    ::

        from xTools4.modules.anchors import copyAnchors
        font = CurrentFont()
        g1 = font['a']
        g2 = font['o']
        copyAnchors(g1, g2, clear=True, proportional=True)

    '''
    # source glyph has no anchors
    if not len(sourceGlyph.anchors):
        return

    # collect anchors in source glyph
    anchorsDict = {}
    for a in sourceGlyph.anchors:
        anchorsDict[a.name] = a.x, a.y

    # clear anchors in target glyph
    if clear:
        targetGlyph.clearAnchors()

    # create anchors in target glyph
    for anchor in anchorsDict:
        x, y = anchorsDict[anchor]
        if proportional:
            factor = targetGlyph.width / float(sourceGlyph.width)
            x *= factor
        targetGlyph.appendAnchor(anchor, (x, y))
        targetGlyph.changed()

def renameAnchor(glyph, anchorName):
    pass