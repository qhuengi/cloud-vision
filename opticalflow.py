import miscutils
import cv2 as cv
import numpy as np
import copy

cloudOld = cv.resize(cv.imread(r'D:\Users\me\Downloads\alignedleft.jpg'),(0,0),fx=0.4,fy=0.4)
cloudNew = cv.resize(cv.imread(r'D:\Users\me\Downloads\alignedright.jpg'),(0,0),fx=0.4,fy=0.4)
mappedOld = miscutils.brMap(cloudOld)
mappedNew = miscutils.brMap(cloudNew)
thOld = miscutils.hytaThreshold(mappedOld) 
thNew = miscutils.hytaThreshold(mappedNew) 
grayOld = cv.cvtColor(cloudOld,cv.COLOR_BGR2GRAY)
grayNew = cv.cvtColor(cloudNew,cv.COLOR_BGR2GRAY)
pOld = cv.goodFeaturesToTrack(grayOld,100,0.3,7,mask=thOld)
pNew,st,err = cv.calcOpticalFlowPyrLK(grayOld,grayNew,pOld,None)
goodOld=pOld[st==1]
goodNew=pNew[st==1]
for i in range(len(goodOld)):
    cv.arrowedLine(cloudOld,tuple(goodOld[i]),tuple(goodNew[i]),(0,255,0), thickness=2)
cv.imshow('optical flow', cloudOld)
while(cv.waitKey())==0:
    pass
cv.destroyAllWindows()
