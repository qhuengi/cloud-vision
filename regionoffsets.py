import cv2 as cv
import numpy as np
# number of regions = ROW_COUNT^2, he wants us to try changing the number of regions
ROW_COUNT = 5

# idk why this is in a separate function, something with memory
def templateMatch(im, template):
    res = cv.matchTemplate(im, template, cv.TM_CCOEFF_NORMED)
    return cv.minMaxLoc(res)

referenceFilename = r'D:\Users\me\Downloads\panelright.jpg'
imFilename = r'D:\Users\me\Downloads\panelleft.jpg'
reference = cv.imread(referenceFilename)
im = cv.imread(imFilename)
referenceDebug = reference
offsets = np.empty((ROW_COUNT, ROW_COUNT, 2))
matchiness = np.empty((ROW_COUNT, ROW_COUNT))
# region dimensions = height & width of image divided by number of rows
regionSize = np.array(np.asarray(reference.shape[:2]) / ROW_COUNT, dtype='uint16')
for y in range(ROW_COUNT):
    # sets bounds of region currently being tested
    [top, bottom] = np.array([y, y + 1]) * regionSize[0]
    print("Y: ", y)
    for x in range(ROW_COUNT):
        print("X: ", x)
        [left, right] = np.array([x, x + 1]) * regionSize[1]
        # arbitrary color but different for each region
        color = (40*x,100,40*y)
        cv.circle(referenceDebug, (left, top), 15, color, -1)
        imRegion = im[top:bottom, left:right]
        min_val, max_val, min_loc, max_loc = templateMatch(reference, imRegion)
        # matchiness array just for debugging
        matchiness[y][x] = max_val
        print("Max loc: ", max_loc)
        offset = np.array([max_loc[1], max_loc[0]])
        cv.circle(referenceDebug, max_loc, 15, color, -1)
        print("Top: ", top, " Left: ", left)
        offsets[y][x] = offset
        cv.line(referenceDebug, (left, top), max_loc, color, 3)
        print(offset)
print(offsets)
cv.imwrite('aaaaaaaaaaaaaaaaaaa.jpg', referenceDebug)
