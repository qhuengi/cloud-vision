import miscutils
import cv2 as cv
left=cv.imread(r'D:\Users\me\Downloads\mleft.png')
right=cv.imread(r'D:\Users\me\Downloads\mright.png')
miscutils.colorGraph(left,right,900)
