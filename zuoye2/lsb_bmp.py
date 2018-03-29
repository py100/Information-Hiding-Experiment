#! python3
#coding=utf8

from PIL import Image
import random

def lsb_hide(f, ratio):
    im = Image.open(f)
    height, width = im.size
    lsb_bit = int(width*height*ratio/100.0)
    pixs = im.load()
    # for i in range(lsb_bit):
    for i in range(lsb_bit):
        d = random.randint(0,1)
        if pixs[i/width, i%width] != d:
            im.putpixel([i//width, i%width], pixs[i/width, i%width]^1)
    im.save(f.split('.')[0] + str(ratio) + '.bmp');
    print ('ratio', ratio, 'saved')

def main():
    source = 'Hide.bmp'
    for i in range(100):
        lsb_hide(source, i)

if __name__=='__main__':
    main()
