import argparse
from PIL import Image


def YinXie(origin, info):
    if origin % 2 == 0:
        if info == 0:
            return origin
        elif info == 1:
            return origin + 1
    else:
        if info == 1:
            return origin
        elif info == 0:
            return origin - 1


def LSB(picture, sec):
    with open(sec, "rb") as f:
        info = f.read()  # [:20]
        global alllen
        alllen = len(info)
        b = bin(int(info.hex(), 16))[2:]
        print(info[:30])
    global blen
    blen = len(b)
    print(blen)
    index = 0
    im = Image.open(picture)
    out = im.copy()
    source = out.load()
    width = im.size[0]
    height = im.size[1]
    for i in range(0, width):
        for j in range(0, height):
            if index < blen:
                source[i, j] = YinXie(source[i, j], int(b[index]))
                index += 1
    out.save("out.bmp")


if __name__ == '__main__':
    LSB("huidu.bmp", "HideInfo.bmp")
    bs = []
    ll = 0
    im = Image.open("out.bmp")
    source = im.load()
    width = im.size[0]
    height = im.size[1]
    for i in range(0, width):
        for j in range(0, height):
            if ll < blen:
                bs.append(str(source[i, j] % 2))
                ll += 1

    b = "".join(bs)
    # print(len(b))
    # print(int(b, 2).to_bytes(alllen, byteorder='big')[:30])
    with open("H2.bmp", "wb") as f:
        f.write(int(b, 2).to_bytes(alllen, byteorder='big'))
