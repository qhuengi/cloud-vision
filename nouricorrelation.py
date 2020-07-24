import cv2 as cv
import miscutils
import numpy as np
BLOCKROWS = 10
filenames=[r'C:\Users\me\cloud-vision\examples\aligned1.jpg',
           r'C:\Users\me\cloud-vision\examples\aligned2.jpg',
           r'C:\Users\me\cloud-vision\examples\aligned3.jpg']
ims=[cv.resize(cv.imread(file),(0,0),fx=0.5,fy=0.5) for file in filenames]
mapped=[miscutils.brMap(im) for im in ims]
diff1 = mapped[2] - mapped[1]
diff2 = mapped[1] - mapped[0]
diff1 = np.array((diff1-diff1.min())/(diff1.max()-diff1.min())*255,dtype='uint8')
diff2 = np.array((diff2-diff2.min())/(diff2.max()-diff2.min())*255,dtype='uint8')
blockHeight = int(diff1.shape[0]/BLOCKROWS)
blockWidth = int(diff1.shape[1]/BLOCKROWS)
for i in range(BLOCKROWS):
    (top,bottom) = (i,i+1)*blockHeight
    for j in range(BLOCKROWS):
        (left,right) = (j,j+1)*blockWidth
        region=diff1[top:bottom,left:right]
        res = cv.matchTemplate(diff2, region, cv.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc=cv.minMaxLoc(res)
