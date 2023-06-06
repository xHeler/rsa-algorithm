def read_bmp(filename):
    with open(filename, 'rb') as f:
        bmp = f.read()
    # The header is the first 54 bytes of the BMP file
    header = bmp[:54]
    # The rest is the actual pixel data
    data = bmp[54:]
    return header, data

def write_bmp(filename, header, data):
    with open(filename, 'wb') as f:
        f.write(header + data)