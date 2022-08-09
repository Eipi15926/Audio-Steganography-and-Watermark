import re
from tkinter import W
from tkinter.filedialog import SaveFileDialog
from scipy.io import wavfile
from scipy.fftpack import dct, idct, fft, fftfreq, ifft
# import pywt
import numpy as np
import matplotlib.pyplot as plt
import wave

# Normalize data signal in int16 suitable for wav library


def normalizeForWav(data):
    return np.int16(data.real)


def draw_time(path, filename):
    f = wave.open(path, 'rb')
    params = f.getparams()
    params = f.getparams()
    # 通道数、采样字节数、采样率、采样帧数
    nchannels, sampwidth, framerate, nframes = params[:4]
    voiceStrData = f.readframes(nframes)
    waveData = np.fromstring(voiceStrData, dtype=np.short)  # 将原始字符数据转换为整数
    # 音频数据归一化
    waveData = waveData * 1.0/max(abs(waveData))
    # 将音频信号规整乘每行一路通道信号的格式，即该矩阵一行为一个通道的采样点，共nchannels行
    waveData = np.reshape(waveData, [nframes, nchannels]).T  # .T 表示转置
    f.close()

    time = np.arange(0, nframes)*(1.0/framerate)
    plt.plot(time, waveData[0, :], c='b')
    plt.xlabel('time')
    plt.ylabel('am')
    plt.savefig('./%s.jpg' % filename)
    plt.show()


def noise(data):
    noise = np.random.randint(5, len(data))
    return noise+data


class DCT_Embed(object):
    def __init__(self, background, watermark, block_size, alpha):
        # watermark = np.where(watermark0 < np.mean(watermark0),0, 1)  # watermark进行(归一化的)二值化
        # print(np.shape(background))
        # print(np.shape(watermark))
        b_h, b_w = background.shape[:2]
        w_h, w_w = watermark.shape[:2]
        assert w_h <= b_h / block_size, \
            "\r\n请确保您的的水印音频尺寸 不大于 原有音频尺寸的1/{:}\r\nbackground尺寸{:}\r\nwatermark尺寸{:}".format(
                block_size, background.shape, watermark.shape
            )

        # 块大小保存
        self.block_size = block_size
        self.block_size_y = b_w
        # 水印强度控制
        self.alpha = alpha
        # 随机序列
        self.k1 = np.random.randn(block_size)
        self.k2 = np.random.randn(block_size)

    def dct_blk(self, background):
        '''
        对background进行分块，然后进行dct变换，得到dct变换后的矩阵
        '''

        background_dct_blocks_h = background.shape[0]//self.block_size
        # background_dct_blocks_w = background.shape[1]
        background_dct_blocks = np.zeros(shape=(
            (background_dct_blocks_h,
             self.block_size, background.shape[1])
        ))  # 前2个维度用来遍历所有block，后2个维度用来存储每个block的DCT变换的值
        # 垂直方向分成background_dct_blocks_h个块
        h_data = np.vsplit(background, background_dct_blocks_h)
        for h in range(background_dct_blocks_h):
            a_block = h_data[h]
            # dct变换
            background_dct_blocks[h, ...] = dct(a_block, type=3, norm="ortho")
        return background_dct_blocks

    def dct_embed(self, dct_data, watermark):
        """_summary_
        嵌入水印到original audio的dct系数中
        Args:
            dct_data (_type_): original audio的dct系数
            watermark (_type_): 归一化二值音频数组0-1
        """
        print("--------dct_embed start-----------------")
        temp = watermark.flatten()
        # assert temp.max() == 1 and temp.min() == 0, "为方便处理，请保证输入的watermark是被二值归一化的"
        result = dct_data.copy()
        for h in range(watermark.shape[0]):
            for w in range(watermark.shape[1]):
                # k = self.k1 if watermark[h, w] == 1 else self.k2
                # 查询块(h,w)并遍历对应块的中频系数（主对角线），进行修改
                # 查询块h，并只改变对应块的一个元素
                # result[h, 0, 0] = dct_data[h, 0, 0]+self.alpha*k[0]
                for i in range(self.block_size):
                    result[h, i, self.block_size_y-1] = dct_data[h,
                                                                 i, self.block_size_y-1]+self.alpha*watermark[h][w]
        print("--------dct_embed end-----------------")
        return result

    def idct_embed(self, dct_data):
        '''
        进行对dct矩阵进行idct变换，完成从频域到空域的变换
        '''
        print("--------idct_embed start-----------------")
        row = None
        result = None
        h = dct_data.shape[0]
        for i in range(h):
            print("--------Round:", i, "-----------------")
            block = idct(dct_data[i, ...], type=3, norm="ortho")
            result = block if i == 0 else np.vstack((result, block))
        print("--------idct_embed end-----------------")
        return result

    def dct_extract(self, synthesis, watermark_size, background):
        """
        从嵌入水印的音频中提取水印
        :param synthesis: 嵌入水印的空域音频
        :param watermark_size: 水印大小
        :return: 提取的空域水印
        """
        w_h, w_w = watermark_size
        recover_watermark = np.zeros(shape=watermark_size)
        synthesis_dct_blocks = self.dct_blk(background=synthesis)
        background_dct_blocks = self.dct_blk(background=background)
        p = np.zeros(self.block_size)
        for h in range(w_h):
            for w in range(w_w):
                for k in range(self.block_size):
                    recover_watermark[h, w] = (
                        synthesis_dct_blocks[h, k, self.block_size_y-1] - background_dct_blocks[h, k, self.block_size_y-1])/self.alpha
                #     p[k] = synthesis_dct_blocks[h, k, self.block_size_y - 1]
                # if corr2(p, self.k1) > corr2(p, self.k2):
                #     recover_watermark[h, w] = 1
                # else:
                #     recover_watermark[h, w] = 0
        return recover_watermark


