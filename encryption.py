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


def encrpbyte(flt, bl):
    # print(flt)
    tmp = struct.pack(">f",flt)
    # print("tmp",tmp)
    lastbit = int(tmp[len(tmp)-1])
    # print("lastint", lastbit)
    lastbit = lastbit ^ 1 + bl
    # print("translastint", lastbit)
    newtmp = tmp[0:(len(tmp)-1)]
    # print("newtmp",newtmp)
    addtmp = struct.pack(">h", lastbit)
    # print("addtmp", addtmp)
    atp = addtmp[len(addtmp)-1:len(addtmp)]
    # print(atp)
    newtmp = newtmp + atp
    # print(atp)
    # print("newtmp",newtmp)
    newflt = struct.unpack(">f", newtmp)
    # print(newflt[0])
    return newflt[0]

#create a bit space to set secret information
def lb_encryption(fltarr, bitarr):
    lenbr = len(bitarr)
    for i in range (0, lenbr):
        fltarr[i] = encrpbyte(fltarr[i],bitarr[i])
    return fltarr

# read the primary wav file:
samplerate, dataleft = wavfile.read('test.wav')
print(dataleft)
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)
# dataleft = dataleft / max(dataleft)  # Normalize Audio Data
# print(dataleft)
coeffs = pywt.wavedec(dataleft, 'bior6.8', mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
#create secret array:
secretarr = img_bit_arr()
print(secretarr)
cD2 = lb_encryption(cD2,secretarr)
print("cD2", cD2)
# get the changed array:
coeffs = cA2, cD2, cD1
newwavarr = pywt.waverec(coeffs, 'bior6.8', mode='sym')
# change array into wav:
print("newwavarr", newwavarr)
wavfile.write('tbd.wav', samplerate, newwavarr)
