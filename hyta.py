import brmap
import cv2 as cv
import numpy as np
def hytaThreshold(mapped, sdthresh = 0.03, fixedThresh = 0.25, method=cv.THRESH_BINARY_INV):
    '''Takes one-channel decimal image (intensities 0-1) and applies hybrid thresholding.

    Keyword arguments
    sdthresh -- min. std. dev. to use adaptive over fixed threshold (default 0.03)
    fixedThresh -- threshold to use for fixed thresholding (default 0.25)
    method -- thresholding method to use (default cv.THRESH_BINARY_INV)
    '''

    mean, stddev = cv.meanStdDev(mapped)
    if stddev < sdthresh:
        return cv.threshold(mapped, brThresh,255, method)[1]
    else:
        # normalizes image from 0-1 to 0-255 because otsu threshold doesn't like        decimals for some reason
        mapped = np.array(mapped * 255, dtype='uint8')
        blur = cv.GaussianBlur(mapped,(5,5),0)
        return cv.threshold(blur, 0,255,method+cv.THRESH_OTSU)[1]
        
