import numpy as np
import pywt
from scipy.io import wavfile
from PIL import Image
import struct

def img_bit_arr():
    img = Image.open('watermark.jpg')  # 读取图片
    img = img.convert('L')  # 灰度化
    col,row = img.size  # 图像大小
    imgarray = np.array(img)

    retarray = []
    for k in range(0, 8):
        retarray.append((col&(2**k))>>k)
        retarray.append((row&(2**k))>>k)

    for i in range(0, row):
        for j in range(0, col):
            for k in range(0, 8):
                retarray.append((imgarray[i, j]&(2**k))>>k)
    print("secretarrlen=",len(retarray),'\n')
    return retarray


def encrpbyte(pe, be):
    return be

#create a bit space in primary array and then put secret bits in it:
def lb_encryption(parr, bitarr):
    lenbr = len(bitarr)
    # for i in range (0, lenbr):
    for i in range(0, 5):
        parr[i] = encrpbyte(parr[i],bitarr[i])
    return parr

# read the primary wav file:
samplerate, data = wavfile.read('test.wav')
# separate left sound channel and right sound channel:
dataleft = []
dataright = []
for elements in data:
    dataleft.append(elements[0])
    dataright.append(elements[1])
print("left soundd channel ", dataleft)
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)
# dataleft = dataleft / max(dataleft)  # Normalize Audio Data
# print(dataleft)
coeffs = pywt.wavedec(dataleft, 'haar', mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
print("coeffs",coeffs)
#create secret array:
# secretarr = img_bit_arr()
# print(secretarr)
# cD2 = lb_encryption(cD2,secretarr)
# print("cD2", cD2)
# get the changed array:
# coeffs = cA2, cD2, cD1
# newwavarr = pywt.waverec(coeffs, 'haar', mode='sym')
# change array into wav:
# print("newwavarr", newwavarr)
# wavfile.write('tbd.wav', samplerate, newwavarr)
