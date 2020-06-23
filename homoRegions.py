import cv2
import numpy as np


MAX_FEATURES_PER_REGION = 100
GOOD_MATCH_PERCENT = 0.15
REGIONS_PER_ROW = 4

def alignImages(im1, im2):

  # Convert images to grayscale
  im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
  im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

  # Detect ORB features and compute descriptors.
  orb = cv2.ORB_create(MAX_FEATURES_PER_REGION)
  keypoints1=[]
  keypoints2=[]
  descriptors1=[]
  descriptors2=[]
  windowHeight = int(im1Gray.shape[0] / REGIONS_PER_ROW)
  windowWidth = int(im1Gray.shape[1] / REGIONS_PER_ROW)
  for i in range(REGIONS_PER_ROW):
    for j in range(REGIONS_PER_ROW):
      cornerY = i*windowHeight
      cornerX = j*windowWidth
      keypointsWindow1, descriptorsWindow1 = orb.detectAndCompute(im1Gray[cornerY:cornerY+windowHeight,cornerX:cornerX+windowWidth],None)
      keypointsWindow2, descriptorsWindow2 = orb.detectAndCompute(im2Gray[cornerY:cornerY+windowHeight,cornerX:cornerX+windowWidth],None)
      if len(keypointsWindow1):
        keypoints1.extend(keypointsWindow1)
        descriptors1.extend(descriptorsWindow1)
      if len(keypointsWindow2):
        keypoints2.extend(keypointsWindow2)
        descriptors2.extend(descriptorsWindow2)
  descriptors1=np.array(descriptors1)
  descriptors2=np.array(descriptors2)
  keypoints1=np.array(keypoints1)
  keypoints2=np.array(keypoints2)
  # Match features.
  matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
  matches = matcher.match(descriptors1, descriptors2, None)
  
  # Sort matches by score
  matches.sort(key=lambda x: x.distance, reverse=False)

  # Remove not so good matches
  numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
  matches = matches[:numGoodMatches]

  # Draw top matches
  imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
  cv2.imwrite("matches.jpg", imMatches)
  
  # Extract location of good matches
  points1 = np.zeros((len(matches), 2), dtype=np.float32)
  points2 = np.zeros((len(matches), 2), dtype=np.float32)

  for i, match in enumerate(matches):
    points1[i, :] = keypoints1[match.queryIdx].pt
    points2[i, :] = keypoints2[match.trainIdx].pt
  
  # Find homography
  h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

  # Use homography
  height, width, channels = im2.shape
  im1Reg = cv2.warpPerspective(im1, h, (width, height))
  
  return im1Reg, h


if __name__ == '__main__':
  
  # Read reference image
  refFilename = r'D:\Users\me\Downloads\3.jpg'
  print("Reading reference image : ", refFilename)
  imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

  # Read image to be aligned
  imFilename = r'D:\Users\me\Downloads\4.jpg'
  print("Reading image to align : ", imFilename);  
  im = cv2.imread(imFilename, cv2.IMREAD_COLOR)
  
  print("Aligning images ...")
  # Registered image will be resotred in imReg. 
  # The estimated homography will be stored in h. 
  imReg, h = alignImages(im, imReference)
  
  # Write aligned image to disk. 
  outFilename = "aligned.jpg"
  print("Saving aligned image : ", outFilename);
  cv2.imshow('',imReg)
  cv2.imwrite(outFilename, imReg)

  # Print estimated homography
  print("Estimated homography : \n",  h)

  retval, rotations, translations, normals = decomposeHomographyMat(h, k)
