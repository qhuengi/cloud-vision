import cv2 as cv
import numpy as np

def brMap(image):
    '''
    Maps each pixel of image to its normalized blue/red ratio (see Li et al., 2011).
    '''
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

def colorGraph(im1, im2, rowNum):
    '''Graphs intensities of each color channel of two images at given row.'''
    cols=im1.shape[1]
    (blue1, green1, red1) = im1[rowNum,:].T
    (blue2, green2, red2) = im2[rowNum,:].T
    plt.figure(1)
    plt.ylim(0, 255)
    plt.title("RGB Plot (Red): Row " + str(rowNum), fontdict=None, loc='center')
    plt.plot(range(0,cols), red1, linewidth=1, label='Left')
    plt.plot(range(0,cols), red2, linewidth=1, label='Right')
    plt.legend()

    plt.figure(2)
    plt.ylim(0, 255)
    plt.title("RGB Plot (Green): Row " + str(rowNum), fontdict=None, loc='center')
    plt.plot(range(0,cols), green1, linewidth=1, label='Left')
    plt.plot(range(0,cols), green2, linewidth=1, label='Right')
    plt.legend()


    plt.figure(3)
    plt.ylim(0, 255)
    plt.title("RGB Plot (Blue): Row " + str(rowNum), fontdict=None, loc='center')
    plt.plot(range(0,cols), blue1, linewidth=1, label='Left')
    plt.plot(range(0,cols), blue2, linewidth=1, label='Right')
    plt.legend()

    plt.show()        

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
                color = tuple(self.matchiness[y][x]*[255,255,255])
                cv.circle(imOffsets, refCorner, 15, color, -1)
                cv.circle(imOffsets, offsetCorner, 15, color, -1)
                cv.line(imOffsets, refCorner, offsetCorner, color, 3)
        return imOffsets

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
    '''Recursively splits bounding rectangle into homogenous rects.

    Keyword arguments
    sdthreshold -- max standard deviation of rectangle before being split. (default 0.13).
    sizethreshold -- min size of rectangle (default 1000).
    '''
    
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
