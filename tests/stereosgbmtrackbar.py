import cv2 as cv
from matplotlib import pyplot as plt
blockSize=11
numDisparities=16
left=cv.cvtColor(cv.imread(r'D:\Users\me\Downloads\bathleft.jpg'), cv.COLOR_BGR2GRAY)
right=cv.cvtColor(cv.imread(r'D:\Users\me\Downloads\bathright.jpg'),cv.COLOR_BGR2GRAY)
left=cv.resize(left,(0,0),fx=0.4,fy=0.4)
right=cv.resize(right,(0,0),fx=0.4,fy=0.4)
def changeBlock(val):
    global blockSize
    blockSize = val
    print(blockSize)
    onTrackbar()
def changeDisparities(val):
    global numDisparities
    numDisparities = val*16
    print(numDisparities)
    onTrackbar()
def onTrackbar():
    ret = cv.StereoSGBM_create(blockSize=blockSize,numDisparities=numDisparities)
    disparity=ret.compute(left,right)
    del ret
    plt.imshow(disparity,'gray')
    plt.show()
cv.namedWindow('trackbar')
trackVal = 20
maxBlock = 30
maxDisparities = 32
cv.createTrackbar('Block Size: ','trackbar',blockSize, maxBlock, changeBlock)
cv.createTrackbar('Num disparities/16: ','trackbar',numDisparities*16,maxDisparities,changeDisparities)
onTrackbar()
cv.waitKey(0) & 0xFF
cv.destroyAllWindows()

