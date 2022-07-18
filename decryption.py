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


def decrpbyte(flt):
    print(flt)
    tmp = struct.pack(">f",flt)
    print("tmp",tmp)
    lastbit = int(tmp[len(tmp)-1])
    print("lastbit",lastbit)
    return lastbit

#create a bit space to set secret information
def lb_decryption(fltarr):
    bitarr = []
    lenfr = len(fltarr)
    for i in range (0, 5):
        bitarr.append(decrpbyte(fltarr[i]))
    return bitarr


samplerate, dataleft = wavfile.read('tbd.wav')
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)
print(dataleft)
# dataleft = dataleft / max(dataleft)  # Normalize Audio Data
# print(dataleft)
coeffs = pywt.wavedec(dataleft, 'haar', mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
print("cD2", cD2)
secretarr = lb_decryption(cD2)
# get the changed array:
print(secretarr)
