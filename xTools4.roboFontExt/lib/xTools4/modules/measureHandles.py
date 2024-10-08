from math import *

'''
1. DOES NOT WORK WITH QUADRATIC CONTOURS
2. SEGMENT LENGTH SHOULD ALSO WORK WITH CURVES

- TO-DO: rewrite using points instead of bPoints?

'''

BEZIER_ARC_CIRCLE = 0.5522847498


def vector(point, angle, distance):
    '''
    Calculate a new position using vector origin, angle and length.

    Args:
        point (tuple): The origin position as a tuple of (x,y) values
        angle (float or int): The angle of the vector (in degrees).
        distance (float or int): The length of the vector.

    Returns:
        A new position as a tuple of (x,y) values.

    '''
    x, y = point
    x += cos(radians(angle)) * distance
    y += sin(radians(angle)) * distance
    return x, y

def getVector(point1, point2):
    '''
    Get the distance and angle between two points.

    Args:
        point1 (tuple): A position as a tuple of (x,y) values.
        point2 (tuple): Another position as a tuple of (x,y) values.

    Returns:
        A tuple with the distance and angle (in degrees) between the points.

    '''
    x1, y1 = point1
    x2, y2 = point2
    a = x2 - x1
    b = y2 - y1
    distance = sqrt(a ** 2 + b ** 2)
    if a != 0:
        angleRadians = atan(float(b) / a)
        angleDegrees = degrees(angleRadians)
    else:
        angleDegrees = 0
    return distance, angleDegrees

def isSelected(bPoint):
    '''
    Check if one or both handles of a bezier point are selected.

    Args:
        bPoint (bPoint): A Bezier point.

    Returns:
        A tuple of boolean values representing the selection state of incoming and outcoming handles.

    '''
    bcpInX  = bPoint.anchor[0] + bPoint.bcpIn[0]
    bcpInY  = bPoint.anchor[1] + bPoint.bcpIn[1]
    bcpOutX = bPoint.anchor[0] + bPoint.bcpOut[0]
    bcpOutY = bPoint.anchor[1] + bPoint.bcpOut[1]

    bcpInSelected  = False
    bcpOutSelected = False

    for pt in bPoint.contour.points:

        if (pt.x == bcpInX and pt.y == bcpInY):
            if pt.selected:
                bcpInSelected = True
                break

        if (pt.x == bcpOutX and pt.y == bcpOutY):
            if pt.selected:
                bcpOutSelected = True
                break

    return bcpInSelected, bcpOutSelected

def getPositions(bPoint):
    '''
    Get positions and handle lengths for a bPoint.

    Args:
        bPoint (RBPoint): A Bezier on-curve point.

    '''
    x0, y0 = bPoint.anchor

    w1, h1 = bPoint.bcpIn
    x1, y1 = x0 + w1, y0 + h1

    w2, h2 = bPoint.bcpOut
    x2, y2 = x0 + w2, y0 + h2

    return (x0, y0), (w1, h1), (w2, h2), (x1, y1), (x2, y2)


