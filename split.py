import brmap
import cv2 as cv
import numpy as np
import copy

def flatten(l, ltypes=(list, tuple)):
    '''Flattens list.'''
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

def filterRect(img, rect,threshold=.4):
    print(rect)
    (x,y,w,h)=rect
    mask = np.zeros(img.shape,dtype='uint8')
    cv.rectangle(mask, (x,y),(x+w,y+h), 255, cv.FILLED)
    mean,stddev = cv.meanStdDev(img,mask=mask)
    return mean < threshold

def split(img, rect, sdthreshold = 0.13,sizethreshold = 1000):
    #import pdb;pdb.set_trace()
    #print(rect)
    mask = np.zeros(img.shape,dtype='uint8')
    (x,y,w,h) = rect
    cv.rectangle(mask,(x,y),(x+w,y+h), 255, cv.FILLED)
    mean,stddev = cv.meanStdDev(img,mask=mask)
    print(stddev)
    if stddev[0][0] < sdthreshold or w*h < sizethreshold:
        return [rect]
    rects = []
    for i in [0,1]:
        for j in [0,1]:
            left = int(x + i*w/2)
            top = int(y + j*h/2)
            rects.append(split(img, (left,top,int(w/2),int(h/2))))
    return flatten(rects,list)
