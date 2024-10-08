mm = 2.834645669291
pt = 0.3527777777778

def mm2pt(mm):
    '''
    Converts a value in millimeters to PostScript points.

    Args:
        mm (float): A value in millimeters.

    Returns:
        The correspondent value in points.

    ::

        >>> from hTools3.modules.units import mm2pt
        >>> mm2pt(10)
        28.34645669291339

    '''
    return mm * 72 / 25.4

def pt2mm(pt):
    '''
    Converts a value in PostScript points to millimeters.

    Args:
        pt (float): A value in points.

    Returns:
        The correspondent value in millimeters.

    ::

        >>> from hTools3.modules.units import pt2mm
        >>> pt2mm(10)
        35.27777777777778

    '''
    return 25.4 * pt / 72

def mm2inch(mm):
    '''
    Converts a value in millimeters to inches.

    Args:
        mm (float): A value in millimeters.

    Returns:
        The correspondent value in inches.

    :: 

        >>> from hTools3.modules.units import mm2inch
        >>> mm2inch(10)
        3.9370000000000003

    '''

    return mm * 0.03937

def inch2mm(inch):
    '''
    Converts a value in inches to millimeters.

    Args:
        inch (float): A value in inches.

    Returns:
        The correspondent value in millimeters.

    :: 

        >>> from hTools3.modules.units import mm2inch
        >>> inch2mm(10)
        254.0

    '''
    return inch * 25.4

def scale2pt(font, scale):
    return font.info.unitsPerEm * scale

def pt2scale(font, pt):
    '''
    Calculates a scaling factor to set a source font at a given point size.

    Args:
        font (RFont): A font object.
        pt (float): The point size.

    Returns:
        A scaling factor as a float.

    ::

        from hTools3.modules.units import pt2scale

        size('A4Landscape')

        f = CurrentFont()
        s = pt2scale(f, 320)

        scale(s)
        translate(0, -f.info.descender)

        for char in 'abcd':
            g = f[char]
            drawGlyph(g)
            translate(g.width, 0)

    '''
    return pt / float(font.info.unitsPerEm)

def gridfit(pos, grid):
    '''
    Round a position to a given grid size.

    Args:
        pos (tuple): A position as a tuple of (x,y) values.
        grid (int): The grid size.

    Returns:
        A new gridfitted position as a tuple of (x,y) values.

    '''
    x, y = pos
    x = int((x // grid) * grid)
    y = int((y // grid) * grid)
    return x, y