class MeasureHandles(object):

    '''
    An object to draw measurements for the handles of a (cubic) BezierPath.

    '''

    boxDraw             = True
    boxColor            = 1, 0, 0, 0.65
    boxCaptionDraw      = True
    boxCaptionColor     = 1, 0, 0

    handlesDraw         = True
    handlesColor        = 0, 0, 1, 0.65
    handlesCaptionDraw  = True
    handlesCaptionColor = 0, 0, 1

    angleDraw           = True
    angleColor          = 0, 1, 0, 0.65
    angleCaptionDraw    = True
    angleCaptionColor   = 0, 1, 0
    angleRadius         = 0.3

    selectionOnly       = True
    strokeWidth         = 1
    strokeDash          = 2

    captionFontSize     = 11
    captionFont         = "Menlo-Bold"
    captionShadow       = ((20, 20), 20, (1, 0, 0)) # offset, blur, color

    bcpData = []

    def __init__(self, ctx):
        '''
        Initialize the measurement object.

        Args:
            ctx (module): A drawing context (``drawBot`` or ``mojo.drawingTools``).

        .. code-block:: python

            import drawBot
            from hTools3.modules.measureHandles import MeasureHandles

            parameters = {
                'angleDraw'           : True,
                'angleColor'          : (1, 0, 0, 0.4),
                'angleCaptionDraw'    : True,
                'angleCaptionColor'   : (1, 0, 0),
                'handlesDraw'         : True,
                'handlesColor'        : (0, 0, 1, 0.4),
                'handlesCaptionDraw'  : True,
                'handlesCaptionColor' : (0, 0, 1),
                'boxDraw'             : True,
                'boxColor'            : (0, 1, 0, 0.4),
                'boxCaptionDraw'      : True,
                'boxCaptionColor'     : (0, 1, 0),
                'selectionOnly'       : False,
                'strokeDash'          : 0,
                'strokeWidth'         : 2,
                'captionFont'         : 'RoboType-Mono',
                'captionFontSize'     : 7,
            }

            font  = CurrentFont()
            glyph = font['s']
            s = 1.4

            fill(None)
            strokeWidth(5)
            stroke(0.8)
            translate(100, 100)
            scale(s)
            drawGlyph(glyph)

            M = MeasureHandles(drawBot)
            M.setParameters(parameters)
            M.draw(glyph)

        '''
        self.ctx = ctx

    def setParameters(self, parameters):
        '''
        Set object attributes from a parameters dictionary.

        Args:
            parameters (dict): A dictionary of attribute names and values.

        '''
        for attr, value in parameters.items():
            setattr(self, attr, value)

    def drawHandles(self, scale, bcpIn=True, bcpOut=True):
        '''
        Draw handles for Bezier path.

        '''
        (x0, y0), (w1, h1), (w2, h2), (x1, y1), (x2, y2) = self.bcpData

        sw = self.strokeWidth * scale * self.strokeDash

        if self.handlesDraw:

            self.ctx.save()
            self.ctx.fill(None)
            self.ctx.stroke(*self.handlesColor)
            self.ctx.strokeWidth(self.strokeWidth * scale)
            self.ctx.lineDash(sw, sw)

            if bcpIn and w1 != 0 or h1 != 0:
                self.ctx.line((x0, y0), (x1, y1))

            if bcpOut and w2 != 0 or h2 != 0:
                self.ctx.line((x0, y0), (x2, y2))

            self.ctx.restore()

        if self.handlesCaptionDraw and (bcpIn or bcpOut):

            self.ctx.save()
            self.ctx.stroke(None)
            self.ctx.fill(*self.handlesCaptionColor)

            if self.captionShadow is not None:
                shadowOffset, shadowBlur, shadowColor = self.captionShadow
                # self.ctx.shadow(shadowOffset, blur=shadowBlur, color=shadowColor)
                pass

            if bcpIn and (w1 != 0 or h1 != 0):
                d1 = sqrt(w1 ** 2 + h1 ** 2)
                d1_caption = '%.2f' % d1 if d1 % 1 else str(int(d1))
                d1_w, d1_h = self.ctx.textSize(d1_caption)
                d1_x = x0 + (w1 * 0.5) - (d1_w * 0.5)
                d1_y = y0 + (h1 * 0.5) - (d1_h * 0.4)
                self.ctx.textBox(d1_caption, (d1_x, d1_y, d1_w, d1_h), align='center')

            if bcpOut and (w2 != 0 or h2 != 0):
                d2 = sqrt(w2 * w2 + h2 * h2)
                d2_caption = '%.2f' % d2 if d2 % 1 else str(int(d2))
                d2_w, d2_h = self.ctx.textSize(d2_caption)
                d2_x = x0 + (w2 * 0.5) - (d2_w * 0.5)
                d2_y = y0 + (h2 * 0.5) - (d2_h * 0.4)
                self.ctx.textBox(d2_caption, (d2_x, d2_y, d2_w, d2_h), align='center')

            self.ctx.restore()

    def drawBox(self, scale, bcpIn=True, bcpOut=True):
        '''
        Draw vertical and horizontal projections for angled handles.

        '''
        (x0, y0), (w1, h1), (w2, h2), (x1, y1), (x2, y2) = self.bcpData

        sw = self.strokeDash * scale

        self.ctx.save()

        if bcpIn and (int(w1) != 0 and int(h1) != 0):

            if self.boxDraw:
                self.ctx.fill(None)
                self.ctx.stroke(*self.boxColor)
                self.ctx.strokeWidth(self.strokeWidth * scale)
                self.ctx.lineDash(sw, sw)
                self.ctx.rect(x0, y0, w1, h1)

            if self.boxCaptionDraw:
                self.ctx.stroke(None)
                self.ctx.fill(*self.boxCaptionColor)

                x1_caption = '%.2f' % abs(w1) if w1 % 1 else str(int(abs(w1)))
                x1_w, x1_h = self.ctx.textSize(x1_caption)
                x1_x = x0 + (w1 * 0.5) - (x1_w * 0.5)
                x1_y = y1 - x1_h * 0.4
                self.ctx.textBox(x1_caption, (x1_x, x1_y, x1_w, x1_h), align='center')

                y1_caption = '%.2f' % abs(h1) if h1 % 1 else str(int(abs(h1)))
                y1_w, y1_h = self.ctx.textSize(y1_caption)
                y1_x = x1 - (y1_w * 0.5)
                y1_y = y0 + (h1 * 0.5) - (y1_h * 0.4)
                self.ctx.textBox(y1_caption, (y1_x, y1_y, y1_w, y1_h), align='center')

        if bcpOut and (int(w2) != 0 and int(h2) != 0):

            if self.boxDraw:
                self.ctx.fill(None)
                self.ctx.stroke(*self.boxColor)
                self.ctx.strokeWidth(self.strokeWidth * scale)
                self.ctx.lineDash(sw, sw)
                self.ctx.rect(x0, y0, w2, h2)

            if self.boxCaptionDraw:
                self.ctx.stroke(None)
                self.ctx.fill(*self.boxCaptionColor)

                x2_caption = '%.2f' % abs(w2) if w2 % 1 else str(int(abs(w2)))
                x2_w, x2_h = self.ctx.textSize(x2_caption)
                x2_x = x0 + (w2 * 0.5) - (x2_w * 0.5)
                x2_y = y2 - x2_h * 0.4
                self.ctx.textBox(x2_caption, (x2_x, x2_y, x2_w, x2_h), align='center')

                y2_caption = '%.2f' % abs(h2) if h2 % 1 else str(int(abs(h2)))
                y2_w, y2_h = self.ctx.textSize(y2_caption)
                y2_x = x2 - (y2_w * 0.5)
                y2_y = y0 + (h2 * 0.5) - (y2_h * 0.4)
                self.ctx.textBox(y2_caption, (y2_x, y2_y, y2_w, y2_h), align='center')

        self.ctx.restore()

    def drawAngles(self, scale, bcpIn=True, bcpOut=True):
        '''
        Draw angle measurements for angled handles.

        '''
        origin, dist1, dist2, pos1, pos2 = self.bcpData

        x0, y0 = origin
        w1, h1 = dist1
        w2, h2 = dist2
        x1, y1 = pos1
        x2, y2 = pos2

        f  = BEZIER_ARC_CIRCLE
        sw = self.strokeWidth * scale * self.strokeDash

        self.ctx.save()

        if bcpIn and not int(w1) == 0 and not int(h1) == 0:

            handleLength, angle = getVector((x0, y0), (x1, y1))

            r  = handleLength * self.angleRadius
            a1 = angle % 90
            a2 = 90 - a1

            if w1 > 0 and h1 > 0:
                x3, y3 = vector((x0, y0), angle - a1 * 0.5, r)
                x4, y4 = vector((x0, y0), angle + a2 * 0.5, r)
                p1_x, p1_y = x0 + r, y0
                p2_x, p2_y = x0, y0 + r
                p3_x, p3_y = p1_x, p1_y + r * f
                p4_x, p4_y = p2_x + r * f, p2_y

            elif w1 > 0 and h1 < 0:
                x3, y3 = vector((x0, y0), angle - a1 * 0.5, r)
                x4, y4 = vector((x0, y0), angle + a2 * 0.5, r)
                p1_x, p1_y = x0 + r, y0
                p2_x, p2_y = x0, y0 - r
                p3_x, p3_y = p1_x, p1_y - r * f
                p4_x, p4_y = p2_x + r * f, p2_y

            elif w1 < 0 and h1 < 0:
                x3, y3 = vector((x0, y0), 180 + angle - a1 * 0.5, r)
                x4, y4 = vector((x0, y0), 180 + angle + a2 * 0.5, r)
                p2_x, p2_y = x0 - r, y0
                p1_x, p1_y = x0, y0 - r
                p3_x, p3_y = p1_x - r * f, p1_y
                p4_x, p4_y = p2_x, p2_y - r * f

            else:
                x3, y3 = vector((x0, y0), 180 + angle - a1 * 0.5, r)
                x4, y4 = vector((x0, y0), 180 + angle + a2 * 0.5, r)
                p1_x, p1_y = x0 - r, y0
                p2_x, p2_y = x0, y0 + r
                p3_x, p3_y = p1_x, p1_y + r * f
                p4_x, p4_y = p2_x - r * f, p2_y

            if self.angleDraw:
                self.ctx.fill(None)
                self.ctx.stroke(*self.angleColor)
                self.ctx.strokeWidth(self.strokeWidth * scale)
                self.ctx.lineDash(sw, sw)
                self.ctx.newPath()
                self.ctx.moveTo((p1_x, p1_y))
                self.ctx.curveTo((p3_x, p3_y), (p4_x, p4_y), (p2_x, p2_y))
                self.ctx.drawPath()

                if not self.boxDraw:
                    self.ctx.newPath()
                    self.ctx.moveTo((p1_x, p1_y))
                    self.ctx.lineTo((x0, y0))
                    self.ctx.lineTo((p2_x, p2_y))
                    self.ctx.drawPath()

            if self.angleCaptionDraw:
                self.ctx.stroke(None)
                self.ctx.fill(*self.angleCaptionColor)

                caption_a1 = '%.2f°' % abs(a1) if a1 % 1 else str(int(abs(a1)))
                a1_w, a1_h = self.ctx.textSize(caption_a1)
                a1_x = x3 - (a1_w * 0.5)
                a1_y = y3 - (a1_h * 0.4)
                self.ctx.textBox(caption_a1, (a1_x, a1_y, a1_w, a1_h), align='center')

                caption_a2 = '%.2f°' % abs(a2) if a2 % 1 else str(int(abs(a2)))
                a2_w, a2_h = self.ctx.textSize(caption_a2)
                a2_x = x4 - (a2_w * 0.5)
                a2_y = y4 - (a2_h * 0.5)
                self.ctx.textBox(caption_a2, (a2_x, a2_y, a2_w, a2_h), align='center')

        if bcpOut and not int(w2) == 0 and not int(h2) == 0:

            handleLength, angle = getVector((x0, y0), (x2, y2))

            r  = handleLength * self.angleRadius
            a1 = angle % 90
            a2 = 90 - a1

            if w2 > 0 and h2 > 0:
                x5, y5 = vector((x0, y0), angle - a1 * 0.5, r)
                x6, y6 = vector((x0, y0), angle + a2 * 0.5, r)
                p1_x, p1_y = x0 + r, y0
                p2_x, p2_y = x0, y0 + r
                p3_x, p3_y = p1_x, p1_y + r * f
                p4_x, p4_y = p2_x + r * f, p2_y

            elif w2 > 0 and h2 < 0:
                x5, y5 = vector((x0, y0), angle - a1 * 0.5, r)
                x6, y6 = vector((x0, y0), angle + a2 * 0.5, r)
                p1_x, p1_y = x0, y0 - r
                p2_x, p2_y = x0 + r, y0
                p3_x, p3_y = p1_x + r * f, p1_y
                p4_x, p4_y = p2_x, p2_y - r * f

            elif w2 < 0 and h2 < 0:
                x5, y5 = vector((x0, y0), 180 + angle - a1 * 0.5, r)
                x6, y6 = vector((x0, y0), 180 + angle + a2 * 0.5, r)
                p1_x, p1_y = x0 - r, y0
                p2_x, p2_y = x0, y0 - r
                p3_x, p3_y = p1_x, p1_y - r * f
                p4_x, p4_y = p2_x - r * f, p2_y

            else:
                x5, y5 = vector((x0, y0), 180 + angle - a1 * 0.5, r)
                x6, y6 = vector((x0, y0), 180 + angle + a2 * 0.5, r)
                p1_x, p1_y = x0 - r, y0
                p2_x, p2_y = x0, y0 + r
                p3_x, p3_y = p1_x, p1_y + r * f
                p4_x, p4_y = p2_x - r * f, p2_y

            if self.angleDraw:
                self.ctx.fill(None)
                self.ctx.stroke(*self.angleColor)
                self.ctx.strokeWidth(self.strokeWidth * scale)
                self.ctx.lineDash(sw, sw)
                self.ctx.newPath()
                self.ctx.moveTo((p1_x, p1_y))
                self.ctx.curveTo((p3_x, p3_y), (p4_x, p4_y), (p2_x, p2_y))
                self.ctx.drawPath()

                if not self.boxDraw:
                    self.ctx.newPath()
                    self.ctx.moveTo((p1_x, p1_y))
                    self.ctx.lineTo((x0, y0))
                    self.ctx.lineTo((p2_x, p2_y))
                    self.ctx.drawPath()

            if self.angleCaptionDraw:
                self.ctx.stroke(None)
                self.ctx.fill(*self.angleCaptionColor)

                caption_a1 = '%.2f°' % a1
                a1_w, a1_h = self.ctx.textSize(caption_a1)
                a1_x = x5 - (a1_w * 0.5)
                a1_y = y5 - (a1_h * 0.4)
                self.ctx.textBox(caption_a1, (a1_x, a1_y, a1_w, a1_h), align='center')

                caption_a2 = '%.2f°' % a2
                a2_w, a2_h = self.ctx.textSize(caption_a2)
                a2_x = x6 - (a2_w * 0.5)
                a2_y = y6 - (a2_h * 0.5)
                self.ctx.textBox(caption_a2, (a2_x, a2_y, a2_w, a2_h), align='center')

        self.ctx.restore()

    def draw(self, glyph, scale=1.0):
        '''
        Draw measurements for Bezier path.

        Args:
            glyph (RGlyph): A glyph object.
            scale (float or int): The scale factor for the drawing.

        '''
        if not glyph:
            return

        self.ctx.save()
        self.ctx.fontSize(self.captionFontSize * scale)
        self.ctx.font(self.captionFont)

        for contour in glyph:
            for bPoint in contour.bPoints:

                if self.selectionOnly:
                    if bPoint.selected:
                        bcpInSelected = bcpOutSelected = True
                    else:
                        bcpInSelected, bcpOutSelected = isSelected(bPoint)

                    if self.selectionOnly and not (bcpInSelected or bcpOutSelected):
                        continue
                else:
                    bcpInSelected = bcpOutSelected = True

                self.bcpData = getPositions(bPoint)

                self.drawBox(scale, bcpIn=bcpInSelected, bcpOut=bcpOutSelected)
                self.drawHandles(scale, bcpIn=bcpInSelected, bcpOut=bcpOutSelected)
                self.drawAngles(scale, bcpIn=bcpInSelected, bcpOut=bcpOutSelected)

        self.ctx.restore()

