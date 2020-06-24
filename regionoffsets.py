import cv2 as cv
import numpy as np

class RegionOffsets:
    '''
    Cross correlates regions of image against reference to find their locations in the reference image.
    
    Parameters
    ----------
    im: Mat
    reference: Mat
    rows: int
    Number of rows of regions to use, i.e. number of regions=rows^2.

    Attributes
    ----------
    im, reference, rows identical to parameters.
    offsets: np.ndarray
    rows x rows x 2 array of image regions' locations in reference image.
    matchiness: np.ndarray
    rows x rows array of max cross correlation score of each region against reference.
    drawOffsets(): Mat
    returns reference image with lines drawn showing offsets of regions.
    '''
    def __init__(self, im, reference, rows = 5):
        self.im = im
        self.reference = reference
        self.rows = rows
        self.offsets = np.empty((rows, rows, 2))
        self.matchiness = np.empty((rows, rows))
        self.__regionSize = np.array(np.asarray(reference.shape[:2]) / rows, dtype='uint16')
        for y in range(rows):
            # sets bounds of region currently being tested
            [top, bottom] = np.array([y, y + 1]) * self.__regionSize[0]
            for x in range(rows):
                progress = int((y / rows + x / (rows**2)) * 100)
                print("Initializing: ", progress, "%")
                [left, right] = np.array([x, x + 1]) * self.__regionSize[1]
                imRegion = im[top:bottom, left:right]
                res = cv.matchTemplate(reference, imRegion, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
                self.matchiness[y][x] = max_val
                offset = np.array([max_loc[1], max_loc[0]])
                self.offsets[y][x] = offset
    def drawOffsets(self):
        imOffsets = self.reference
        for y in range(self.rows):
            for x in range(self.rows):
                # circle function is (x,y) instead of (y,x) for some reason
                refCorner = (x * self.__regionSize[1], y * self.__regionSize[0])
                offsetCorner = tuple(np.array(self.offsets[y][x][::-1],dtype='int32'))
                # arbitrary unique color for each region
                color = (40*x,100,40*y)
                cv.circle(imOffsets, refCorner, 15, color, -1)
                cv.circle(imOffsets, offsetCorner, 15, color, -1)
                cv.line(imOffsets, refCorner, offsetCorner, color, 3)
        return imOffsets
