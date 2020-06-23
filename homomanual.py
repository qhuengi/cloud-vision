import cv2 as cv
import numpy as np

imReference = cv.imread(r'D:\Users\me\Downloads\panelright.jpg')
im = cv.imread(r'D:\Users\me\Downloads\panelleft.jpg')
pointsReference = np.array([[650,1748],
                            [248,1469],
                            [491,1388],
                            [1860,1279]])
points = np.array(         [[1633,1738],
                            [430,1466],
                            [661,1385],
                            [2664,1278]])
h, mask = cv.findHomography(points, pointsReference, cv.RANSAC)
imReg = cv.warpPerspective(im, h, (imReference.shape[1],imReference.shape[0]))
cv.imwrite('imreg.jpg',imReg)
