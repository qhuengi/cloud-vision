import cv2 as cv
from matplotlib import pyplot as plt
blockSize=11
numDisparities=16*9
left=cv.cvtColor(cv.imread(r'D:\Users\me\Downloads\bathleft.jpg'), cv.COLOR_BGR2GRAY)
right=cv.cvtColor(cv.imread(r'D:\Users\me\Downloads\bathright.jpg'),cv.COLOR_BGR2GRAY)
left=cv.resize(left,(0,0),fx=0.4,fy=0.4)
right=cv.resize(right,(0,0),fx=0.4,fy=0.4)
ret=cv.StereoSGBM_create(blockSize=blockSize,numDisparities=numDisparities)
disparity=ret.compute(left,right)
plt.imshow(disparity,'gray')
plt.show()
