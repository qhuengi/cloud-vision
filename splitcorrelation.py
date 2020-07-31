import miscutils
import cv2 as cv
import numpy as np
import copy
SDTHRESH=0.013
SPLITSIZETHRESH=8000
SIZETHRESH=1000

cloudleft = cv.resize(cv.imread(r'D:\Users\me\Downloads\alignedleft.jpg'),(0,0),fx=0.4,fy=0.4)
cloudleftgray=cv.cvtColor(cloudleft,cv.COLOR_BGR2GRAY)
cloud = cv.resize(cv.imread(r'D:\Users\me\Downloads\alignedright.jpg'),(0,0),fx=0.4,fy=0.4)
mapped = miscutils.brMap(cloud)
cv.imwrite('blueredratio.jpg',mapped)
cv.imshow('mapped',mapped)
th = miscutils.hytaThreshold(mapped) 
cv.imshow('thresh',th)
cv.imwrite('thresh.jpg',th)
contours, hier = cv.findContours(th, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# removes contours which are children of other contours
indices = filter(lambda x: hier[0][x][3] < 0, range(len(hier[0])))
contoursFiltered = list(map(lambda x: contours[x],indices))
imContours=copy.deepcopy(cloud)
cv.drawContours(imContours,contoursFiltered,-1,(0,255,0),3)
cv.imwrite('contours.jpg',imContours)
cv.imshow('contours',imContours)
# finds bounding rectangles of filtered contours
boundRects = list(map(cv.boundingRect,contoursFiltered))
ugh=copy.deepcopy(cloud)
for rect in boundRects:
    cv.rectangle(ugh, (rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]), (0,255,0),2)
cv.imwrite('boundRects.jpg',ugh)
# filter out tiny rectangles
boundRects = list(filter(lambda x: x[2]*x[3] > SIZETHRESH, boundRects))
# maps each rect to list of smaller rects generated by split, filters non-cloud rects
splitRects=list(map(lambda x: miscutils.split(mapped, x, sdthreshold=SDTHRESH,sizethreshold=SPLITSIZETHRESH), boundRects))
test=copy.deepcopy(cloud)
for rects in splitRects:
    for rect in rects:
        cv.rectangle(test, (rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]), (0,255,0),2)
cv.imshow('test',test)
cv.imshow('ff',ugh)
while cv.waitKey() == -1:
    pass
cv.destroyAllWindows()
'''
for rects in splitRects:
    for rect in rects:
        imMatch = copy.deepcopy(cloudleft)
        imRect = copy.deepcopy(cloud)
        (x,y,w,h)=rect
        region=cloud[y:y+h,x:x+w]
        regionGray=cv.cvtColor(region,cv.COLOR_BGR2GRAY)
        res = cv.matchTemplate(cloudleftgray,regionGray,cv.TM_CCOEFF_NORMED)
        minval,maxval,minloc,maxloc=cv.minMaxLoc(res)
        top_left=maxloc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(imMatch, top_left, bottom_right, 255,2)
        cv.rectangle(imRect, (x,y),(x+w,y+h),255,2)
        cv.imshow('match',imMatch)
        cv.imshow('original',imRect)
        while cv.waitKey() == -1:
            pass
        cv.destroyAllWindows()
'''
def matchLoc(maskRect):
    (x,y,w,h) = maskRect
    region = cv.cvtColor(cloud[y:y+h,x:x+w], cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(cloudleftgray,region,cv.TM_CCOEFF_NORMED)
    minval,maxval,minloc,maxloc = cv.minMaxLoc(res)
    matchCenter = (int(maxloc[0] + w/2), int(maxloc[1] + h/2))
    return [matchCenter, (int(x+w/2),int(y+h/2))]
displacements = [list(map(matchLoc, rects)) for rects in splitRects]
for row in displacements:
    for disp in row:
        cv.arrowedLine(test,disp[1], disp[0], (255,0,0), 2,tipLength=0.3)
cv.imshow('displacements',test)
while cv.waitKey() == -1:
    pass
cv.destroyAllWindows()
cv.imwrite('rectDisplacements.jpg',test)

