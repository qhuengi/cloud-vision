import cv2 as cv
import numpy as np

cloud=cv.imread(r"D:\Users\me\Downloads\cloud.jpg")
def ratio(pixel):
    if pixel[2]==0:
	    pixel[2]=1
    brRatio=pixel[0]/pixel[2]
    return (brRatio-1)/(brRatio+1)

def imageMap(image,func):
    mapped=np.empty(image.shape[0:2])
    for i in range(0,image.shape[0]):
        for j in range(0,image.shape[1]):
            mapped[i][j]=func(image[i][j])
    return(mapped)

thresholdValue=0.25

#ratioDebug=lambda x:int(255*ratio(x))
cloudRatio=imageMap(cloud,ratio)
#cloudRatioDebug=imageMap(cloud,ratioDebug).astype(np.int8)
ret,thresh=cv.threshold(cloudRatio,.25,1,cv.THRESH_BINARY)
cv.imshow('threshold',thresh)
cv.imshow('orig',cloud)
