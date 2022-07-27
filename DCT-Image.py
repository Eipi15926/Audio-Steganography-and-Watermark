import math
# import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.io import wavfile
from scipy.fftpack import dct,idct
import random

def DCT(data):
    dct_audio = dct(data,norm ='ortho')
    return dct_audio

def iDCT(data):
    idct_audio = idct(data,norm ='ortho')
    return idct_audio

def dct_embed(audio0,img,len,random):
    # print((np.asarray(audio0)).shape)
    numFrames = math.ceil(audio0.shape[0] / len)
    print(numFrames)
    numFrames = numFrames -1
    frames = list()
    for i in range(numFrames):
        frames.append(audio0[i * len: (i * len) + len])

    DCTCoeffs = np.zeros((numFrames, len))
    for i in range(numFrames):
            DCTCoeffs[i] = DCT(frames[i])

    for i in range(numFrames):
        if i == 0:
            audio = DCTCoeffs[i]
        else:
            audio = np.concatenate((audio, DCTCoeffs[i]), axis=0)

    width, height = img.size
    embedded = audio.copy()


    for i in range(width):
        for j in range(height):
            value = img.getpixel(xy=(i, j))
            value = 1 if value == 255 else 0
            x = i * height + j
            r = random[x]
            embedded[r] = setLastBit(embedded[r], value)

    return embedded

def idct_embed(audio,len):
    numFrames = math.ceil(audio.shape[0] / len)
    print(numFrames)

    frames = list()
    for i in range(numFrames):
        frames.append(audio[i * len: (i * len) + len])

    iDCTCoeffs = np.zeros((numFrames, len))
    for i in range(numFrames):
        iDCTCoeffs[i] = iDCT(frames[i])

    for i in range(numFrames):
        if i == 0:
            audio0 = iDCTCoeffs[i]
        else:
            audio0 = np.concatenate((audio0, iDCTCoeffs[i]), axis=0)

    synthesis = audio0
    return synthesis

def dct_extract(audio,len,random):
    numFrames = math.ceil(audio.shape[0] / len)
    print(numFrames)
    numFrames = numFrames - 1
    frames = list()
    for i in range(numFrames):
        frames.append(audio[i * len: (i * len) + len])

    DCTCoeffs = np.zeros((numFrames, len))
    for i in range(numFrames):
        DCTCoeffs[i] = DCT(frames[i])

    for i in range(numFrames):
        if i == 0:
            audio0 = DCTCoeffs[i]
        else:
            audio0 = np.concatenate((audio0, DCTCoeffs[i]), axis=0)


    width, heigth = (112, 112)  # sizeExtraction(joinAudio)
    image = Image.new("1", (width, heigth))

    for i in range(width):
        for j in range(heigth):
            x = i * heigth + j
            r = random[x]
            value = getLastBit(audio0[r])
            image.putpixel(xy=(i, j), value=value)

    return image


def setLastBit(number, bit):
    if type(number) in (int, np.int16, np.int64):
        return ((number >> 1) << 1) | bit #位运算符，左边最后一位归0，取并集，最后一位值为value
    elif type(number) in (float, np.float64):
        whole, dec = splitFloat(number)
        number = setLastBit(whole, bit)
        number = number + dec
        return number

def getLastBit(number):
    if type(number) in (int, np.int16, np.int64):
        return int(number % 2)
    elif type(number) in (float, np.float64):
        whole, dec = splitFloat(number)
        return getLastBit(whole)

def splitFloat(number):

    whole = int(number)
    dec = number - whole
    return whole, dec

def show_wav(wave_input_path):
    samplerate, data = wavfile.read(wave_input_path)
    plt.figure()
    plt.plot(data)
    plt.show()

if __name__ == '__main__':
    root = ".."

    resultList = random.sample(range(0, 100000), 112*112)

    frames = 100

    img2 = Image.open("lock.png")
    img = img2.convert('1')

    samplerate, data = wavfile.read("buddy_19s.wav")
    print(samplerate)

    print((np.asarray(data)).shape)

    embed_watermak_audio = dct_embed(audio0=data,img=img,len=frames,random = resultList)  # 在dct块中嵌入水印图像

    synthesis = idct_embed(audio=embed_watermak_audio,len=frames)  # idct变换得到空域图像

    print((np.asarray(synthesis)).shape)
    wavfile.write("Output.wav", samplerate, synthesis.astype(np.int16))

    # samplerate2,data2 = wavfile.read("Output1_snr150.wav")

    extract_watermark = dct_extract(audio=synthesis,len=frames,random = resultList)
    extract_watermark.save("extract_watermark.png")


    images = [img, extract_watermark]
    titles = ["Watermark", "Extract_Watermark"]
    for i in range(2):
        plt.subplot(1, 2, i + 1)
        if i % 2:
            plt.imshow(images[i], cmap=plt.cm.gray)
        else:
            plt.imshow(images[i])
        plt.title(titles[i])
        plt.axis("off")
    plt.show()

    show_wav("buddy_19s.wav")
    show_wav("Output.wav")


