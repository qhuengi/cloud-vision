#many parts taken from wip.py

import miscutils
import cv2 as cv
import numpy as np
import copy
Y_COORD = 200
BUFFER = 1

cloud1 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\a1.jpg')
mapped1 = miscutils.brMap(cloud1)
th1 = miscutils.hytaThreshold(mapped1) 
contours1, hier1 = cv.findContours(th1, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# removes contours which are children of other contours
indices1 = filter(lambda x: hier1[0][x][3] < 0, range(len(hier1[0])))
contoursFiltered1 = list(map(lambda x: contours1[x],indices1))
imContours1=copy.deepcopy(cloud1)
cv.drawContours(imContours1,contoursFiltered1,-1,(0,255,0),3)
cv.imshow('contours1',imContours1)

cloud2 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\a2.jpg')
mapped2 = miscutils.brMap(cloud2)
th2 = miscutils.hytaThreshold(mapped2) 
contours2, hier2 = cv.findContours(th2, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# removes contours which are children of other contours
indices2 = filter(lambda x: hier2[0][x][3] < 0, range(len(hier2[0])))
contoursFiltered2 = list(map(lambda x: contours2[x],indices2))
imContours2=copy.deepcopy(cloud2)
cv.drawContours(imContours2,contoursFiltered2,-1,(0,255,0),3)
cv.imshow('contours2',imContours2)

contoursList1 = []
contoursList2 = []
for a in range(len(contoursFiltered1)):
    for b in range(len(contoursFiltered1[a])):
        if contoursFiltered1[a][b][0][1] in range(Y_COORD - BUFFER, Y_COORD + BUFFER):
            contoursList1.append(contoursFiltered1[a][b][0][0])
            contoursList1 = sorted(contoursList1)
for a in range(len(contoursFiltered2)):
    for b in range(len(contoursFiltered2[a])):
        if contoursFiltered2[a][b][0][1] in range(Y_COORD - BUFFER, Y_COORD + BUFFER):
            contoursList2.append(contoursFiltered2[a][b][0][0])
            contoursList2 = sorted(contoursList2)
print(contoursList1)
print(contoursList2)

while cv.waitKey() == -1:
    pass
cv.destroyAllWindows()
