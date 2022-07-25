# 为音频嵌入图片水印
## 使用指南
### 环境搭建

安装Python3和如下packages（`pip install package-name`）:
- numpy 
- pywt 
- scipy
- PIL 

### 水印的嵌入程序：`encryption_cD2`
将所有需要用到的文件放在同一个文件夹下。
程序输入：
- 一张100*100的jpg图片作为要嵌入的水印
- 一个长度不少于3s的单声道wav音频

程序输出：嵌入了水印的wav音频

### 水印的提取程序：`decryption`
该程序接受一个嵌入了水印的音频作为输入，输出从音频中提取出的水印图片。
