import argparse
from PIL import Image
import os


def YinXie(origin, info):
        # 负责隐写的函数，如向4（0000 0100）中隐写1，则等于5。 函数中origin相当于4，info相当于1
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


def LSB(picture, sec, percent):
        # LSB隐写函数，picture是要隐写的图片，sec是隐写内容的文件，percent是隐写的比例
    percent = int(percent)
    with open(sec, "rb") as f:  # 以二进制格式读取文件
        info = f.read()
        # alllen = len(info)
        b = bin(int(info.hex(), 16))[2:]  # 将文件内容从bytes转为01字符串
    blen = len(b)
    index = 0
    im = Image.open(picture)  # 打开图片
    out = im.copy()
    source = out.load()
    width = im.size[0]
    height = im.size[1]

    # 判断隐写的内容是否足够支撑隐写率（事实上我准备的隐写内容是一张图片，全部隐写之后也只能达到93%的隐写率）
    if width * height * percent / 100 >= blen:
        Hlen = blen
        percent = round(Hlen / (width * height) * 100)
    else:
        Hlen = width * height * percent / 100

    for i in range(0, width):
        for j in range(0, height):
            if index < Hlen:
                source[i, j] = YinXie(source[i, j], int(b[index]))  # 对每个像素进行隐写
                index += 1
    out.save(os.path.join("out", "out%d.bmp" % percent))  # 将隐写之后的图片保存到out文件夹下
    print("bitlen:%d\thide percent:%s%%" % (Hlen, percent))  # byteslen:%d\t


def recover(picture, blen, byteslen):
        # LSB隐写的提取函数，最好不讲
    bs = []
    ll = 0
    im = Image.open(picture)
    source = im.load()
    width = im.size[0]
    height = im.size[1]
    for i in range(0, width):
        for j in range(0, height):
            if ll < blen:
                bs.append(str(source[i, j] % 2))
                ll += 1

    b = "".join(bs)
    with open("recover.bmp", "wb") as f:
        f.write(int(b, 2).to_bytes(byteslen, byteorder='big'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LSB")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--hide", "-H", help='hide infomation', action="store_true")
    group.add_argument("--recover", "-R", help='recover infomation', action="store_true")
    parser.add_argument("--picture", "-p")
    parser.add_argument("--secret_picture", "-s")
    parser.add_argument("--percent", "-c")
    args = parser.parse_args()
    if args.hide:
        LSB(args.picture, args.secret_picture, args.percent)
    elif args.recover:
        recover(args.picture, 1928143, 241018)
