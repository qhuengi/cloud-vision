import brmap
import cv2 as cv
import numpy as np
def hytaThreshold(mapped, sdthresh = 0.03, fixedThresh = 0.25):
    '''Takes one-channel decimal image (intensities 0-1) and applies hybrid thresholding.

    Keyword arguments
    sdthresh -- min. std. dev. to use adaptive over fixed threshold (default 0.03)
    fixedThresh -- threshold to use for fixed thresholding (default 0.25)
    '''

    mean, stddev = cv.meanStdDev(mapped)
    if stddev < sdthresh:
        return cv.threshold(mapped, brThresh,255,cv.THRESH_BINARY)[1]
    else:
        # normalizes image from 0-1 to 0-255 because otsu threshold doesn't like        decimals for some reason
        mapped = np.array(mapped * 255, dtype='uint8')
        blur = cv.GaussianBlur(mapped,(5,5),0)
        return cv.threshold(mapped, 0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
        
