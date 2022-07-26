import wave
import matplotlib.pyplot as plt
import numpy as np

def draw_time(path,filename):
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

draw_time("testbits.wav","wpy_noise")