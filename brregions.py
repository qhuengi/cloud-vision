import brmap
import cv2 as cv
import numpy as np
ROW_COUNT = 10
cloud = cv.imread(r'D:\Users\me\Downloads\cloud.jpg')
mapped = brmap.brMap(cloud)
regionSize = np.array(np.array(cloud.shape)/ROW_COUNT, dtype = 'uint16')
means=np.empty((ROW_COUNT,ROW_COUNT))
for y in range(ROW_COUNT):
    [top, bottom] = np.array([y, y + 1]) * regionSize[0]
    for x in range(ROW_COUNT):
        [left, right] = np.array([x, x + 1]) * regionSize[1]
        region = cloud[top:bottom,left:right]
        means[y][x]=np.sum(region)/(region.shape[0]*region.shape[1])
norm=255/np.max(means)
test=np.empty(cloud.shape[0:2],dtype='uint8')
for y in range(ROW_COUNT):
    [top, bottom] = np.array([y, y + 1]) * regionSize[0]
    for x in range(ROW_COUNT):
        [left, right] = np.array([x, x + 1]) * regionSize[1]
        test[top:bottom,left:right]=means[y][x]*norm*np.ones(region.shape[:2])
cv.imshow('test',test)
        
        


