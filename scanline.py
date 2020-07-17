import miscutils
import cv2 as cv
import numpy as np
rowNum = 200
SEGMENTS = 3

im1 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\im0.png')
im2 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\im1.png')

miscutils.colorGraph(im1, im2, rowNum)

scanline1 = im1[rowNum:rowNum+1,:]
scanline2 = im2[rowNum:rowNum+1,:]
#^^ is the :rowNum+1 necessary? ^^
length = int(scanline1.shape[1]/SEGMENTS)
#aligns segments of first scanline to entire second scanline
for i in range(length, scanline1.shape[1]+1, length):
    segment = scanline1[:,i - length:i]
    res = cv.matchTemplate(segment, scanline2, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    print(i)
    print(max_loc)
    #offset = max_loc[0] - int(length/2)
    #print(offset)
