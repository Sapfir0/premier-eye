import os
import sys
from imageai.Detection import ObjectDetection
import settings as cfg

class ImageAI():
    detector = None
    customObjects = None

    def __init__(self):
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(os.path.join(cfg.APP_PATH, cfg.DATASET_DIR_IMAGE_AI))
        self.detector.loadModel(detection_speed=cfg.DETECTION_SPEED)

        self.customObjects = self.detector.CustomObjects(person=True, car=True, truck=True) #указывает на те объекты, которые мы ищем на кадре

    def pipeline(self, filename):
        detections = self.detectMyObjects(filename, cfg.OUTPUT_DIR_IMAGE_AI + filename) 
        countedObj = self.countObjects(detections)
        print(countedObj)
        self.getBoxesForObjectWithId(detections)
        return countedObj


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
            if(eachObject['name'] == "person"):
                personCount+=1
            if(eachObject['name'] == "car"):
                carCount+=1
            if(eachObject['name'] == "truck"):
                truckCount+=1

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
            minimum_percentage_probability=cfg.MINIMUM_PERCENTAGE_PROBABILITY
            )

        return detections



