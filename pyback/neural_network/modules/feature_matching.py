# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html#py-feature-homography

import cv2
from settings import Settings as cfg

lastObjectId = 0
def setIdToObject(objectId, i):
    print(objectId)
    if not isinstance(objectId, list):
        return "-"
    if objectId[i] <= lastObjectId:
        lastObjectId = objectId
        objectId = lastObjectId+1
    
    print(i >= len(objectId), i, len(objectId))
    if i >= len(objectId):
        return i

    id = objectId[i]['id']

    return id


def checkNewFrame(r, rgb_image, objectsFromCurrentFrame, hasOldFrames=False):
    """
    :param r:
    :param rgb_image:
    :param objectsFromCurrentFrame: матрицы объектов с текущего кадра
    :return:
    """
    if not hasOldFrames:
        foundedDifferentObjects = uniqueObjects(self.objectsFromPreviousFrame, objectsFromCurrentFrame, r)
        self._visualize_detections(rgb_image, image)
    else:
        self._visualize_detections(rgb_image, image)
        self.counter = 1

    self.objectsFromPreviousFrame = objectsFromCurrentFrame


def uniqueObjects(objectsFromPreviousFrame: np.ndarray, objectsFromCurrentFrame: np.ndarray, r: np.ndarray,
                   saveUniqueObjects=False) -> np.ndarray:
    """
        input:
            objectsFromPreviousFrame - an array of objects in the previous frame \n
            objectsFromCurrentFrame - an array of objects on the current frame \n
            r - information about objects obtained with mask rcnn \n
        output: returns an array of objects in both frames.
    """
    foundedUniqueObjects = []
    objectId = 0
    for previousObjects in objectsFromPreviousFrame:
        for currentObjects in objectsFromCurrentFrame:
            if sift.compareImages(previousObjects, currentObjects):  # то это один объект
                obj = {
                    "id": objectId,
                    "type": r['class_ids'][objectId],  # TODO исправить!!!
                    "coordinates": r['rois'][objectId]
                }
                objectId += 1
                # все, матрицы можем выкидывать
                foundedUniqueObjects.append(obj)
                if saveUniqueObjects:
                    img1 = str(objectId) + ".jpg"
                    img2 = str(objectId) + "N" + ".jpg"
                    cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, img1),
                                previousObjects)

    return foundedUniqueObjects



def compareImages(img1, img2):
    """
        OpenCV Contrib Modules
        input: 2 compared images
        conclusion: the result of the comparison [True | False]
    """
    print(img1, "jigjsdjgidsigjsijgsdjgijgsjgjsdijgisjgs", img2)
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1, None)
    kp2, des2 = sift.detectAndCompute(img2, None)

    indexParams = dict(algorithm=cfg.FLANN_INDEX_KDTREE, trees=5)
    searchParams = dict(checks=50)

    flann = cv2.FlannBasedMatcher(indexParams, searchParams)

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
