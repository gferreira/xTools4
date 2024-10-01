'''
Tools to convert between different color models.

'''

__all__ = [
    'rgb2nscolor', 'nscolor2rgb',
    'rgb2hex',     'hex2rgb',
    'rgb2cmyk',    'cmyk2rgb',
]

# -------
# NSColor
# -------

from AppKit import NSColor

def rgb2nscolor(rgbColor):
    '''
    Convert RGB color tuple to NSColor object.

    Args:
        rgbColor (tuple): RGB color as a tuple of 1, 2, 3 or 4 values (floats between 0 and 1).

    Returns:
        A NSColor object.

    >>> rgbColor = 1, 0, 0
    >>> rgb2nscolor(rgbColor)
    NSCalibratedRGBColorSpace 1 0 0 1

    '''
    if rgbColor is None:
        return
    elif len(rgbColor) == 1:
        r = g = b = rgbColor[0]
        a = 1.0
    elif len(rgbColor) == 2:
        grey, a = rgbColor
        r = g = b = grey
    elif len(rgbColor) == 3:
        r, g, b = rgbColor
        a = 1.0
    elif len(rgbColor) == 4:
        r, g, b, a = rgbColor
    else:
        return
    nsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(r, g, b, a)
    return nsColor

def nscolor2rgb(nsColor):
    '''
    Convert from NSColor object to RGBA color tuple.

    Args:
        nsColor (NSColor): A color object.

    Returns:
        A tuple of RGBA values.

    >>> nsColor = NSColor.colorWithCalibratedRed_green_blue_alpha_(0, .5, 1, .8)
    >>> nsColorToRGB(nsColor)
    (0.0, 0.5, 1.0, 0.8)

    '''
    r = nsColor.redComponent()
    g = nsColor.greenComponent()
    b = nsColor.blueComponent()
    a = nsColor.alphaComponent()
    return r, g, b, a

# -----------
# hexadecimal
# -----------

def hex2rgb(hexColor):
    '''
    Convert hexadecimal color to RGB color tuple.

    Args:
        hexColor (str): A hexadecimal color.

    Returns:
        A tuple of RGB values.

    >>> hexColor = 'FF0099'
    >>> hexToRGB(hexColor)
    (1.0, 0.0, 0.6)

    '''
    hexColor = hexColor.lstrip('#')
    lv = len(hexColor)
    rgb = tuple()
    for i in range(0, lv, lv//3):
        rgb += (int(hexColor[i:i+lv//3], 16) / 255.0,)
    return rgb

def rgb2hex(rgbColor):
    '''
    Convert RGB color tuple to hexadecimal color.

    Args:
        rgbColor (tuple): RGB color as a tuple of 3 values.

    Returns:
        A hexadecimal color.

    >>> rgbColor = 1.0, 0.2, 0.0
    >>> RGBToHex(rgbColor)
    'ff3300'

    '''
    r, g, b = rgbColor
    r, g, b = int(r*255), int(g*255), int(b*255)
    return '%02x%02x%02x' % (r, g, b)

# -------
# process
# -------

# http://stackoverflow.com/questions/14088375/how-can-i-convert-rgb-to-cmyk-and-vice-versa-in-python

RGB_SCALE  = 1.0
CMYK_SCALE = 1.0

def rgb2cmyk(rgbColor, cmyk_scale=CMYK_SCALE, rgb_scale=RGB_SCALE):
    '''
    Convert RGB color tuple to CMYK color.

    Args:
        rgbColor (tuple): RGB color as a tuple of 3 values.

    Returns:
        A CMYK color.

    >>> rgbColor = 1.0, 0.2, 0.0
    >>> rgb2cmyk(rgbColor)
    (0.0, 0.8, 1.0, 0.0)

    '''
    if rgbColor == (0, 0, 0):
        # black
        return 0, 0, 0, cmyk_scale

    r, g, b = rgbColor

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / rgb_scale
    m = 1 - g / rgb_scale
    y = 1 - b / rgb_scale

    # extract out k [0, 1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy) / (1 - min_cmy)
    m = (m - min_cmy) / (1 - min_cmy)
    y = (y - min_cmy) / (1 - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c * cmyk_scale, m * cmyk_scale, y * cmyk_scale, k * cmyk_scale

def cmyk2rgb(cmykColor, cmyk_scale=CMYK_SCALE, rgb_scale=RGB_SCALE):
    '''
    Convert CMYK color tuple to RGB color.

    Args:
        cmykColor (tuple): CMYK color as a tuple of 4 values.

    Returns:
        A RGB color.

    >>> cmykColor = 1.0, 0.5, 0.0, 0.0
    >>> cmyk2rgb(cmykColor)
    (0.0, 0.5, 1.0)

    '''
    c, m, y, k = cmykColor

    r = rgb_scale * (1.0 - c / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    g = rgb_scale * (1.0 - m / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))
    b = rgb_scale * (1.0 - y / float(cmyk_scale)) * (1.0 - k / float(cmyk_scale))

    return r, g, b

# ----------------
# deprecated names
# ----------------

rgbToNSColor = rgb2nscolor
nsColorToRGB = nscolor2rgb
nscolor2rgba = nsColorToRGBa = nscolor2rgb
hexToRGB = hex2rgb
RGBToHex = rgb2hex

# -------
# testing
# -------

if __name__ == "__main__":

    import doctest
    doctest.testmod()

