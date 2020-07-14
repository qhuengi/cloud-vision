#might delete this later? is this useful?
import cv2 as cv
import numpy as np
import miscutils
SD_THRESH = 0.03
FIXED_THRESH = 0.025
METHOD = cv.THRESH_BINARY_INV

img = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\B1.jpg')
cv.imshow('img',img)

img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
hyta = miscutils.hytaThreshold(img, SD_THRESH, FIXED_THRESH, METHOD)
cv.imshow('hyta',hyta)

truth = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\B1_GT.jpg')
truth = cv.cvtColor(truth, cv.COLOR_BGR2GRAY)
cv.imshow('truth',truth)

print(cv.matchTemplate(hyta, truth, cv.TM_CCOEFF_NORMED))

while cv.waitKey() == -1:
    pass
cv.destroyAllWindows()
