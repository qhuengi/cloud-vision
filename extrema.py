#looks through segments of a scanline, and detects its color "spikes" and matches with the same spikes of the other scanline
#this is based off of scanline.py, might want to combine into one script later

#CURRENT PROBLEMS: don't want to include 1. connections that are obviously wrong, 2. detecting min/max at non-"tips" of curves. that part is wip.
#this is all so spaghetti

import miscutils
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
rowNum = 300
SEGMENT_WIDTH = 50
MIN_DIFF = 130
SEARCH_BUFFER = 5

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
    minBlue = min(blues)
    maxBlue = max(blues)
    '''
    #min cannot be at the edges of segment; only at the "tip" of a curve
    if (blues.index(minBlue) == 0 or blues.index(minBlue) + 1 == len(blues)):
        mins = []
        prev = blues[0]
        for i in range(1,len(blues)):
            blue = blues[i]
            if blue > prev:
                mins.append(prev)
            prev = blue
        minBlue = min(mins)
    if (blues.index(maxBlue) == 0 or blues.index(maxBlue) + 1 == len(blues)):
        maxs = []
        prev = blues[0]
        for i in range(1,len(blues)):
            blue = blues[i]
            if blue < prev:
                maxs.append(prev)
            prev = blue
        maxBlue = max(maxs)
    '''
        
    diff = maxBlue - minBlue
    if diff >= MIN_DIFF:            
        minPos = blues.index(minBlue) + i
        maxPos = blues.index(maxBlue) + i

        #"looking" to left only (the left image is the right skewed graph)
        segment2 = scanline2[i - SEARCH_BUFFER:max(i + SEGMENT_WIDTH - SEARCH_BUFFER, 0)]
        blues2 = []
        for k in range(len(segment2)):
            blues2.append(segment2[k][0])
        minBlue2 = min(blues2)
        maxBlue2 = max(blues2)
        
        '''
        if (blues2.index(minBlue2) == 0 or blues2.index(minBlue2) + 1 == len(blues2)):
            mins = []
            prev = blues2[0]
            for i in range(1,len(blues2)):
                blue = blues2[i]
                if blue > prev:
                    mins.append(prev)
                prev = blue
            minBlue2 = min(mins)
        if (blues2.index(maxBlue2) == 0 or blues2.index(maxBlue2) + 1 == len(blues2)):
            maxs = []
            prev = blues2[0]
            for i in range(1,len(blues2)):
                blue = blues2[i]
                if blue < prev:
                    maxs.append(prev)
                prev = blue
            maxBlue2 = max(maxs)
        '''
            
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
        plt.legend()
        plt.show()
