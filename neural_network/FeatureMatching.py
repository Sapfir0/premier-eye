# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html#py-feature-homography

import numpy as np
import cv2
from matplotlib import pyplot as plt

def compareImages(img1, img2):
    MIN_MATCH_COUNT = 50 # меньше этого числа совпадений, будем считать что объекты разные
    FLANN_INDEX_KDTREE = 0 # алгоритм
    cencitivity=0.7

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < cencitivity*n.distance:
            good.append(m)

    if len(good)>MIN_MATCH_COUNT:
        print("Enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT) )
    else:
        print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT) )


