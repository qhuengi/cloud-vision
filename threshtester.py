import os
from functools import reduce
import cv2 as cv
from skimage import filters
import miscutils
import numpy as np
confusion = {'TP':[255,255],'FP':[255,0],'TN':[0,0],'FN':[0,255]}
methods={}
def hybridFactory(func):
    def hybrid(img,fixedThresh=None,sdthresh=None):
        mean,stddev=cv.meanStdDev(img)
        if stddev < sdthresh:
            return cv.threshold(img,fixedThresh,255,cv.THRESH_BINARY_INV)[1]
        return func(img)
    return hybrid
def kwargsWrapper(func):
    def wrapped(img,**kwargs):
        return func(img)
    return wrapped
def binary(img, fixedThresh=None,sdthresh=None):
    return cv.threshold(img,fixedThresh,255,cv.THRESH_BINARY_INV)[1]
methods['binary']=binary
methods['otsu'] = kwargsWrapper(lambda img:cv.threshold(cv.GaussianBlur(img,(5,5),0),0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)[1])
methods['hybrid otsu'] = hybridFactory(methods['otsu'])
methods['mce'] = kwargsWrapper(lambda img: cv.threshold(img,filters.threshold_li(img),255,cv.THRESH_BINARY_INV)[1])
methods['hybrid mce'] = hybridFactory(methods['mce'])
maps={}
maps['br']=lambda x: np.array(miscutils.brMap(x)*255,dtype='uint8')
maps['saturation'] = lambda img:cv.cvtColor(img,cv.COLOR_BGR2HSV)[:,:,1]
params={}
params['br']={'fixedThresh':int(0.25*255),'sdthresh':0.03}
params['saturation']={'fixedThresh':29,'sdthresh':4.5}
imDirectory = r'C:\Users\me\cloud-vision\threshtester\images'
files = os.listdir(imDirectory)
gtDirectory = r'C:\Users\me\cloud-vision\threshtester\2GT'
results = {mapName: {methodName: {result: 0 for result in confusion} for methodName in methods} for mapName in maps}
for file in files:
    print(file)
    imPath = imDirectory + '\\' + file
    gtPath = gtDirectory + '\\' + file[:file.find('.jpg')] + '_GT.jpg'
    im = cv.imread(imPath)
    gt = cv.imread(gtPath)
    for mapName in maps:
        mapped=maps[mapName](im)
        for method in methods:
            th = methods[method](mapped,**params[mapName])
            pixelMatches = np.array([th.flatten(),cv.cvtColor(gt,cv.COLOR_BGR2GRAY).flatten()]).T
            for result in confusion:
                matches = np.count_nonzero((pixelMatches==confusion[result]).all(1))
                results[mapName][method][result]+=matches
def total(x,y):
    return (None,x[1]+y[1])
accuracy={mapName: {methodName: None for methodName in methods} for mapName in maps}
for mapName in results:
    for method in results[mapName]:
        pxTotal = reduce(total,list(results[mapName][method].items()))[1]
        for result in results[mapName][method]:
            results[mapName][method][result]/=pxTotal
        accuracy[mapName][method]=results[mapName][method]['TP']+results[mapName][method]['TN']

