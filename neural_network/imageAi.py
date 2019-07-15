import os
import sys
import cv2
from imageai.Detection import ObjectDetection
from os.path import join
import numpy as np

from neural_network.neural_network import Neural_network
import neural_network.modules.feature_matching as sift
import helpers.timeChecker as timeChecker
from settings import Settings as cfg

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
        #print()
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

    previous_extracted_objects = None
    def extractObjects(self, inputName, outputName, saveImage=False):
        returned_image, detections, current_extracted_objects = self.detector.detectObjectsFromImage(
            input_image=inputName, 
            output_type="array", 
            extract_detected_objects=True, 
            minimum_percentage_probability=cfg.DETECTION_MIN_CONFIDENCE)
        #print(returned_image, detections, extracted_objects)
        currentObjectFromFrame = []

        # for i in current_extracted_objects:
        #     cv2.imwrite(join(cfg.OUTPUT_DIR_IMAGE_AI, "1.jpg"), i)
        if (self.previous_extracted_objects):
            for current in current_extracted_objects:
                for previous in self.previous_extracted_objects:
                    #print(Fore.LIGHTCYAN_EX + str(previous), str(current))
                    print(previous)
                    sift.compareImages(previous, current)


        boxes=[]
        for i in detections:
            boxes.append(i['box_points'])

        self.previous_extracted_objects = current_extracted_objects
        return boxes
        
    def uniqueObjects(self, imagesFromPreviousFrame, imagesFromCurrentFrame, r):
        #previousObject = cv2.imread(imagesFromPreviousFrame)
        #currentObject = cv2.imread(imagesFromCurrentFrame) 
        foundedUniqueObjects = []; objectId = 0
        obj = {
            "id": None,
            "type":  None,
            "coordinates": None
        }
        if( sift.compareImages(imagesFromPreviousFrame, imagesFromCurrentFrame)  ): # то это один объект
            print("Уникально")
            #obj['id'] = objectId; obj['type'] = r['name']; obj['coordinates'] = r['box_points']
            #objectId += 1
            #foundedUniqueObjects.append(obj) # все, матрицы можем выкидывать

        return foundedUniqueObjects