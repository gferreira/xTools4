# menuTitle: find nested components

from xTools4.modules.messages import noFontOpen, showMessage

# TODO: read global settings
messageMode = 1
verbose = True


def getNestingLevels(g, levels=0):
    if g.components:
        levels += 1
        for c in g.components:
            baseGlyph = g.font[c.baseGlyph]
            levels = getNestingLevels(baseGlyph, levels)
    return levels

def findNestedComponents(font):

    if font is None:
        if verbose:
            showMessage(noFontOpen, messageMode)
        return

    nestedCount = 0

    if font is not None:
        for g in font:
            L = getNestingLevels(g)
            if L > 1:
                print(g.name, L)
                nestedCount += 1

    if nestedCount == 0:
        print('no nested components found.\n')


if __name__ == '__main__':

    findNestedComponents(CurrentFont())
