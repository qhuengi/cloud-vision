import cv2 as cv
import miscutils
filename = r'D:\Users\me\Downloads\croppedcloud.jpg'
resizeFactor = 0.2
cloud = cv.resize(cv.imread(filename), (0,0),fx=resizeFactor, fy=resizeFactor)
mapped = miscutils.brMap(cloud)
thresh = miscutils.hytaThreshold(mapped)
cv.imshow('threshold',thresh)
cv.imshow('cloud',cloud)
while(cv.waitKey()==0):
    pass
