import os
from pydub import AudioSegment
import numpy as np
import pywt
from scipy.io import wavfile
from PIL import Image
from matplotlib import pyplot as plt
# 音频文件路径
path = "tbd.wav"
# 读取音频文件，设置采样率<default=44100>
song = AudioSegment.from_wav(path).set_frame_rate(22050)
# 按32k的bitrate导出文件到指定路径,这里是直接覆盖原文件
song.export("tbd_compress.wav", format='wav', bitrate='32k')


sampleRate, Data = wavfile.read('tbd_compress.wav')  # 获取采样率和音频数据

newRate = 44100
wavfile.write('new_name.wav', newRate, Data.astype(np.int16))  # 重新写入新的采样率音频文件
