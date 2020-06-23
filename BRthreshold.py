import cv2 as cv
import numpy as np

filename=r"D:\Users\me\Downloads\cloud.jpg"
cloud=cv.imread(filename)

# returns normalized blue/red ratio
def ratio(pixel):
    # sets red pixel intensity to 1 to avoid division by 0
    if pixel[2]==0:
	    pixel[2]=1
    brRatio=pixel[0]/pixel[2]
    return (brRatio-1)/(brRatio+1)

# applies function to each pixel of image, kind of stupid
def imageMap(image,func):
    mapped=np.empty(image.shape[0:2])
    for i in range(0,image.shape[0]):
        for j in range(0,image.shape[1]):
            mapped[i][j]=func(image[i][j])
    return(mapped)

thresholdValue=0.25

cloudRatio=imageMap(cloud,ratio)
ret,thresh=cv.threshold(cloudRatio,.25,1,cv.THRESH_BINARY)
cv.imshow('threshold',thresh)
cv.imshow('orig',cloud)
