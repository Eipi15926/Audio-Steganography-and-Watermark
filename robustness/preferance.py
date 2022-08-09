from skimage.metrics import peak_signal_noise_ratio as psnr
from PIL import Image
import numpy as np
import cv2


def psnr_(x, y):
    im1 = np.array(Image.open(x))
    im2 = np.array(Image.open(y))
    print(psnr(im1, im2))


def ncc(x, y):
    img1 = cv2.imread(x)
    img2 = cv2.imread(y)
    print(np.mean(np.multiply((img1-np.mean(img1)),
          (img2-np.mean(img2))))/(np.std(img1)*np.std(img2)))


if __name__ == "__main__":
    # img1 = 'dwt/watermark.jpg'
    # img2 = 'dwt/dwt.jpg'
    # img3 = 'dwt/dwt+.jpg'
    # ncc(img1, img2)
    # ncc(img1, img3)
    # print("DWT-LSB")
    img1 = 'cut/reveal-cut_from_back/original.png'
    img2 = 'cut/reveal-cut_from_back/reveal_cut50.jpg'
    img3 = 'cut/reveal-cut_from_back/reveal_cut62.5.jpg'
    img4 = 'cut/reveal-cut_from_back/reveal_cut75.jpg'
    img5 = 'cut/reveal-cut_from_back/reveal_cut87.5.jpg'
    # img6 = 'cg_v/reveal-db-bits/reveal_bits-db+4.jpg'
    # img7 = 'cg_v/reveal-db-bits/reveal_bits-db+6.jpg'
    # img8 = 'reveal-bits-snr/reveal_bits-snr100.jpg'
    # img9 = 'reveal-bits-snr/reveal_bits-snr150.jpg'
    # psnr_(img1, img2)
    ncc(img1, img2)
    ncc(img1, img3)
    ncc(img1, img4)
    ncc(img1, img5)
    # ncc(img1, img6)
    # ncc(img1, img7)
    # ncc(img1, img8)
    # ncc(img1, img9)
    # print("DWT")
    # img1 = 'cg_v/reveal-db/original.jpg'
    # img2 = 'cg_v/reveal-db/reveal_db-2.jpg'
    # img3 = 'cg_v/reveal-db/reveal_db-4.jpg'
    # img4 = 'cg_v/reveal-db/reveal_db-6.jpg'
    # img5 = 'cg_v/reveal-db/reveal_db+2.jpg'
    # img6 = 'cg_v/reveal-db/reveal_db+4.jpg'
    # img7 = 'cg_v/reveal-db/reveal_db+6.jpg'
    # img8 = 'reveal-snr/reveal-snr100.jpg'
    # img9 = 'reveal-snr/reveal-snr150.jpg'
    # psnr_(img1, img2)
    # ncc(img1, img2)
    # ncc(img1, img3)
    # ncc(img1, img4)
    # ncc(img1, img5)
    # ncc(img1, img6)
    # ncc(img1, img7)
    # ncc(img1, img8)
    # ncc(img1, img9)
