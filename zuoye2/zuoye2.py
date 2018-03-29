#! python3
#coding=utf8

from PIL import Image
import sys
import random


def Change(percent):
    r = random.randrange(0, 100)
    if r > percent:
        return False
    else:
        return True


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


def F(bitList, ftype, percent):
    if ftype == 0:
        return bitList
    elif ftype > 0:
        newBitList = []
        for i in bitList:
            if Change(percent):
                if i % 2 == 0:
                    newBitList.append(i + 1)
                else:
                    newBitList.append(i - 1)
            else:
                newBitList.append(i)
        return newBitList
    elif ftype < 0:
        newBitList = []
        for i in bitList:
            if Change(percent):
                if i % 2 == 0:
                    newBitList.append(i - 1)
                else:
                    newBitList.append(i + 1)
            else:
                newBitList.append(i)
        return newBitList


def Zrange(source, xindex, yindex):
    bitList = []  # 一维列表， Z字排序之后的像素值
    flag = True  # 表示Z字排序处于向右上方的趋势
    i = j = 0
    while i < 8 and j < 8:
        bitList.append(source[xindex + i, yindex + j])
        # bitList.append(source[xindex + i][yindex + j])
        if flag:
            i, j = i + 1, j - 1
            if j < 0:
                j = 0
                flag = False
            if i >= 8:
                i = 7
                j += 2
                flag = False
        else:
            i, j = i - 1, j + 1
            if i < 0:
                i = 0
                flag = True
            if j >= 8:
                j = 7
                i += 2
                flag = True
    return bitList


def RelationShip(bitList):
    return sum([bitList[i + 1] - bitList[i] for i in range(len(bitList) - 1)])


def RS(picture, bili):
    im = Image.open(picture)
    source = im.copy().load()  # 加载图片

    width = im.size[0]
    height = im.size[1]
    new_width = width - width % 8
    new_height = height - height % 8

    RmNum = SmNum = R_mNum = S_mNum = 0
    AllNum = 0
    for i in range(0, new_width - 7, 8):
        for j in range(0, new_height - 7, 8):
            AllNum += 1
            ZrangeList = Zrange(source, i, j)
            origin_rs = RelationShip(ZrangeList)
            FeiFu_rs = RelationShip(F(ZrangeList, 1, bili))
            FeiZheng_rs = RelationShip(F(ZrangeList, -1, bili))
            if FeiFu_rs >= origin_rs:
                RmNum += 1
            elif FeiFu_rs < origin_rs:
                SmNum += 1
            if FeiZheng_rs >= origin_rs:
                R_mNum += 1
            elif FeiZheng_rs < origin_rs:
                S_mNum += 1
    Rm, Sm, R_m, S_m = RmNum / AllNum, SmNum / AllNum, R_mNum / AllNum, S_mNum / AllNum
    print(Rm, R_m, Sm, S_m)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        picture = "small.bmp"
        RS(picture, 70)
        # print("未指定信息载体图片。")
    elif len(sys.argv) == 2:
        picture = sys.argv[1]
        RS(picture, 70)
    else:
        print("输入的参数过多。")
