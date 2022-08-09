from skimage.metrics import peak_signal_noise_ratio as psnr
from PIL import Image
import numpy as np
import cv2


def psnr_(x, y):
    img1 = np.array(Image.open(x))
    img2 = np.array(Image.open(y))
    print(psnr(img1, img2))


def ncc(x, y):
    img1 = cv2.imread(x)
    img2 = cv2.imread(y)
    print(np.mean(np.multiply((img1-np.mean(img1)),
          (img2-np.mean(img2))))/(np.std(img1)*np.std(img2)))


if __name__ == "__main__":
    img1 = 'piano_3s.jpg'
    img2 = 'compress_ext.jpg'
    # psnr_(img1, img2)
    ncc(img1, img2)
