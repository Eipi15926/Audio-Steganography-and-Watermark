import numpy as np
from PIL import Image


def test():
    img = Image.open('watermark.jpg')  # 读取图片
    img = img.convert('L')  # 灰度化

    cols, rows = img.size  # 图像大小
    print("cols=",cols,"rows=",rows)
    Value = [[0] * cols for i in range(rows)]  # 创建一个大小与图片相同的二维数组

    img_array = np.array(img)
#    print(img_array)
#    print('\n')

    for x in range(0, rows):
        for y in range(0, cols):
            Value[x][y] = img_array[x, y]  # 存入数组
    print(Value)


if __name__ == '__main__':
    test()
