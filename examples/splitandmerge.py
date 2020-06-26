import brmap
import cv2 as cv
import numpy as np
import copy
cloud=cv.imread(r'D:\Users\me\Downloads\cloud.jpg')
img=np.array(brmap.brMap(cloud)*255,dtype='uint8')
blur = cv.GaussianBlur(img,(5,5),0)
ret,th = cv.threshold(blur,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
contours, hier = cv.findContours(th, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
imContours = copy.deepcopy(cloud)
cv.drawContours(imContours, contours, -1, (0,0,255),2)
# removes contours which are children of other contours
indices = filter(lambda x: hier[0][x][3] < 0, range(len(hier[0])))
contoursFiltered = list(map(lambda x: contours[x],indices))
imFiltered = copy.deepcopy(cloud)
cv.drawContours(imFiltered, contoursFiltered, -1, (0,0,255),2)
boundRects = list(map(lambda x: cv.boundingRect(x),contoursFiltered))
for rect in boundRects:
    cv.rectangle(cloud,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,255,0),2)
cv.imshow('rect',cloud)
cv.imshow('contours',imContours)
cv.imshow('filtered',imFiltered)
