'''
Tools to work with Bezier curves.

'''

from __future__ import division
import math

def getBezierPoint(t, pt1, pt2, pt3, pt4, reverse=True):
    '''
    Use the `Bernstein Basis Function`_ to get a point in a `Bezier curve`_.

    Args:
        t (float): A float representing the ratio of the desired point.
        pt1 (tuple): The ``x,y`` coordinate of the first point (on-curve).
        pt2 (tuple): The ``x,y`` coordinate of the second point (off-curve).
        pt3 (tuple): The ``x,y`` coordinate of the third point (off-curve).
        pt4 (tuple): The ``x,y`` coordinate of the last point (on-curve).
        reverse (bool): Get point for the reverse value of ``t``.

    >>> pt1 = 320, 162
    >>> pt2 = 138, 528
    >>> pt3 = 416, 856
    >>> pt4 = 854, 794
    >>> getBezierPoint(0.5, pt1, pt2, pt3, pt4, reverse=True)
    (354.5, 638.5)

    .. _Bezier curve: https://en.wikipedia.org/wiki/B%C3%A9zier_curve
    .. _Bernstein Basis Function: https://en.wikipedia.org/wiki/Bernstein_polynomial

    '''

    def B1(t):
        return t * t * t

    def B2(t):
        return 3 * t * t * (1 - t)

    def B3(t):
        return 3 * t * (1 - t) * (1 - t)

    def B4(t):
        return (1 - t) * (1 - t) * (1 - t)

    x1, y1 = pt1
    x2, y2 = pt2
    x3, y3 = pt3
    x4, y4 = pt4

    if reverse:
        t = 1.0 - t

    x = x1 * B1(t) + x2 * B2(t) + x3 * B3(t) + x4 * B4(t)
    y = y1 * B1(t) + y2 * B2(t) + y3 * B3(t) + y4 * B4(t)

    return x, y

# --------------
# curvature comb
# --------------

# tip of the hat to Yanone's SpeedPunk:
# http://www.yanone.de/software/speedpunk/

# this implementation was translated into Python from:
# http://beta.observablehq.com/@dhotson/drawing-better-looking-curves

def lerp(p1, p2, t):
    '''
    Linear interpolation between two points.

    Args:
        p1 (Point): A Point object.
        p2 (Point): Another Point object.
        t (float): The interpolation factor.

    Returns:
        A new Point object interpolated from p1 and p2.

    '''
    return p1 * (1 - t) + p2 * t

def glyphToBezierSegments(glyph):
    '''
    Convert an RGlyph into lists of ``BezierSegment`` objects.

    '''

    contours = []
    for contour in glyph.contours:

        segments = []
        for i, segment in enumerate(contour):

            if i == 0:
                lastPt = segment[0]
                continue

            p0 = lastPt

            if len(segment) == 3:
                p1, p2, p3 = segment
                segment = BezierSegment(Point((p0.x, p0.y)), Point((p1.x, p1.y)), Point((p2.x, p2.y)), Point((p3.x, p3.y)))
                segments.append(segment)

            else:
                p1 = p0
                p2 = p3 = segment[0]

            lastPt = p3

        contours.append(segments)

    return contours

class Point:
    '''
    A basic Bezier Point object with support for math operations and normalization.

    '''

    def __init__(self, pos):
        '''
        Create a new Point object from ``x,y`` coordinates.

        Args:
            pos (tuple): A pair of ``x,y`` coordinates.

        Returns:
            A new Point object.

        >>> p = Point((100, 100))
        >>> p.x, p.y
        (100, 100)

        '''
        x, y = pos
        self.x = x
        self.y = y

    def __mul__(self, n):
        '''
        Multiply the point by a factor.

        Args:
            n (int or float): The multiplication factor.

        Returns:
            A new Point object.

        >>> p1 = Point((100, 100))
        >>> p2 = p1 * 3
        >>> p2.x, p2.y
        (300, 300)

        '''
        return Point((self.x * n, self.y * n))

    def __add__(self, p):
        '''
        Add the point to another point.

        Args:
            p (Point): Another point.

        Returns:
            A new Point object.

        >>> p1 = Point((100, 100))
        >>> p2 = Point((300, 300))
        >>> p3 = p1 + p2
        >>> p3.x, p3.y
        (400, 400)

        '''
        return Point((self.x + p.x, self.y + p.y))

    def __sub__(self, p):
        '''
        Subtract the point from another point.

        Args:
            p (Point): Another point.

        Returns:
            A new Point object.

        >>> p1 = Point((100, 100))
        >>> p2 = Point((300, 300))
        >>> p3 = p2 - p1
        >>> p3.x, p3.y
        (200, 200)
        >>> p4 = p1 - p2
        >>> p4.x, p4.y
        (-200, -200)

        '''
        return Point((self.x - p.x, self.y - p.y))

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normal(self):
        return Point((-self.y, self.x))

    def normalise(self):
        return self * (1.0 / self.mag())

class BezierSegment:
    '''
    A basic Bezier Segment object with support for point and curvature calculations.

    '''

    def __init__(self, p0, p1, p2, p3):
        '''
        Initiliaze a BezierSegment from four Points (two on-curve, two off-curve).

        Args:
            p0 (Point): The first on-curve point.
            p1 (Point): The first off-curve point.
            p2 (Point): The second off-curve point.
            p3 (Point): The second on-curve point.

        '''
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def position(self, t):
        '''
        Get a point on the curve based on a given factor.

        Args:
            t (float): A float representing the ratio of the desired point.

        Returns:
            A Point object.

        >>> p0 = Point((0, 0))
        >>> p1 = Point((0, 60))
        >>> p2 = Point((40, 100))
        >>> p3 = Point((100, 100))
        >>> B = BezierSegment(p0, p1, p2, p3)
        >>> pt = B.position(0.5)
        >>> pt.x, pt.y
        (27.5, 72.5)

        '''
        p1 = self.p0 * ((1 - t) ** 3)
        p2 = self.p1 * (3 * (1 - t) ** 2 * t)
        p3 = self.p2 * (3 * (1 - t) * t ** 2)
        p4 = self.p3 * (t ** 3)
        return p1 + p2 + p3 + p4

    def d(self, t):
        '''
        First derivative of the curve. Describes the tangent along the curve. Used to calculate the normal (line perpedincular to the curve).

        '''
        d  = (self.p1 - self.p0) * (3 * (1 - t) ** 2)
        d += (self.p2 - self.p1) * (6 * (1 - t) * t)
        d += (self.p3 - self.p2) * (3 * t ** 2)
        return d

    def dd(self, t):
        '''
        Second derivative of the curve. Describes how quickly the tangent is changing.

        '''
        dd  = self.p2 - self.p1 * 2 + self.p0
        dd *= 6 * (1 - t)
        dd += (self.p3 - self.p2 * 2 + self.p1) * 6 * t
        return dd

    def curvature(self, t):
        '''
        Calculate the segments’s curvature at a given point.

        Args:
            t (float): A float representing the ratio of the desired point.

        Returns:
            The curvature value.

        >>> p0 = Point((0, 0))
        >>> p1 = Point((0, 60))
        >>> p2 = Point((40, 100))
        >>> p3 = Point((100, 100))
        >>> B = BezierSegment(p0, p1, p2, p3)
        >>> B.curvature(0.5)
        -0.011544600509168123

        '''
        d  = self.d(t)
        dd = self.dd(t)
        return (d.x * dd.y - d.y * dd.x) / (d.x ** 2 + d.y ** 2) ** (3 / 2)


# -------
# testing
# -------

if __name__ == "__main__":

    import doctest
    doctest.testmod()
