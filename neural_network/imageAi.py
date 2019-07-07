from imageai.Detection import ObjectDetection
import sys
import time
from io import StringIO #возможно не нужно уже
import settings as cfg
import os

execution_path = os.getcwd()

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath( os.path.join(execution_path ,cfg.DATASET_DIR_IMAGE_AI))
detector.loadModel(detection_speed=cfg.DETECTION_SPEED)

customObjects = detector.CustomObjects(person=True, car=True, truck=True) #указывает на те объекты, которые мы ищем на кадре

def imageAiPipeline(currentImage):
    detections, elapsed_time = imageAi.detectMyObjects(currentImage, cfg.OUTPUT_DIR_IMAGE_AI + filename) 
    countedObj = imageAi.countObjects(detections)
    print(countedObj)
    imageAi.getBoxesForObjectWithId(detections)
    return elapsed_time, countedObj


def getBoxesForObjectWithId(detections):
    boxes = {}
    objectId = 0 # ПЕРЕПИСАТЬ
    for eachObject in detections:
        coordinates = eachObject['box_points'] #массив из 4 значений
        boxes.update({objectId:coordinates})
        objectId+=1
    print(boxes)
    return boxes
       

def countObjects(detections):
    personCount=0; carCount=0; truckCount =0
    for eachObject in detections:
        if(eachObject['name'] == "person"):
            personCount+=1
        if(eachObject['name'] == "car"):
            carCount+=1
        if(eachObject['name'] == "truck"):
            truckCount+=1
    #print("Людей: ", personCount)
    #print("Грузовиков: ",truckCount)
    #print("Машин: ",carCount)
    #print("--------------------------------")
    countedObj = {
        "person": personCount,
        "truck": truckCount,
        "car": carCount
    }
    return countedObj


def detectMyObjects(inputName, outputName):
    start_time = time.time()

    detections = detector.detectCustomObjectsFromImage(
        custom_objects=customObjects,
        input_image=os.path.join(execution_path , inputName), 
        output_image_path=os.path.join(execution_path , outputName),
        minimum_percentage_probability=cfg.MINIMUM_PERCENTAGE_PROBABILITY
        )
    elapsed_time = time.time() - start_time
    #print("--- %s seconds ---" % elapsed_time)
    return detections, elapsed_time



