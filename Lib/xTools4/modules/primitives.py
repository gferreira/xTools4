'''
Helpers for drawing basic geometric shapes with a pen.

'''

#: A constant for drawing circular arcs with beziers.
BEZIER_ARC_CIRCLE = 0.5522847493

def rect(pen, x, y, w, h):
    '''
    Draw a rectangle with a pen object.

    '''
    pen.moveTo((x, y))
    pen.lineTo((x, y + h))
    pen.lineTo((x + w, y + h))
    pen.lineTo((x + w, y))
    pen.closePath()

def oval(pen, x, y, w, h):
    '''
    Draw an oval with a pen object.

    '''
    rx = w * 0.5
    ry = h * 0.5
    bcpx = BEZIER_ARC_CIRCLE * rx
    bcpy = BEZIER_ARC_CIRCLE * ry
    x += rx
    y += ry
    pen.moveTo((x, y + ry))
    pen.curveTo((x + bcpx, y + ry), (x + rx, y + bcpy), (x + rx, y))
    pen.curveTo((x + rx, y - bcpy), (x + bcpx, y - ry), (x, y - ry))
    pen.curveTo((x - bcpx, y - ry), (x - rx, y - bcpy), (x - rx, y))
    pen.curveTo((x - rx, y + bcpy), (x - bcpx, y + ry), (x, y + ry))
    pen.closePath()

def polygon(pen, points, close=True):
    '''
    Draw a polygon with a pen object.

    '''
    for i, pt in enumerate(points):
        if i == 0:
            pen.moveTo(pt)
        else:
            pen.lineTo(pt)
    if close:
        pen.closePath()
    else:
        pen.endPath()

def element(pen, x, y, w, h, ratio=BEZIER_ARC_CIRCLE):
    '''
    Draw an element with a pen object.

    '''
    rx = w * 0.5
    ry = h * 0.5
    bcpx = ratio * rx
    bcpy = ratio * ry
    x += rx
    y += ry
    pen.moveTo((x, y + ry))
    pen.curveTo((x + bcpx, y + ry), (x + rx, y + bcpy), (x + rx, y))
    pen.curveTo((x + rx, y - bcpy), (x + bcpx, y - ry), (x, y - ry))
    pen.curveTo((x - bcpx, y - ry), (x - rx, y - bcpy), (x - rx, y))
    pen.curveTo((x - rx, y + bcpy), (x - bcpx, y + ry), (x, y + ry))
    pen.closePath()

def roundedRect(pen, x, y, w, h, radius, ratio=BEZIER_ARC_CIRCLE):
    r = radius
    d = r * ratio
    pen.moveTo((x, y + h - r))
    pen.curveTo((x, y + h - d), (x + d, y + h), (x + r,  y + h))
    pen.lineTo((x + w - r, y + h))
    pen.curveTo((x + w - d, y + h), (x + w, y + h - d), (x + w, y + h - r))
    pen.lineTo((x + w, y + r))
    pen.curveTo((x + w, y + d), (x + w - d, y), (x + w - r, y))
    pen.lineTo((x + r, y))
    pen.curveTo((x + d, y), (x, y + d), (x, y + r))
    pen.closePath()

#---------------
# drawing tools
#---------------

def drawRectInGlyph(glyph, x, y, w, h):
    '''
    Draw a rectangle in a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        x (int or float): Horizontal position.
        y (int or float): Vertical position.
        w (int or float): The width of the rectangle.
        h (int or float): The height of the rectangle.

    ::

        g = CurrentGlyph()
        drawRectInGlyph(g, 50, 100, 120, 120)

    '''
    pen = glyph.getPen()
    rect(pen, x, y, w, h)

def drawOvalInGlyph(glyph, x, y, w, h):
    '''
    Draw an oval in a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        x (int or float): Horizontal position.
        y (int or float): Vertical position.
        w (int or float): The width of the rectangle.
        h (int or float): The height of the rectangle.

    ::

        g = CurrentGlyph()
        drawOvalInGlyph(g, 50, 100, 120, 120)

    '''
    pen = glyph.getPen()
    oval(pen, x, y, w, h)

def drawElementInGlyph(glyph, x, y, w, h, ratio=BEZIER_ARC_CIRCLE):
    '''
    Draw an element inside a glyph.

    Args:
        glyph (RGlyph): A glyph object.
        x (int or float): Horizontal position.
        y (int or float): Vertical position.
        w (int or float): The width of the rectangle.
        h (int or float): The height of the rectangle.
        ratio (float): The ratio of the handle lengths in relation to width or height.

    ::

        g = CurrentGlyph()
        drawElementInGlyph(g, 50, 100, 120, 120, ratio=0.75)

    '''
    pen = glyph.getPen()
    element(pen, x, y, w, h, ratio)

def drawRoundedRectInGlyph(glyph, x, y, w, h, radius, ratio=BEZIER_ARC_CIRCLE):
    pen = glyph.getPen()
    roundedRect(pen, x, y, w, h, radius, ratio=ratio)

def addGlyphDrawingTools(RGlyph):
    '''
    Adds drawing methods to RGlyph objects.

    Args:
        RGlyph (RGlyph): The environment’s RGlyph object.

    Call ``addGlyphDrawingTools`` once to add drawing methods to the ``RGlyph`` object::

        from mojo.roboFont import RGlyph
        addGlyphDrawingTools(RGlyph)

    After that it becomes possible to draw shapes in a glyph directly::

        g = CurrentGlyph()
        g.rect(0, 0, 80, 80)
        g.oval(80, 80, 90, 90)
        g.element(170, 170, 100, 100, ratio=0.85)

    '''
    RGlyph.rect        = drawRectInGlyph
    RGlyph.oval        = drawOvalInGlyph
    RGlyph.element     = drawElementInGlyph
    RGlyph.roundedRect = drawRoundedRectInGlyph

#---------
# testing
#---------

if __name__ == '__main__':

    from mojo.roboFont import RGlyph

    addGlyphDrawingTools(RGlyph)

    g = CurrentGlyph()
    g.clear()
    g.rect(0, 0, 100, 100)
    g.oval(100, 100, 100, 100)
    g.element(200, 200, 100, 100, ratio=0.85)
    g.roundedRect(300, 300, 100, 100, 20, ratio=0.85)
