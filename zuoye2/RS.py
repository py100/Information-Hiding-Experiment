#! python3
# coding=utf8

from PIL import Image
import sys
import random


def Change(percent):
    # 按给定的概率输出是否翻转
    r = random.randrange(0, 100)
    if r > percent:
        return False
    else:
        return True


def F(bitList, ftype, percent):
    # 翻转函数，bitlist是Z字排序之后的64个像素的像素值， ftype>0 进行非负翻转， ftype<0 进行非正翻转
    # percent是非零翻转所占的比例
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
    # Z字排序函数，source是整个图片的像素矩阵， xindex和yindex分别为正在进行Z字排序的8*8小块的左上顶点在整个矩阵中的位置
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
    # 像素相关性计算函数。
    # 原理是Z字排序之后的列表，后一项减前一项的绝对值，的累加和
    return sum([abs(bitList[i + 1] - bitList[i]) for i in range(len(bitList) - 1)])


def RS(picture, bili):
    # RS分析函数， picture为要分析的图片， bili为非零翻转所占的比例
    im = Image.open(picture)
    source = im.copy().load()  # 加载图片

    width = im.size[0]
    height = im.size[1]
    new_width = width - width % 8
    new_height = height - height % 8

    RmNum = SmNum = R_mNum = S_mNum = 0  # 初始值为零
    AllNum = 0
    for i in range(0, new_width - 7, 8):
        for j in range(0, new_height - 7, 8):
            AllNum += 1
            ZrangeList = Zrange(source, i, j)  # Z字排序
            origin_rs = RelationShip(ZrangeList)  # 初始像素相关性
            FeiFu_rs = RelationShip(F(ZrangeList, 1, bili))  # 非负翻转之后的像素相关性
            FeiZheng_rs = RelationShip(F(ZrangeList, -1, bili))  # 非正翻转之后的初始像素相关性

            if FeiFu_rs > origin_rs:
                RmNum += 1
            elif FeiFu_rs < origin_rs:
                SmNum += 1
            if FeiZheng_rs > origin_rs:
                R_mNum += 1
            elif FeiZheng_rs < origin_rs:
                S_mNum += 1
    Rm, Sm, R_m, S_m = RmNum / AllNum, SmNum / AllNum, R_mNum / AllNum, S_mNum / AllNum
    print(Rm, R_m, Sm, S_m)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        picture = sys.argv[1]
        RS(picture, int(sys.argv[2]))
    else:
        print("必须输入两个参数，图片的名称和非零翻转的比例")
