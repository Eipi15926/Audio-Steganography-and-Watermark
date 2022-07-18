import numpy as np
import pywt
from scipy.io import wavfile

def flt_to_int(arrayname):
    retarr = []
    for elements in arrayname:
        retarr.append(int(elements))
    return retarr


def insert(wavarr,secarr):
    return (wavarr+secarr)
# read the primary wav file:
samplerate, dataleft = wavfile.read('test.wav')
print(dataleft)
print("len=",len(dataleft))
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)

dataleft = dataleft / max(dataleft)  # Normalize Audio Data
coeffs = pywt.wavedec(dataleft, 'bior6.8', mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
print("cD2[0]=", cD2[0])
bytearr = bytes(cD2[0])
print(bytearr)
print("byte", int(bytearr[len(bytearr)-1]))

import struct
tst = struct.pack("<f", -1.6065048e-08)
print(tst)
# -> 'c99cdc60'
numbit = struct.unpack("<f", tst)

print(numbit[0] + 1)
# -> '60dc9cc9'

#create secret array:
secretarr = []

for elements in cD2:
    secretarr.append(1)
cofeffs=insert(cD2,secretarr)
# get the changed array:
newwavarr = pywt.waverec(coeffs, 'bior6.8', mode='sym')
# change array into wav:
wavfile.write('sampleR.wav', samplerate, newwavarr)