def mean2(x):
    y = np.sum(x) / np.size(x)
    return y


def corr2(a, b):
    """
    相关性判断
    """
    a = a - mean2(a)
    b = b - mean2(b)
    r = (a * b).sum() / np.sqrt((a * a).sum() * (b * b).sum())
    return r


if __name__ == "__main__":
    # samplerate, data = wavfile.read("piano.wav")
    # dctData = dct(data, type=3, norm="ortho")
    # # print(dctData, np.shape(dctData))
    # dctData = noise(dctData)
    # idctData = idct(dctData, type=3, norm="ortho")
    # # print("idctData == dctData?", idctData == dctData)
    # idctData = normalizeForWav(idctData)
    # wavfile.write("piano_dct.wav", samplerate, idctData)
    # draw_time("piano.wav")
    # draw_time("piano_dct.wav")

    alpha = 0.1
    block_size = 4
    # 1.数据读取
    samplerate_wm, data_wm = wavfile.read("piano_3s.wav")
    # data_wm = np.where(data_wm < np.mean(data_wm),0, 1)  # watermark进行(归一化的)二值化
    samplerate_bg, data_bg = wavfile.read("buddy_19s.wav")
    if((np.shape(data_bg)[0] % block_size) != 0):
        data_bg = np.r_[data_bg, np.zeros(
            block_size-(np.shape(data_bg)[0] % block_size))]
    if(data_bg.ndim == 1):
        a = np.array(np.zeros(data_bg.shape[0])).T
        data_bg = np.c_[np.array([data_bg]).T, a]
    print(np.shape(data_wm), np.shape(data_bg))

    # 2.dct
    dct_embed = DCT_Embed(background=data_bg, watermark=data_wm,
                          block_size=block_size, alpha=alpha)
    # background_dct_blocks = dct_embed.dct_blk(background=data_bg)
    # # print(np.shape(background_dct_blocks))
    # embed_wm_blocks = dct_embed.dct_embed(
    #     dct_data=background_dct_blocks, watermark=data_wm)
    # synthesis = dct_embed.idct_embed(dct_data=embed_wm_blocks)
    # data = normalizeForWav(synthesis)
    # wavfile.write("piano_dct.wav", samplerate_bg, data)

    # # samplerate0, data0 = wavfile.read("buddy_19s.wav")
    # # print(np.shape(data0))
    # # samplerate, data = wavfile.read("piano_dct.wav")
    # # print(np.shape(data))
    # # data = data[:, 0]
    # # print(np.shape(data))
    # # print(data0, data)
    # # wavfile.write("piano_dct.wav", samplerate, data)
    # draw_time("piano_3s.wav","piano_3s")
    # draw_time("buddy_19s.wav","buddy_19s")
    # draw_time("piano_dct.wav","piano_dct")

    # 3.提取水印
    samplerate_syn, data_syn = wavfile.read("bunny_compress.wav")
    if((np.shape(data_syn)[0] % block_size) != 0):
        data_syn = np.r_[data_syn, np.zeros(
            block_size-(np.shape(data_syn)[0] % block_size))]
    if(data_syn.ndim == 1):
        a = np.array(np.zeros(data_syn.shape[0])).T
        data_syn = np.c_[np.array([data_syn]).T, a]
    print(np.shape(data_syn))
    extract_watermark = dct_embed.dct_extract(
        synthesis=data_syn, watermark_size=data_wm.shape, background=data_bg)
    data = normalizeForWav(extract_watermark)
    wavfile.write("compress_ext.wav", samplerate_wm, data)
    draw_time("piano_3s.wav", "piano_3s")
    draw_time("compress_ext.wav", "compress_ext")
