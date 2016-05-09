#!/usr/bin/env python

# Inspired by: https://gist.github.com/sbp/3084622

import struct
import sys
import zlib


def parse(png_bytes):
    png_bytes = png_bytes[8:]  # remove signature

    while png_bytes:
        length = struct.unpack('>I', png_bytes[:4])[0]
        png_bytes = png_bytes[4:]

        chunk_type = png_bytes[:4]
        png_bytes = png_bytes[4:]

        chunk_data = png_bytes[:length]
        png_bytes = png_bytes[length:]

        crc = struct.unpack('>I', png_bytes[:4])[0]
        png_bytes = png_bytes[4:]

        yield chunk_type, chunk_data


def main():
    name = sys.argv[1]
    with open(name, 'rb') as f:
        png_bytes = f.read()

    out_file_index = 0
    for chunk_type, chunk_data in parse(png_bytes):
        if chunk_type == "zTXt":
            null_byte = chunk_data.find("\0")
            chunk_data = chunk_data[null_byte + 2:]
            uncompressed_chunk_data = zlib.decompress(chunk_data)
            with open("zTXt." + str(out_file_index) + ".txt", "wb") as f:
                f.write(uncompressed_chunk_data)
            out_file_index += 1


if __name__ == '__main__':
    main()