class MeasureSegmentsMaker:

    positions = []
    lengths   = []
    angles    = []

    def buildLineSegment(self, segment):

        p1, p2 = segment

        d, a = getVector((p1.x, p1.y), (p2.x, p2.y))

        lengthCaption = f'{d:.2f}' if d % 1 else f'{int(d)}'
        angleCaption  = f'{abs(a):.2f}°' if a % 1 else f'{int(abs(a))}°'

        x = p1.x + (p2.x - p1.x) * 0.5
        y = p1.y + (p2.y - p1.y) * 0.5

        return (x, y), lengthCaption, angleCaption

    def build(self, glyph):

        if not glyph:
            return

        self.positions = []
        self.lengths   = []
        self.angles    = []

        for contour in glyph:
            for i, segment in enumerate(contour):

                if i == 0:
                    pt1 = contour[-1][-1]
                pt2 = segment[-1]

                if len(segment) == 1:
                    position, length, angle = self.buildLineSegment((pt1, pt2))
                    self.positions.append([position])
                    self.lengths.append([length])
                    self.angles.append([angle])

                pt1 = pt2

class MeasureHandlesMaker:

    positions = []
    lengths   = []
    angles    = []

    def buildBPoint(self, bPoint, bcpIn=True, bcpOut=True):

        (x0, y0), (w1, h1), (w2, h2), (x1, y1), (x2, y2) = getPositions(bPoint)

        positions = []
        lengths   = []
        angles    = []

        if bcpIn and (w1 != 0 or h1 != 0):

            handleLength, angle = getVector((x0, y0), (x1, y1))

            a1 = angle
            d1 = sqrt(w1 ** 2 + h1 ** 2)

            d1_caption = f'{d1:.2f}' if d1 % 1 else f'{int(d1)}'
            a1_caption = f'{abs(a1):.2f}°' if a1 % 1 else f'{int(abs(a1))}°'

            d1_x = x0 + (w1 * 0.5)
            d1_y = y0 + (h1 * 0.5)

            positions.append((d1_x, d1_y))
            lengths.append(d1_caption)
            angles.append(a1_caption)

        if bcpOut and (w2 != 0 or h2 != 0):

            handleLength, angle = getVector((x0, y0), (x2, y2))

            a2 = angle
            d2 = sqrt(w2 ** 2 + h2 ** 2)

            d2_caption = f'{d2:.2f}' if d2 % 1 else f'{int(d2)}'
            a2_caption = f'{abs(a2):.2f}°' if a2 % 1 else f'{int(abs(a2))}°'

            d2_x = x0 + (w2 * 0.5)
            d2_y = y0 + (h2 * 0.5)

            positions.append((d2_x, d2_y))
            lengths.append(d2_caption)
            angles.append(a2_caption)

        return positions, lengths, angles

    def build(self, glyph):

        if not glyph:
            return

        self.positions = []
        self.lengths   = []
        self.angles    = []

        for contour in glyph:
            for bPoint in contour.bPoints:
                position, length, angle = self.buildBPoint(bPoint)
                self.positions.append(position)
                self.lengths.append(length)
                self.angles.append(angle)
