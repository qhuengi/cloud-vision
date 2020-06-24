import cv2 as cv
import numpy as np


def brMap(image, threshold=0.25):
    """Maps each pixel to its normalized blue/red ratio (see Li et al., 2011).

    Keyword arguments:
    threshold -- threshold value for ratio, between 0 and 1, default 0.25.
    """
    mapped=np.empty(image.shape[0:2])
    for i in range(0,image.shape[0]):
        for j in range(0,image.shape[1]):
            pixel=image[i][j]
            # sets red pixel intensity to 1 to avoid division by 0
            if pixel[2]==0:
                pixel[2]=1
            brRatio=pixel[0]/pixel[2]
            mapped[i][j]=(brRatio-1)/(brRatio+1)
    return mapped
