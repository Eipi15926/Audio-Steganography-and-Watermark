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
    retarray.append(col)
    retarray.append(row)
    for i in range(0,col):
        for j in range(0, row):
            retarray.append(imgarray[i,j])
    print("secretarrlen=",len(retarray),'\n')
    return retarray


def encrpbyte(bl):
    print(bl)
    addtmp = struct.pack(">h", bl)
    print("addtmp", addtmp)
    for i in range(0,3-len(addtmp)):
        addtmp = addtmp + struct.pack(">h",0)
    print("newaddtmp",addtmp)
    newflt = struct.unpack(">f", addtmp)
    print(newflt[0])
    return newflt[0]

#create a bit space to set secret information
def lb_encryption(fltarr, bitarr):
    lenbr = len(bitarr)
    for i in range (0, lenbr):
        fltarr[i] = encrpbyte(bitarr[i])
    return fltarr

# read the primary wav file:
samplerate, dataleft = wavfile.read('test.wav')
print(dataleft)
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)
# dataleft = dataleft / max(dataleft)  # Normalize Audio Data
# print(dataleft)
coeffs = pywt.wavedec(dataleft, 'haar', mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
#create secret array:
secretarr = img_bit_arr()
print(secretarr)
cD2 = lb_encryption(cD2,secretarr)
print("cD2", cD2)
# get the changed array:
coeffs = cA2, cD2, cD1
newwavarr = pywt.waverec(coeffs, 'haar', mode='sym')
# change array into wav:
print("newwavarr", newwavarr)
wavfile.write('tbd.wav', samplerate, newwavarr)
