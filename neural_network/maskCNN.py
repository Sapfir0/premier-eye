import os
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
import cv2
import mrcnn.visualize
import mrcnn.utils
from mrcnn.model import MaskRCNN

#from pathlib import Path
import time
import colorsys
import random
from colorama import Fore

import settings as cfg
import neural_network.modules.feature_matching as sift
from neural_network.modules.heatmap import Heatmap
from neural_network.modules.decart import DecartCoordinates
import services.database_controller as db

class Mask():
    CLASS_NAMES = None
    COLORS = None
    imagesFromPreviousFrame = None # объекты на предыщуем кадре
    model = None
    objectOnFrames = 0 # сколько кадров мы видели объект(защитит от ложных срабатываний)
    
    counter=0

    def __init__(self):
        with open(cfg.CLASSES_FILE, 'rt') as file:
            self.CLASS_NAMES = file.read().rstrip('\n').split('\n')

        # generate random (but visually distinct) colors for each class label
        hsv = [(i / len(self.CLASS_NAMES), 1, 1.0) for i in range(len(self.CLASS_NAMES))]

        self.COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
        random.seed(42)
        random.shuffle(self.COLORS)

        self.model = MaskRCNN(mode="inference", model_dir=cfg.LOGS_DIR, config=cfg.MaskRCNNConfig())
        self.model.load_weights(cfg.DATASET_DIR, by_name=True)

    def ImageMaskCNNPipeline(self, filename):

        image = cv2.imread(join(cfg.IMAGE_DIR, filename))
        r, rgb_image, elapsed_time2 = self.detectByMaskCNN(image)
        imagesFromCurrentFrame = self.extractObjectsFromR(image, r['rois'], saveImage=False)  #почему-то current иногда бывает пустым
        #print(Fore.LIGHTBLACK_EX + "Длины ", len(r['rois']), " : ", len(imagesFromCurrentFrame) )
        # запоминаем найденные изображения, а потом сравниваем их с найденными на следующем кадре
        #print(Fore.LIGHTBLACK_EX + "Столько объектов на текущем кадре ", len(imagesFromCurrentFrame))

        foundedDifferentObjects = None
        if (self.counter): 
            foundedDifferentObjects = self.uniqueObjects(self.imagesFromPreviousFrame, imagesFromCurrentFrame, r)
            #print(Fore.LIGHTMAGENTA_EX + "Пришедшие с предыдущего кадра объекты:", foundedDifferentObjects)
            countedObj, masked_image = self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'], objectId=foundedDifferentObjects)
        else:
            countedObj, masked_image = self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'])
            self.counter = 1
        #r['rois'] - массив координат левого нижнего и правого верхнего угла у найденных объектов

        self.imagesFromPreviousFrame = imagesFromCurrentFrame
        #print(imagesFromCurrentFrame)

        cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, filename), image ) #IMAGE, а не masked image
        
        if (cfg.SAVE_COLORMAP):
            heatmap = Heatmap()
            heatmap.createHeatMap(image, filename)

        return r['rois']

    def uniqueObjects(self, imagesFromPreviousFrame, imagesFromCurrentFrame, r, saveUniqueObjects=False):
        foundedDifferentObjects = []; objectId = 0
        #print(Fore.RED + str(len(imagesFromCurrentFrame)) + ":" + str(len(imagesFromPreviousFrame)) )
        for previousObjects in imagesFromPreviousFrame:
            for currentObjects in imagesFromCurrentFrame: 
                if( sift.compareImages(previousObjects, currentObjects)  ): # то это один объект
                    object = {
                        "id": objectId,
                        "type":  r['class_ids'][objectId],
                        "coordinates": r['rois'][objectId]
                    }
                    objectId += 1
                    #imagesFromCurrentFrame.remove(currentObjects) # оптимизация от некита
                    foundedDifferentObjects.append(object) # все, матрицы можем выкидывать
                    if (saveUniqueObjects):
                        img1 = str(objectId) + ".jpg"; img2 = str(objectId) +  "N" + ".jpg" 
                        cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, img1), previousObjects )
                        #self.counter=1
        #print(Fore.RED + str(len(imagesFromCurrentFrame)) + ":" + str(len(imagesFromPreviousFrame)) )

        return foundedDifferentObjects

    def extractObjectsFromR(self, image, boxes, saveImage=False):
        objects=[]
        for i in boxes:
            y1, x1, y2, x2 = i 
            cropped = image[y1:y2, x1:x2] # вырежет все объекты в отдельные изображения
            objects.append(cropped)
            if (saveImage): 
                cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, f"{i}.jpg"), cropped )
        return objects


    def getCenterOfDownOfRectangle(self, boxes): # задан левый нижний и правый верхний угол
        allCenters = []
        for i in range(boxes.shape[0]):
            y1, x1, y2, x2 = boxes[i]
            midleDownPoint = [ (x1+x2)/2, y1]
            allCenters.append(midleDownPoint)
        return allCenters


    def visualize_detections(self, image, masks, boxes, class_ids, scores, objectId="-"):
        
        # Create a new solid-black image the same size as the original image
        masked_image = np.zeros(image.shape)

        bgr_image = image[:, :, ::-1]
        font = cv2.FONT_HERSHEY_DUPLEX

        person_count = 0; cars_count = 0; truck_count = 0
        # Loop over each detected person
        for i in range(boxes.shape[0]):
            classID = class_ids[i]

            if not classID in[1,3,4]:
                continue 

            if classID == 1:
                person_count+=1
            if classID == 3:
                cars_count+=1
            if classID == 4:
                truck_count+=1
            
            # Get the bounding box of the current person
            y1, x1, y2, x2 = boxes[i]

            mask = masks[:, :, i]
            color = (1.0, 1.0, 1.0) # White
            image = mrcnn.visualize.apply_mask(image, mask, color, alpha=0.6) # рисование маски

    
            if(classID > len(self.CLASS_NAMES)):
                print(Fore.RED + "Exception: Undefined classId - " + str(classID))
                return -1

            #print("итератор: ", i)
            #print("обджектАйди: ", objectId)
            id = None
            if (i-1 < len(objectId)): # правильно будет меньше либо равен, но попробую юзнуть меьшн
                if (objectId == "-"):
                    id = objectId
                else:
                    if (not len(objectId) == 0):
                        print(i-1, len(objectId))
                        id = objectId[i-1]['id']  # т.к. на первом кадре мы ничего не делаем
                        #print("Приравниваю к: ", id)
                    else:
                        id = "puk"
            else:
                id = "crit"                 
            
            label = self.CLASS_NAMES[classID]
            color = [int(c) for c in np.array(self.COLORS[classID]) * 255] # ух круто
            text = "{}: {:.3f} {}".format(label, scores[i], id)

            cv2.rectangle(bgr_image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(bgr_image, text, (x1, y1-20), font, 0.8, color, 2)        

        rgb_image = bgr_image[:, :, ::-1]

        countedObj = {
            "person": person_count,
            "truck": truck_count,
            "car": cars_count
        }
        #print(countedObj)
        return countedObj, rgb_image.astype(np.uint8)

    def detectByMaskCNN(self, image):
        rgb_image = image[:, :, ::-1]
        start_time= time.time()
        r = self.model.detect([rgb_image], verbose=1)[0] #тут вся магия
        # проверить что будет если сюда подать НЕ ОДНО ИЗОБРАЖЕНИЕ, А ПОТОК
        
        elapsed_time = time.time() - start_time
        print(Fore.GREEN + f"--- {elapsed_time} seconds by detect object with network ---" )
        return r, rgb_image, elapsed_time

