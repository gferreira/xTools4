import os

imgs = ['/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.30.23.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.30.27.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 19.04.28.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 19.04.32.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.31.27.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.31.32.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.32.25.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.32.28.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.33.34.png', '/hipertipo/tools/_extensions/hTools3/docs/images/glyph/_temp/Screen Shot 2021-05-15 at 18.33.38.png']

x, y = 690, 89

for i, img in enumerate(imgs):
    if i%2:
        continue
    imgPalette = imgs[i+1]
    print(img)
    print(imgPalette)
    print()

    w, h = imageSize(img)
    newPage(w, h)
    fill(1)
    rect(0, 0, w, h)
    image(img, (0, 0))
    image(imgPalette, (x, y))


dstFolder = '/hipertipo/tools/_extensions/hTools3/docs/images/glyph'
dstPath = os.path.join(dstFolder, 'display-options_preview.png')
saveImage(dstPath, multipage=True)
