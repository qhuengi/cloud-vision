#looks through segments of a scanline, and detects its color "spikes" and matches with the same spikes of the other scanline
#this is based off of scanline.py, might want to combine into one script later
import miscutils
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
rowNum = 300
SEGMENT_WIDTH = 30
MIN_DIFF = 40
SEARCH_BUFFER = 10

im1 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\a.png')
im2 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\stuff\b.png')

miscutils.colorGraph(im1, im2, rowNum)

im1[:,:,1] = np.zeros([im1.shape[0], im1.shape[1]])
im2[:,:,1] = np.zeros([im2.shape[0], im2.shape[1]])
im1[:,:,2] = np.zeros([im1.shape[0], im1.shape[1]])
im2[:,:,2] = np.zeros([im2.shape[0], im2.shape[1]])

scanline1 = im1[rowNum]
scanline2 = im2[rowNum]

#diffs used to prevent duplicates
diffs = []
for i in range(0, scanline1.shape[0] + 1 - SEGMENT_WIDTH):
    segment = scanline1[i:i + SEGMENT_WIDTH]
    blues = []
    for j in range(len(segment)):
        blues.append(segment[j][0])
    diff = max(blues) - min(blues)
    if diff >= MIN_DIFF:
        minPos = blues.index(min(blues)) + i
        maxPos = blues.index(max(blues)) + i
        
        segment2 = scanline2[max(i,i - SEARCH_BUFFER):min(i + SEGMENT_WIDTH, i + SEGMENT_WIDTH + SEARCH_BUFFER)]
        blues2 = []
        for k in range(len(segment2)):
            blues2.append(segment2[k][0])
    
        minPos2 = blues2.index(min(blues2))+ i - SEARCH_BUFFER
        maxPos2 = blues2.index(max(blues2))+ i - SEARCH_BUFFER
        #something is bugged here that makes the graphs look wrong

        if (minPos2 - minPos,maxPos2 - maxPos) in diffs:
            continue

        print("(" + str(minPos2 - minPos) + "," + str(maxPos2 - maxPos) + ")")
        diffs.append((minPos2 - minPos,maxPos2 - maxPos))

        #note for later: need an auto-detect for MIN_DIFF value
        #(so we don't have too few/many qualified diffs)

        plt.figure(i)
        plt.ylim(0, 255)
        plt.title("Matched min and max: " + str(i), fontdict=None, loc='center')
        plt.plot(range(0,scanline1.shape[0]), scanline1, linewidth=1, label='Left')
        plt.plot(range(0,scanline1.shape[0]), scanline2, linewidth=1, label='Right')
        plt.plot([minPos,minPos2],[min(blues),min(blues2)],linewidth=2)
        plt.plot([maxPos,maxPos2],[max(blues),max(blues2)],linewidth=2)
        plt.legend()
        plt.show()
