import png, array

reader = png.Reader(filename='sword.png')

w, h, pixels, metadata = reader.read()

pix = list(pixels)

print pix[0]
