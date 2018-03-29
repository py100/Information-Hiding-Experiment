with open("HideInfo.bmp", "rb") as f:
    info = f.read()
    print(type(info[0:2].hex()))
