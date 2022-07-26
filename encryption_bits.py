import numpy as np
import pywt
from scipy.io import wavfile
from PIL import Image

# watermark-image-size:
col = 100
row = 100
# wavelet function type:
dwttype = 'bior5.5'

def img_bit_arr():
    img = Image.open('watermark.jpg')  # read the image
    img = img.convert('L')  # an array of integer ranging from 0 to 255
    imgarray = np.array(img)
    retarray = []
    print("imgarray", imgarray)
    retarray.append(col)
    retarray.append(row)
    for i in range(0,col):
        for j in range(0, row):
            for k in range(0, 8):
                retarray.append((imgarray[i, j]&(2**k))>>k)
    print("secretarrlen=",len(retarray),'\n')
    return retarray

tms = 2
#create a bit space to set secret information
def lb_encryption(fltarr, bitarr):
    lenbr = len(bitarr)
    for i in range (0, lenbr):
        if(bitarr[i]>0):
            fltarr[i*tms] = 100
        else:
            fltarr[i*tms] = 10
    return fltarr

# read the primary wav file:
samplerate, dataleft = wavfile.read('test.wav')
print(dataleft.dtype)# the wav type must be int16
# print("left sound channel ", dataleft)
print("dataleft", dataleft)
coeffs = pywt.wavedec(dataleft, dwttype, mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
print("coeffs",coeffs)

#create secret array:
secretarr = img_bit_arr()
print(secretarr)
cD2 = lb_encryption(cD2,secretarr)
print("cD2len",len(cD2))
print("cD2", cD2)
# get the changed array:
coeffs = cA2, cD2, cD1
newwavarr = pywt.waverec(coeffs, dwttype, mode='sym')
# print("dataleft", dataleft)
print("newwavarr", newwavarr)
newwavarr = newwavarr.astype("int16")
print(newwavarr.dtype)
wavfile.write('testbits.wav', samplerate, newwavarr)
print("succeed in hiding watermark in the audio")