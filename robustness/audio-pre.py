import math
import numpy as np
import wave
from scipy.io import wavfile

a = [0, 1, 1, 1, 1]
b = [0, 1, 1, 1, 1]


# 计算平均值
def mean(x):
    return sum(x) / len(x)


# 计算每一项数据与均值的差
def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]


# 辅助计算函数 dot product 、sum_of_squares
def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))


def sum_of_squares(v):
    return dot(v, v)


# 方差
def variance(x):
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)


# 标准差
def standard_deviation(x):
    return math.sqrt(variance(x))


# 协方差
def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)


# 相关系数
def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else:
        return 0


# print(a)
# print(b)
# print(standard_deviation(a))
# print(standard_deviation(b))
# print(correlation(a, b))
samplerate_wm, data_wm = wavfile.read("dct-extract/piano_3s.wav")
samplerate_10, data_10 = wavfile.read("dct-extract/db_ext.wav")
print(np.shape(data_wm))
print(np.shape(data_10))
d1 = data_wm[:, 0]
d2 = data_wm[:, 1]
d1 = np.transpose(d1)
d2 = np.transpose(d2)
d3 = data_10[:, 0]
d4 = data_10[:, 1]
d3 = np.transpose(d3)
d4 = np.transpose(d4)
print(correlation(d1, d3))
print(correlation(d2, d4))
