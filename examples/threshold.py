import brmap
import cv2 as cv
import numpy as np
cloud=cv.imread(r'D:\Users\me\Downloads\cloud.jpg')
img=np.array(brmap.brMap(cloud)*255,dtype='uint8')
threshMethods=[cv.THRESH_BINARY,cv.THRESH_BINARY+cv.THRESH_OTSU]
ret1,th1 = cv.threshold(img,255*.25,255,cv.THRESH_BINARY)
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# Otsu's thresholding after Gaussian filtering
#blur = cv.GaussianBlur(img,(5,5),0)
#ret2,th2 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
con1,hier1 = cv.findContours(th1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
imContours1=cv.drawContours(cloud,con1,-1,(0,255,0),3)
cv.imshow('binary',imContours1)
con2,hier2 = cv.findContours(th2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
imContours2=cv.drawContours(cloud,con2,-1,(0,255,0),3)
cv.imshow('otsu',imContours2)
