# Reference: https://zhuanlan.zhihu.com/p/196387205
import pathlib
from pydub import AudioSegment

input_wav_file = 'tbd.wav'
output_wav_file = 'tbd_db.wav'

snd = AudioSegment.from_wav(input_wav_file)
# 获取时长、分贝数、采样率
print(snd.duration_seconds, snd.dBFS, snd.frame_rate)
# len = snd.duration_seconds
# tms = 0.375
# 剪30秒核心片段，单位为毫秒
# snd_mid = snd[1000:len*1000]
# 调大音量，单位分贝
snd_mid = snd
snd_mid = snd_mid - 6
# 剪最后30秒片段
# snd_end = snd[-30000:]

# 加上原始信息
tags={'artist': 'DOTA', 'album': 'Cut', 'comments': 'Come to Python1024!'}
# 导出文件
snd_mid.export(output_wav_file, format='wav')