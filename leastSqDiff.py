import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sys

img1 = cv2.imread("20200606_120040.jpg")
rows, cols, channels = img1.shape
print(str(sys.maxsize))
print("Rows: " + str(rows))
print("Columns: " + str(cols))

rowNum = int(input("Enter a row number: "))

#get rgb vals for image 1:
red1 = []
green1 = []
blue1 = []
brightness1 = []

img1_hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

for i in range(cols):
    pixel = img1[rowNum, i]
    red1.append(pixel[2])
    green1.append(pixel[1])
    blue1.append(pixel[0])
    pixel2 = img1_hsv[rowNum, i]
    brightness1.append(pixel2[2])

redTotal1 = 0
greenTotal1 = 0
blueTotal1 = 0

brightnessRatios = []

#calculate sums
for redPx in red1:
    redTotal1 += redPx
for greenPx in green1:
    greenTotal1 += greenPx
for bluePx in blue1:
    blueTotal1 += bluePx
img2 = cv2.imread("20200606_120046.jpg")

img2_hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
red2 = []
green2 = []
blue2 = []

redTotal2 = 0
greenTotal2 = 0
blueTotal2 = 0

leastSqDiff = 0
leastSqDiffRow = 0

brightness2 = []

sqDiff = 0

#50 rows of pixels above
for x in range(0, 50):
    for i in range(cols):
        pixel2 = img2[rowNum + x, i]
        red2.append(pixel2[2])
        green2.append(pixel2[1])
        blue2.append(pixel2[0])
        pixel3 = img2_hsv[rowNum+x, i]
        brightness2.append(pixel3[2])
    plt.figure(1)
    plt.ylim(0, 255)
    plt.title("Brightness Plot: Right Image Row " + str(rowNum+x), fontdict=None, loc='center')
    plt.plot(range(0,cols), brightness1, linewidth=1, label='Left')
    plt.plot(range(0,cols), brightness2, linewidth=1, label='Right')
    plt.legend()
    plt.show()
    #calculate sums
    for redPx in red2:
        redTotal2 += redPx
    for greenPx in green2:
        greenTotal2 += greenPx
    for bluePx in blue2:
        blueTotal2 += bluePx
    
    #get squared difference
    deltaR = redTotal2 - redTotal1
    deltaG = greenTotal2 - greenTotal1
    deltaB = blueTotal2 - blueTotal1
    sqDiff = pow(deltaR, 2) + pow(deltaG, 2) + pow(deltaB, 2)
    if x == 0:
        leastSqDiff = sqDiff
        leastSqDiffRow = rowNum + x
        print("Red Total: " + str(redTotal2))
        print("Delta R: " + str(deltaR))

    else:
        if sqDiff < leastSqDiff:
            leastSqDiff = sqDiff
            leastSqDiffRow = rowNum + x
    redTotal2 = 0
    greenTotal2 = 0
    blueTotal2 = 0
    red2.clear()
    green2.clear()
    blue2.clear()
    brightness2.clear()
    sqDiff = 0

#50 rows of pixels below
for x in range(0, 50):
    for i in range(cols):
        pixel2 = img2[rowNum - x, i]
        red2.append(pixel2[2])
        green2.append(pixel2[1])
        blue2.append(pixel2[0])
        pixel3 = img2_hsv[rowNum-x, i]
        brightness2.append(pixel3[2])
    plt.figure(1)
    plt.ylim(0, 255)
    plt.title("Brightness Plot: Right Image Row " + str(rowNum-x), fontdict=None, loc='center')
    plt.plot(range(0,cols), brightness1, linewidth=1, label='Left')
    plt.plot(range(0,cols), brightness2, linewidth=1, label='Right')
    plt.legend()
    plt.show()
    #calculate sums
    for redPx in red2:
        redTotal2 += redPx
    for greenPx in green2:
        greenTotal2 += greenPx
    for bluePx in blue2:
        blueTotal2 += bluePx

    #get squared difference
    deltaR = redTotal2 - redTotal1
    deltaG = greenTotal2 - greenTotal1
    deltaB = blueTotal2 - blueTotal1
    sqDiff = pow(deltaR, 2) + pow(deltaG, 2) + pow(deltaB, 2)
    if x == 0:
        leastSqDiff = sqDiff
        leastSqDiffRow = rowNum - x
    else:
        if sqDiff < leastSqDiff:
            leastSqDiff = sqDiff
            leastSqDiffRow = rowNum - x
    redTotal2 = 0
    greenTotal2 = 0
    blueTotal2 = 0
    red2.clear()
    green2.clear()
    blue2.clear()
    sqDiff = 0
print("leastSqDiffRow: " + str(leastSqDiffRow))
