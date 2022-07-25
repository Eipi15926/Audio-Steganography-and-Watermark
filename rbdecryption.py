import numpy as np
import pywt
from scipy.io import wavfile
from PIL import Image
import struct
from matplotlib import pyplot as plt

#create a bit space to set secret information
def lb_decryption(imgarr):
    col = imgarr[0]
    row = imgarr[1]
    cnt = 2
    grayimg = np.zeros((100,100))
    for i in range(0,100):
        for j in range(0,100):
            grayimg[i,j]=imgarr[cnt]
            cnt = cnt + 1
    plt.imsave('rbreveal.jpg', grayimg)
    img = Image.open('watermark.jpg')  # 读取图片
    img = img.convert('L')  # 灰度化
    imgarray = np.array(img)
    print("imgarray",imgarray)
    im = Image.open('watermark.jpg').convert('L').save('graymrk.png')
    # 使用matplotlib读取图像然后保存为numpy中的数组
    colorimg = np.array(plt.imread('watermark.jpg'))
    print("colorimg", colorimg)
    print("grayimg", grayimg)


samplerate, dataleft = wavfile.read('tbd_compress.wav')
t = np.arange(len(dataleft)) / float(samplerate)  # Getting Time
tmp = max(dataleft)
print(dataleft)
# dataleft = dataleft / max(dataleft)  # Normalize Audio Data
# print(dataleft)
coeffs = pywt.wavedec(dataleft, 'haar', mode='sym', level=2)  # DWT
cA2, cD2, cD1 = coeffs
print("cD2", cD2)


imgarr = cD2.astype("int16")
secretarr = lb_decryption(imgarr)
# get the changed array:
# print(secretarr)
