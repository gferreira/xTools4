pdfPath = 'icon.pdf'

w, h = imageSize(pdfPath)
print(w, h)

s = 30

size(w*s, h*s)
scale(s)
image(pdfPath, (0, 0))

print(width(), height())

pngPath = pdfPath.replace('.pdf', '.png')
saveImage(pngPath)
