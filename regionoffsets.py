import cv2 as cv
import numpy as np
ROW_COUNT = 5

def templateMatch(im, template):
    res = cv.matchTemplate(im, template, cv.TM_CCOEFF_NORMED)
    return cv.minMaxLoc(res)
def rotate(im, angle):
    center = (int(im.shape[1]/2),int(im.shape[0]/2))
    rot_mat = cv.getRotationMatrix2D(center, angle, 1.0)
    result = cv.warpAffine(im, rot_mat, im.shape[1::-1])
    return result

referenceFilename = r'D:\Users\me\Downloads\panelright.jpg'
imFilename = r'D:\Users\me\Downloads\panelleft.jpg'
reference = cv.imread(referenceFilename)
im = cv.imread(imFilename)
referenceDebug = reference
#im=rotate(reference, 3)
offsets = np.empty((ROW_COUNT, ROW_COUNT, 2))
matchiness = np.zeros((ROW_COUNT, ROW_COUNT))
# region dimensions = height & width of image divided by number of rows
regionSize = np.array(np.asarray(reference.shape[:2]) / ROW_COUNT, dtype='uint16')
for y in range(ROW_COUNT):
    [top, bottom] = np.array([y, y + 1]) * regionSize[0]
    print("Y: ", y)
    for x in range(ROW_COUNT):
        print("X: ", x)
        [left, right] = np.array([x, x + 1]) * regionSize[1]
        color = (40*x,100,40*y)
        cv.circle(referenceDebug, (left, top), 15, color, -1)
        imRegion = im[top:bottom, left:right]
        min_val, max_val, min_loc, max_loc = templateMatch(reference, imRegion)
        matchiness[y][x] = max_val
        print("Max loc: ", max_loc)
        offset = np.array([max_loc[1], max_loc[0]])
        cv.circle(referenceDebug, max_loc, 15, color, -1)
        print("Top: ", top, " Left: ", left)
        offsets[y][x] = offset
        cv.line(referenceDebug, (left, top), max_loc, color, 3)
        print(offset)
print(offsets)
cv.imwrite('aaaaaaaaaaaaaaaaaaa.jpg',referenceDebug)
