#looks through segments of a scanline, and detects its color "spikes" and matches with the same spikes of the other scanline
#this is based off of scanline.py, might want to combine into one script later

#still working as intended, but it's still matching wrong spikes. I don't know how to fix that

import miscutils
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
rowNum = 300
SEGMENT_WIDTH = 50
MIN_DIFF = 80
SEARCH_BUFFER = 40

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
    #probably want to turn this chunk (and others) into function
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
    #
        
    diff = maxBlue - minBlue
    if diff >= MIN_DIFF:
        minPos = blues.index(minBlue) + i
        maxPos = blues.index(maxBlue) + i

        #"looking" to the left of minPos and maxPos, separately
        #
        segment2L = scanline2[minPos - SEARCH_BUFFER:minPos]
        blues2L = []
        for k in range(len(segment2L)):
            blues2L.append(segment2L[k][0])
        mins = []
        for l in range(1,len(blues2L) - 1):
            if blues2L[l] < blues2L[l - 1] and blues2L[l] < blues2L[l + 1]:
                mins.append(blues2L[l])
        if mins == []:
            continue
        minBlue2 = min(mins)
        #
        
        #
        segment2R = scanline2[maxPos - SEARCH_BUFFER:maxPos]
        blues2R = []
        for m in range(len(segment2R)):
            blues2R.append(segment2R[m][0])
        maxs = []
        for n in range(1,len(blues2R) - 1):
            if blues2R[n] > blues2R[n - 1] and blues2R[n] > blues2R[n + 1]:
                maxs.append(blues2R[n])
        if maxs == []:
            continue
        maxBlue2 = max(maxs)
        #
            
        minPos2 = blues2L.index(minBlue2)+ minPos - SEARCH_BUFFER
        maxPos2 = blues2R.index(maxBlue2)+ maxPos - SEARCH_BUFFER

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
