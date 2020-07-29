import brmap
import cv2 as cv
import numpy as np
import copy
import matplotlib.pyplot as plt
cloud=cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\cloud.jpg')
img=np.array(brmap.brMap(cloud)*255,dtype='uint8')
blur = cv.GaussianBlur(img,(5,5),0)
ret,th = cv.threshold(blur,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
contours, hier = cv.findContours(th, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
imContours = copy.deepcopy(cloud)
cv.drawContours(imContours, contours, -1, (0,0,255),2)
# removes contours which are children of other contours
indices = filter(lambda x: hier[0][x][3] < 0, range(len(hier[0])))
contoursFiltered = list(map(lambda x: contours[x],indices))
imFiltered = copy.deepcopy(cloud)
cv.drawContours(imFiltered, contoursFiltered, -1, (0,0,255),2)
# finds bounding rectangles of filtered contours
boundRects = list(map(lambda x: cv.boundingRect(x),contoursFiltered))
for rect in boundRects:
    cv.rectangle(cloud,(rect[0],rect[1]),(rect[0]+rect[2],rect[1]+rect[3]),(0,255,0),2)
cv.imshow('rect',cloud)
cv.imshow('contours',imContours)
cv.imshow('filtered',imFiltered)

##following orb code from opencv docs

img2 = cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\cloud.jpg',cv.IMREAD_GRAYSCALE) # trainImage
for rect in boundRects:

    cloud=cv.imread(r'C:\Users\ktsun\AppData\Local\Programs\Python\Python38-32\cloud.jpg')
    img1 = cloud[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
    
    # Initiate ORB detector
    orb = cv.ORB_create()
    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    
    # create BFMatcher object
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1,des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    # Draw first 10 matches.
    img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.imshow(img3),plt.show()

