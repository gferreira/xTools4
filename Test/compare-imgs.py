import os, glob

folder = os.getcwd()
imgsFolder = os.path.join(folder, 'images')
dialogGroups = ['glyphs', 'glyph', 'font', 'batch']

ignore = [
    'layersLock',
    'buildConstructions',
    'modifiersLayers',
    'displayOptions',
]

for dialogsGroup in dialogGroups:

    imgsFolder_hTools3 = os.path.join(imgsFolder, 'hTools3', dialogsGroup)
    imgsFolder_hTools4 = os.path.join(imgsFolder, 'hTools4', dialogsGroup)

    assert os.path.exists(imgsFolder_hTools3)
    assert os.path.exists(imgsFolder_hTools4)

    imgs_hTools4 = glob.glob(f'{imgsFolder_hTools4}/*.png')

    for imgPath in sorted(imgs_hTools4):
        dialogName = os.path.splitext(os.path.split(imgPath)[-1])[0]
        if dialogName in ignore:
            continue

        imgPath2 = imgPath.replace('images/hTools4', 'images/hTools3')

        newPage('A2Landscape')
    
        w1, h1 = imageSize(imgPath)
        image(imgPath, (0, height()-h1))

        if not os.path.exists(imgPath2):
            print(f'ERROR: {imgPath2} does not exist!')
            continue

        w2, h2 = imageSize(imgPath2)
        with savedState():
            translate(width()/2, height())
            scale(2)
            image(imgPath2, (0, -h2))

        fontSize(36)
        text(dialogName, (20, 20))


# folder = os.getcwd()
# pdfPath = os.path.join(folder, 'compare-hTools4-hTools3.pdf')
# saveImage(pdfPath)
