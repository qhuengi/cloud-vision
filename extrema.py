#looks through segments of a scanline, and detects its color "spikes" and matches with the same spikes of the other scanline
#this is based off of scanline.py, might want to combine into one script later

#CURRENT PROBLEM: the extremas are matching with the wrong ones... I am not sure how to fix this

import miscutils
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
rowNum = 300
SEGMENT_WIDTH = 50
MIN_DIFF = 100
SEARCH_BUFFER = 20

im1 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\a.png') #left image
im2 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\b.png') #right image

miscutils.colorGraph(im1, im2, rowNum)

im1[:,:,1] = np.zeros([im1.shape[0], im1.shape[1]])
im2[:,:,1] = np.zeros([im2.shape[0], im2.shape[1]])
im1[:,:,2] = np.zeros([im1.shape[0], im1.shape[1]])
im2[:,:,2] = np.zeros([im2.shape[0], im2.shape[1]])

scanline1 = im1[rowNum]
scanline2 = im2[rowNum]

prevX = 0
prevY = 0
for i in range(0, scanline1.shape[0] - SEGMENT_WIDTH):
    segment = scanline1[i:i + SEGMENT_WIDTH]
    blues = []
    for j in range(len(segment)):
        blues.append(segment[j][0])
        
    mins = []
    maxs = []
    for k in range(1,len(blues) - 1):
        if blues[k] > blues[k - 1] and blues[k] > blues[k + 1]:
            maxs.append(blues[k])
        elif blues[k] < blues[k - 1] and blues[k] < blues[k + 1]:
            mins.append(blues[k])
    if mins == [] or maxs == []:
        continue
    minBlue = min(mins)
    maxBlue = max(maxs)
        
    diff = maxBlue - minBlue
    if diff >= MIN_DIFF:            
        minPos = blues.index(minBlue) + i
        maxPos = blues.index(maxBlue) + i

        #"looking" to left only (the left image is the right skewed graph)
        segment2 = scanline2[i - SEARCH_BUFFER:max(i + SEGMENT_WIDTH - SEARCH_BUFFER, 0)]
        blues2 = []
        for k in range(len(segment2)):
            blues2.append(segment2[k][0])
            
        mins = []
        maxs = []
        for l in range(1,len(blues2) - 1):
            if blues2[l] > blues2[l - 1] and blues2[l] > blues2[l + 1]:
                maxs.append(blues2[l])
            elif blues2[l] < blues2[l - 1] and blues2[l] < blues2[l + 1]:
                mins.append(blues2[l])
        if mins == [] or maxs == []:
            continue
        minBlue2 = min(mins)
        maxBlue2 = max(maxs)
            
        minPos2 = blues2.index(minBlue2)+ i - SEARCH_BUFFER
        maxPos2 = blues2.index(maxBlue2)+ i - SEARCH_BUFFER

        if (minPos2 - minPos) == prevX or (maxBlue2 - maxBlue) == prevY:
            continue

        print("(" + str(minPos2 - minPos) + "," + str(maxPos2 - maxPos) + ")")
        prevX = minPos2 - minPos
        prevY = maxBlue2 - maxBlue

        plt.figure(i)
        plt.ylim(0, 255)
        plt.title("Matched min and max: " + str(i), fontdict=None, loc='center')
        plt.plot(range(0,scanline1.shape[0]), scanline1, linewidth=1, label='Left')
        plt.plot(range(0,scanline1.shape[0]), scanline2, linewidth=1, label='Right')
        plt.plot([minPos,minPos2],[minBlue,minBlue2],linewidth=2)
        plt.plot([maxPos,maxPos2],[maxBlue,maxBlue2],linewidth=2)
        plt.axvline(x=i, linestyle = '--')
        plt.axvline(x=i + SEGMENT_WIDTH, linestyle = '--')
        plt.legend()
        plt.show()
