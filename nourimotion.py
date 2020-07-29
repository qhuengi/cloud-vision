import cv2 as cv
import miscutils
import numpy as np
# params for ShiTomasi corner detection
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
filenames=[r'C:\Users\me\cloud-vision\examples\aligned1.jpg',
           r'C:\Users\me\cloud-vision\examples\aligned2.jpg',
           r'C:\Users\me\cloud-vision\examples\aligned3.jpg']
ims=[cv.resize(cv.imread(file),(0,0),fx=0.5,fy=0.5) for file in filenames]
mapped=[np.array(cv.cvtColor(im,cv.COLOR_BGR2HSV)[:,:,1],dtype='int16') for im in ims]
cv.imshow('mapped',mapped[0])
cv.waitKey(0) & 0xFF
diff2 = mapped[2] - mapped[1]
diff1 = mapped[1] - mapped[0]
diff1 = np.array((diff1-diff1.min())/(diff1.max()-diff1.min())*255,dtype='uint8')
diff2 = np.array((diff2-diff2.min())/(diff2.max()-diff2.min())*255,dtype='uint8')
thresh1 = cv.threshold(diff1,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
thresh2 = cv.threshold(diff2,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
p1=cv.goodFeaturesToTrack(thresh1, mask=None,**feature_params)
p2,st,err=cv.calcOpticalFlowPyrLK(thresh1,thresh2,p1,None,**lk_params)
p1Good=p1[st==1]
p2Good=p2[st==1]
im2=cv.resize(cv.imread(filenames[1]),(0,0),fx=0.5,fy=0.5)
for n in range(len(p1Good)):
    cv.arrowedLine(im2,tuple(p1Good[n]),tuple(p2Good[n]),(255,0,0),thickness=2)
cv.imshow('thresh1',thresh1)
cv.imshow('thresh2',thresh2)
cv.imshow('daflow',im2)
cv.waitKey(0) & 0xFF
cv.imwrite(r'C:\Users\me\cloud-vision\nouriopticalflow.jpg', im2)
cv.imwrite('thresh1.jpg',thresh1)
cv.imwrite('thresh2.jpg',thresh2)
cv.imwrite('diff1.jpg',diff1)
cv.imwrite('diff2.jpg',diff2)
