'''
A collection of standard messages for use in xTools4 dialogs.

'''

from mojo.UI import PostBannerNotification

def showMessage(messageText, mode=0):
    '''
    Display a given message to the user.

    Args:
        mode (int): The display mode of the message. ``0``: print to console, ``1``: show banner notification

    ::
    
        from xTools4.modules.messages import showMessage
        showMessage('hello world', mode=1)

    '''
    if mode == 0:
        print(messageText)
    else:
        PostBannerNotification('xTools4', messageText)

def noXSelected(x):
    '''
    Generic message to be used when a required object is not selected.

    '''
    return f'No {x} selected.\nPlease select one or more {x}s.\n'

def noXOpen(x):
    '''
    Generic message to be used when a required object is not open.

    '''
    return f'No {x} open.\nPlease open at least one {x}.\n'

# ------
# points
# ------

#: Message to be used when no point is selected.
noPointSelected = noXSelected('point')

#: Message to be used when only one point is selected.
onlyOnePoint = 'Only one point selected.\nPlease select at least two points.\n'

#: Message to be used when at least two points must be selected.
atLeastTwoPoints = 'Please select at least two points.\n'

# --------
# contours
# --------

#: Message to be used when no contour is selected.
noContourSelected = noXSelected('contour')

# ------
# glyphs
# ------

#: Message to be used when no glyph is open.
noGlyphOpen = noXOpen('glyph')

#: Message to be used when no glyph is selected.
noGlyphSelected = noXSelected('glyph')

# ------
# layers
# ------

#: Message to be used when no layer is selected.
noLayerSelected = noXSelected('layer')

# -----
# fonts
# -----

#: Message to be used when no font is open.
noFontOpen = noXOpen('font')

#: Message to be used when at least two fonts must be open.
onlyOneFont = 'Only one font open.\nPlease open at least one more font.\n'

# ------
# folder
# ------

#: Message to be used when there are no font files in a given folder.
noFontInFolder = 'Folder does not contain a font.\nPlease add some fonts to the folder, or choose another folder.\n'
