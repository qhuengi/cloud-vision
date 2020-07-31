import copy
import cv2 as cv
import miscutils
import numpy as np
BLOCKROWS = 7
filenames=[r'C:\Users\me\cloud-vision\examples\aligned1.jpg',
           r'C:\Users\me\cloud-vision\examples\aligned2.jpg',
           r'C:\Users\me\cloud-vision\examples\aligned3.jpg']
ims=[cv.resize(cv.imread(file),(0,0),fx=0.5,fy=0.5) for file in filenames]
mapped=[miscutils.brMap(im) for im in ims]
diff2 = mapped[2] - mapped[1]
diff1 = mapped[1] - mapped[0]
diff1 = np.array((diff1-diff1.min())/(diff1.max()-diff1.min())*255,dtype='uint8')
diff2 = np.array((diff2-diff2.min())/(diff2.max()-diff2.min())*255,dtype='uint8')
thresh1 = cv.threshold(diff1,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
thresh2 = cv.threshold(diff2,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
cv.imshow('thresh1',thresh1)
cv.imshow('thresh2',thresh2)
cv.waitKey(0) & 0xFF
blockHeight = int(diff1.shape[0]/BLOCKROWS)
blockWidth = int(diff1.shape[1]/BLOCKROWS)
im1 = copy.deepcopy(ims[1])
for i in range(BLOCKROWS):
    (top,bottom) = tuple(np.array((i,i+1))*blockHeight)
    for j in range(BLOCKROWS):
        (left,right) = tuple(np.array((j,j+1))*blockWidth)
        region=diff1[top:bottom,left:right]
        res = cv.matchTemplate(diff2, region, cv.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc=cv.minMaxLoc(res)
        cv.arrowedLine(im1,(left,top),tuple(max_loc),(255,0,0),thickness=2)
cv.imshow('',im1)
cv.imwrite('nouricorrelationnothresh.jpg',im1)
cv.waitKey(0) & 0xFF
cv.destroyAllWindows()
