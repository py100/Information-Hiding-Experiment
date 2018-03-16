from PIL import Image
from math import cos, pi
import sys


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
    source = im.copy().load()  # 加载图片

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
    new_width = width - width % 8
    new_height = height - height % 8

    new_Source = [[0 * x * i for x in range(new_height)] for i in range(new_width)]  # 创建新矩阵
    result_file.write("%d %d\n" % (new_width, new_height))

    for i in range(0, new_width - 8, 8):
        for j in range(0, new_height - 8, 8):

            # 对每个小块儿进行DCT变换和量化处理
            for v in range(8):
                for u in range(8):

                    # DCT变换
                    Cu = Cv = 1
                    if not v:
                        Cv = 2**(-0.5)
                    if not u:
                        Cu = 2**(-0.5)
                    t = 0
                    for y in range(8):
                        for x in range(8):
                            t += source[i + y, j + x] * cos((2 * x + 1) * u * pi / 16) * cos((2 * y + 1) * v * pi / 16)
                    t = 0.25 * Cu * Cv * t

                    # 量化
                    t = round(t / LHTable[v][u])

                    # 隐写
                    if not stop_flag:
                        if t not in {0, 1, -1}:
                            t = YinXie(t, Bsecret[secret_index])
                            secret_index += 1
                            if secret_index == secret_len:
                                stop_flag = True

                    # 计算之后的值放入新矩阵
                    new_Source[i + v][j + u] = t

    for i in range(new_height):
        for j in range(new_width):
            result_file.write("%d " % new_Source[j][i])
        result_file.write("\n")

    result_file.close()


if __name__ == "__main__":
    secret = "I love you!"
    if len(sys.argv) == 1:
        picture = "small.bmp"
        result_filename = "result.txt"
        information_hide(picture, secret, result_filename)
        # print("未指定信息载体图片。")
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
