from PIL import Image
from math import cos, pi
import sys


def DCT(temp8):
    S = []
    for v in range(8):
        heng = []
        for u in range(8):
            Cu = Cv = 1
            if ~v:
                Cv = 2**(-0.5)
            if ~u:
                Cu = 2**(-0.5)
            t = 0
            for y in range(8):
                for x in range(8):
                    t += temp8[x][y] * cos((2 * x + 1) * v * pi / 16) * cos((2 * y + 1) * u * pi / 16)
            heng.append(0.25 * Cu * Cv * t)
        S.append(heng)
    return S


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


def my_print(temp, result_file):
    for i in range(8):
        for j in range(8):
            result_file.write(str(temp[i][j]) + " ")
        result_file.write("\n")
    result_file.write("\n")


LHTable = [[16, 11, 10, 16, 24, 40, 51, 61],
           [12, 12, 14, 19, 26, 58, 60, 55, ],
           [14, 13, 16, 24, 40, 57, 69, 56, ],
           [14, 17, 22, 29, 51, 87, 80, 62, ],
           [18, 22, 37, 56, 68, 109, 103, 77],
           [24, 35, 55, 64, 81, 104, 113, 92],
           [49, 64, 78, 87, 103, 121, 120, 101],
           [72, 92, 95, 98, 112, 100, 103, 99], ]


def information_hide(picture, secret, result_filename):
    im = Image.open(picture)
    result_file = open(result_filename, "w")

    # 将密语的每个字符，变为8位的二进制ASCII码
    Bsecret = []
    for letter in secret:
        bstring = '{:0>8}'.format(bin(ord(letter))[2:])
        for x in bstring:
            Bsecret.append(int(x))
    secret_index = 0
    secret_len = len(Bsecret)

    stop_flag = False  # 标志是否已经将密语全部隐写

    width = im.size[0]
    height = im.size[1]
    source = im.copy().load()
    for i in range(8, width - width % 8 - 8, 8):
        for j in range(0, height - height % 8 - 8, 8):
            temp = []
            for x in range(8):
                heng = []
                for y in range(8):
                    heng.append(source[i + x, j + y])
                temp.append(tuple(heng))
            temp = DCT(temp)
            for x in range(8):
                for y in range(8):
                    temp[x][y] = round(temp[x][y] / LHTable[x][y])
                    if not stop_flag:
                        if temp[x][y] not in (0, 1, -1):
                            temp[x][y] = YinXie(temp[x][y], Bsecret[secret_index])
                            secret_index += 1
                            if secret_index == secret_len:
                                stop_flag = True
            my_print(temp, result_file)

    result_file.close()


if __name__ == "__main__":
    secret = "I love you!"
    if len(sys.argv) == 1:
        print("未指定信息载体图片。")
    elif len(sys.argv) == 2:
        picture = sys.argv[1]
        result_filename = "result.txt"
        information_hide(picture, secret, result_filename)
    elif len(sys.argv) == 3:
        picture = sys.argv[1]
        result_filename = sys.argv[2]
        information_hide(picture, secret, result_filename)
    else:
        print("输入的参数过多。")
