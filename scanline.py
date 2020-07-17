import miscutils
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

rowNum = 200
SEGMENTS = 10

im1 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\im0.png')
im2 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\im1.png')

miscutils.colorGraph(im1, im2, rowNum)

im1[:,:,1] = np.zeros([im1.shape[0], im1.shape[1]])
im2[:,:,1] = np.zeros([im2.shape[0], im2.shape[1]])
im1[:,:,2] = np.zeros([im1.shape[0], im1.shape[1]])
im2[:,:,2] = np.zeros([im2.shape[0], im2.shape[1]])

scanline1 = im1[rowNum]
scanline2 = im2[rowNum]
length = int(scanline1.shape[0]/SEGMENTS)
#aligns segments of first scanline to entire second scanline
for i in range(length, scanline1.shape[0]+1, length):
    segment = scanline1[i - length:i]
    res = cv.matchTemplate(segment, scanline2, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    offset = int(max_loc[1] - (i - length/2))
    print(offset)
    
    scanline1Offset = np.roll(scanline1, offset)
    plt.figure(i)
    plt.ylim(0, 255)
    plt.title("Aligned Segment: " + str(i), fontdict=None, loc='center')
    plt.plot(range(0,scanline1.shape[0]), scanline1Offset, linewidth=1, label='Left')
    plt.plot(range(0,scanline1.shape[0]), scanline2, linewidth=1, label='Right')
    plt.legend()

plt.show()
