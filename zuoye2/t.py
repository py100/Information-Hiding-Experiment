from PIL import Image
import random


def Change(zhengfu, percent):
    r = random.randrange(0, 100)
    if r > percent:
        return 0
    else:
        if zhengfu >= 0:
            return 1
        else:
            return -1


def RelationShip(bitList):
    return sum([bitList[i + 1] - bitList[i] for i in range(len(bitList) - 1)])
    # return [bitList[i + 1] - bitList[i] for i in range(len(bitList) - 1)]


# print([i for i in range(10)])
# print(RelationShip([i for i in range(10)]))
# for i in range(10):
#     print(Change(1, 80))
out = Image.open("Hide.jpg").convert("L")
out = out.resize((643, 402))
out.save("HideInfo.bmp")
