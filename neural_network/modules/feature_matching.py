# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html#py-feature-homography

import numpy as np
import cv2
from matplotlib import pyplot as plt
from settings import Settings as cfg


def setIdToObject(objectId):
    id = None
    if (i-1 < len(objectId)): # правильно будет меньше либо равен, но попробую юзнуть меьшн
        if (objectId == "-"):
            id = objectId
        else:
            if (not len(objectId) == 0):
                print(i-1, len(objectId))
                id = objectId[i-1]['id']  # т.к. на первом кадре мы ничего не делаем
            else:
                id = "puk"
    else:
        id = "crit"               
    
    return NotImplemented


def compareImages(img1, img2):
    """
        Важно, для работы этой функции необходимы opencv contib модули
        input: 2 сравниваемых изображения
        output: результат сравнения [True|False]
    """

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    index_params = dict(algorithm=cfg.FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    counter = 0
    for m, n in matches:
        if m.distance < cfg.cencitivity*n.distance:
            counter += 1

    if counter > cfg.MIN_MATCH_COUNT:
        #print("Enough matches are found - %d/%d" % (counter,cfg.MIN_MATCH_COUNT) )
        return True
    else:
        #print("Not enough matches are found - %d/%d" % (counter,cfg.MIN_MATCH_COUNT) )
        return False


