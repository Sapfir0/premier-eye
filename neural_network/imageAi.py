import os
import sys
from imageai.Detection import ObjectDetection
import settings as cfg
from os.path import join
from neural_network.neural_network import Neural_network
import cv2
import numpy as np
import neural_network.modules.feature_matching as sift
import helpers.timeChecker as timeChecker

class ImageAI(Neural_network):
    detector = None
    customObjects = None

    def __init__(self):
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(cfg.APP_PATH, cfg.DATASET_DIR_IMAGE_AI))
        self.detector.loadModel(detection_speed=cfg.DETECTION_SPEED)

        self.customObjects = self.detector.CustomObjects(person=True, car=True, truck=True) #указывает на те объекты, которые мы ищем на кадре

    @timeChecker.checkElapsedTimeAndCompair(10, 5, 3)
    def pipeline(self, filename):
        super().pipeline(filename)
        #detections = self.detectMyObjects(join(cfg.IMAGE_DIR, filename), join(cfg.OUTPUT_DIR_IMAGE_AI, filename)) 
        boxes = self.extractObjects(join(cfg.IMAGE_DIR, filename), join(cfg.OUTPUT_DIR_IMAGE_AI, filename))
        #countedObj = self.countObjects(detections)
        #boxes = self.getBoxesForObjectWithId(detections)
        return boxes


    def getBoxesForObjectWithId(self, detections):
        boxes = {}
        objectId = 0 # ПЕРЕПИСАТЬ
        for eachObject in detections:
            coordinates = eachObject['box_points'] #массив из 4 значений
            boxes.update({objectId:coordinates})
            objectId+=1
        print(boxes)
        return boxes
        

    def countObjects(self, detections):
        personCount=0; carCount=0; truckCount =0
        for eachObject in detections:
            if(eachObject['name'] == "person"): personCount+=1
            if(eachObject['name'] == "car"): carCount+=1
            if(eachObject['name'] == "truck"): truckCount+=1

        countedObj = {
            "person": personCount,
            "truck": truckCount,
            "car": carCount
        }
        return countedObj


    def detectMyObjects(self, inputName, outputName):

        detections = self.detector.detectCustomObjectsFromImage(
            custom_objects=self.customObjects,
            input_image=os.path.join(cfg.APP_PATH, inputName),
            output_image_path=os.path.join(cfg.APP_PATH, outputName),
            minimum_percentage_probability=cfg.DETECTION_MIN_CONFIDENCE
            )

        return detections
    previous_objects_path = None
    def extractObjects(self, inputName, outputName, saveImage=False):
        detections, current_objects_path = self.detector.detectObjectsFromImage(
            input_image=os.path.join(cfg.APP_PATH, inputName),
            output_image_path=os.path.join(cfg.APP_PATH, outputName),
            minimum_percentage_probability=cfg.DETECTION_MIN_CONFIDENCE,
            extract_detected_objects=True
            )
        #currentObjectFromFrame = []
        if self.previous_objects_path:
            for current in current_objects_path:
                for previous in self.previous_objects_path:
                    self.uniqueObjects(current, previous, detections)

        print(detections)
        print(current_objects_path)
        boxes=[]
        for i in detections:
            boxes.append(i['box_points'])

        self.previous_objects_path = current_objects_path
        return boxes
        
    def uniqueObjects(self, imagesFromPreviousFrame, imagesFromCurrentFrame, r):
        previousObject = cv2.imread(imagesFromPreviousFrame)
        currentObject = cv2.imread(imagesFromCurrentFrame) 
        foundedUniqueObjects = []; objectId = 0
        obj = {
            "id": None,
            "type":  None,
            "coordinates": None
        }
        if( sift.compareImages(previousObject, currentObject)  ): # то это один объект
            obj['id'] = objectId; obj['type'] = r['name']; obj['coordinates'] = r['box_points']
            objectId += 1
            foundedUniqueObjects.append(obj) # все, матрицы можем выкидывать

        print(foundedUniqueObjects)
        return foundedUniqueObjects