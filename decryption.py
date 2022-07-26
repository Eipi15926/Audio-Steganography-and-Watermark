import numpy as np
import pywt
from scipy.io import wavfile
from matplotlib import pyplot as plt
dwttype = 'bior5.5'

#create a bit space to set secret information
def lb_decryption(imgarr):
    cnt = 2
    grayimg = np.zeros((100,100))
    for i in range(0,100):
        for j in range(0,100):
            grayimg[i,j]=imgarr[cnt*10]
            cnt = cnt + 1
    # print("grayimg",grayimg)
    plt.imsave('reveal.jpg', grayimg)
    tmpimg = np.array(plt.imread('reveal.jpg'))
    print("tmpimg", tmpimg)
    for i in range(0,100):
        for j in range(0,100):
            tmpimg[i,j]=[grayimg[i,j],grayimg[i,j],grayimg[i,j]]
    plt.imsave('reveal.jpg',tmpimg)



samplerate, dataleft = wavfile.read('tbd.wav')
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)
print("dataleft", dataleft)
# dataleft = dataleft / max(dataleft)  # Normalize Audio Data
# print(dataleft)
coeffs = pywt.wavedec(dataleft, dwttype, mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
print("cD2", cD2)
imgarr = cD2.astype("int16")
secretarr = lb_decryption(imgarr)
# get the changed array:
# print(secretarr)
