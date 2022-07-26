from pydub import AudioSegment
# 音频文件路径
path = "tbd.wav"
# 读取音频文件，设置采样率<default=44100>
song = AudioSegment.from_wav(path).set_frame_rate(44100)
# 按32k的bitrate导出文件到指定路径,这里是直接覆盖原文件
song.export("tbd_compress.wav", format='wav', bitrate='32k')
