#!/usr/bin/env python3

import png  # PyPNG: https://github.com/drj11/pypng  doc: https://pythonhosted.org/pypng/index.html

png_reader = png.Reader("alice_shocked.png")
width, height, pixels, metadata = png_reader.read()

palette = metadata['palette']

out_pixels = []
for row in pixels:
    out_row = []
    for pixel in row:
        r, g, b = palette[pixel]

        out_row.insert(0, r)
        out_row.insert(1, g)
        out_row.insert(2, b)

    out_pixels.append(out_row)

png_writer = png.Writer(width=width, height=height)
out_file = open("out.png", "wb")
png_writer.write(out_file, out_pixels)
out_file.close()
