#this code is bad

import cv2 as cv
import numpy as np
import brmap
import random

image=cv.imread(r"C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\cloud.jpg")
cv.imshow('orig', image)

#CHANGE AS NEEDED (do not set too high or else your computer will explode)
radius = 1
threshold = 0.25

ret,image = cv.threshold(brmap.brMap(image), threshold, 1, cv.THRESH_BINARY)
image = np.array(image,dtype='float32')
image = cv.cvtColor(image,cv.COLOR_GRAY2BGR)
cv.imshow('thresh', image)
for i in range(0,image.shape[0]):
    for j in range(0,image.shape[1]):
        pixel=image[i][j]
        if pixel[0]==0:
            colorFound = False
            color = np.array([0,0,0])
            vDist = 0
            #vertical search
            for y in range(i-radius,i+radius):
                if y < 0 or y > image.shape[0]:
                    continue
                if np.all(image[y][j]) != np.all(np.array([255,255,255])) and np.all(image[y][j]) != np.all(np.array([0,0,0])):
                    colorFound = True
                    vDist = abs(y - i)
                    color = image[y][j]
                    break
            #horizontal search
            for x in range(i-radius,i+radius):
                if x < 0 or x > image.shape[1]:
                    continue
                if np.all(image[i][x]) != np.all(np.array([255,255,255])) and np.all(image[i][x]) != np.all(np.array([0,0,0])):
                    colorFound = True
                    hDist = abs(x - j)
                    if hDist < vDist:
                        color = image[i][x]
                    break
            if colorFound:
                pixel = color
            else:
                pixel = np.array([random.randint(1,254),random.randint(1,254),random.randint(1,254)])
cv.imshow('colors', image)
