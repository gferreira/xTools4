from Quartz import CoreGraphics
import AppKit
import Quartz

def imagecapture(rect=None, window=None, path=None, excludeDesktop=True, windowShadow=True):
    """
    rect: top, left, w, h
    """
    if rect is None:
        rect = CoreGraphics.CGRectInfinite
    else:
        rect = AppKit.NSMakeRect(*rect)

    imageOptions = CoreGraphics.kCGWindowImageDefault

    if window is None:
        windowID = CoreGraphics.kCGNullWindowID 
        options = CoreGraphics.kCGWindowListOptionAll
    else:
        rect = CoreGraphics.CGRectNull
        options = CoreGraphics.kCGWindowListOptionIncludingWindow
        windowID = window.windowNumber()
        if not windowShadow:
            imageOptions |= CoreGraphics.kCGWindowListOptionOnScreenOnly 
            #imageOptions |= CoreGraphics.kCGWindowImageBoundsIgnoreFraming
    
    if excludeDesktop:
        options |=  CoreGraphics.kCGWindowListExcludeDesktopElements

    print(window)
    print(windowID)
    # print(rect)

    screenshot = CoreGraphics.CGWindowListCreateImage(
        rect,
        options,
        windowID,
        imageOptions)

    # print(screenshot)
    image = AppKit.CIImage.imageWithCGImage_(screenshot)

    print(image)
    # print()

    bitmapRep = AppKit.NSBitmapImageRep.alloc().initWithCIImage_(image)
    pngData = bitmapRep.representationUsingType_properties_(AppKit.NSPNGFileType, None)
    if path:        
        pngData.writeToFile_atomically_(path, False)
    nsImage = AppKit.NSImage.alloc().initWithSize_(bitmapRep.size())
    nsImage.addRepresentation_(bitmapRep)
    return nsImage


from mojo.UI import CurrentFontWindow
window = CurrentFontWindow().window().getNSWindow()
im = imagecapture(window=window)
w, h = im.size()
newPage(w, h)
image(im, (0, 0))

from hTools3.dialogs.glyphs.move import MoveGlyphsDialog
D = MoveGlyphsDialog()
window = D.w.getNSWindow()
im = imagecapture(window=window)
w, h = im.size()
newPage(w, h)
image(im, (0, 0))

