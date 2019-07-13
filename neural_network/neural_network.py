from abc import ABC, abstractmethod

class neural_networks(ABC):

    @abstractmethod
    @timeChecker.checkElapsedTimeAndCompair(10, 5, 3)
    def pipeline(self, filename):
        
        return NotImplemented


    def extractImages():
        return NotImplemented


    def detectMyObjects():
        return NotImplemented

    def detectObjects():
        return NotImplemented

    def countObjects():
        return NotImplemented


    def __init__(self):
    def pipeline(self, filename):
    def setIdToObject():
    def uniqueObjects(self, imagesFromPreviousFrame, imagesFromCurrentFrame, r, saveUniqueObjects=False):
    def extractObjectsFromR(self, image, boxes, saveImage=False):
    def visualize_detections(self, image, masks, boxes, class_ids, scores, objectId="-"):
    def detectByMaskCNN(self, image):


    def __init__(self):
    def pipeline(self, filename):
    def getBoxesForObjectWithId(self, detections):
    def countObjects(self, detections):
    def detectMyObjects(self, inputName, outputName):



