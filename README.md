# Audio steganography and a picture watermark embedded in the audio using DWT/DWT-LSB
## Project profile

**This is a project of SWS3011, DOTA Defence of the ancient, finished by Group 4.**

We apply several audio-watermark algorithm, I'm responsible for the DWT part and make some progress to combine DWT and LSB together as a new method.

This project writes a certain size gray scale map into audio as watermark, which has certain practical significance in the field of copyright protection.
## Guides
### The environment to build

Please install Python3 and the following packages（`pip install package-name`）:
- numpy 
- pywt 
- scipy
- PIL 

### Embedding program for watermarking：`encryption`
Please put all the required files under the same folder.
This program inputs：

- a 100*100 jpg image as the watermark to be embedded
- a mono wav file whose length is more than 10 seconds

and outputs an audio with watermark.

### The extraction procedure for the watermarking was performed：`decryption`
The program accepts an embedded watermark audio as input and outputs the watermark picture extracted from the audio.

### Robustness detection folder：`robustness`
The robustness tests provided are：

- The noise is added to the audio at a given sampling rate at a certain signal to noise ratio

- Change the volume
- Cut audio