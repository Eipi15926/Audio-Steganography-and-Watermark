"""
添加高斯噪声, 参考https://pythontechworld.com/article/detail/hMfygc6PlBy4
"""
import soundfile as sf
import math
import librosa
import numpy as np


def add_noise(audio_path, noise_path,out_path, SNR, sr=44100):
    src, sr = librosa.core.load(audio_path, sr=sr)   # 读取浮点语音序列和采样率
    random = np.random.rand(len(src))   # 产生与音频等长的[0,1)均匀分布序列
    Ps = np.sum(src ** 2) / len(src)   # 语音信号功率Ps
    Pn1 = np.sum(random ** 2) / len(random)   # 噪声功率Pn1

    k=math.sqrt(Ps/(10**(SNR/10)*Pn1))
    random_values=random * k   # 噪声序列
    Pn=np.sum(random_values**2)/len(random_values)   # 噪声功率Pn

    snr=10*math.log10(Ps/Pn)   # 信噪比
    print("当前信噪比：", snr)


    sf.write(noise_path, random_values, sr)   # 噪声写入文件
    outdata = src + random_values   # 添加噪声后的音频
    sf.write(out_path, outdata, sr)   # 添加噪声后的音频写入文件


def main():
    origin_au = 'testbits.wav'
    out_au = 'testbits_noise.wav'
    # origin_au = './music/steg.wav'
    noise = 'noise.wav'
    # out_au = './music/add_noise.wav'
    SNR = 50
    add_noise(origin_au, noise, out_au, SNR)


if __name__=="__main__":
    main()