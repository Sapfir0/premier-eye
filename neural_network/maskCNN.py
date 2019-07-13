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
from colorama import Fore

import settings as cfg
import neural_network.modules.feature_matching as sift
from neural_network.modules.heatmap import Heatmap
from neural_network.modules.decart import DecartCoordinates
import services.database_controller as db
import helpers.timeChecker as timeChecker
import neural_network.modules.extra as extra
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

        self.COLORS = extra.getRandomColors(self.CLASS_NAMES)
        self.model = MaskRCNN(mode="inference", model_dir=cfg.LOGS_DIR, config=cfg.MaskRCNNConfig())
        self.model.load_weights(cfg.DATASET_DIR, by_name=True)
    
    @timeChecker.checkElapsedTimeAndCompair(10, 5, 3)
    def pipeline(self, filename):
        """
            Считай, почти мейн
        """
        image = cv2.imread(join(cfg.IMAGE_DIR, filename))
        r, rgb_image= self.detectByMaskCNN(image)
        imagesFromCurrentFrame = self.extractObjectsFromR(image, r['rois'], saveImage=False)  #почему-то current иногда бывает пустым
        # запоминаем найденные изображения, а потом сравниваем их с найденными на следующем кадре

        foundedDifferentObjects = None
        if (self.counter): 
            foundedDifferentObjects = self.uniqueObjects(self.imagesFromPreviousFrame, imagesFromCurrentFrame, r)
            countedObj, masked_image = self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'], objectId=foundedDifferentObjects)
        else:
            countedObj, masked_image = self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'])
            self.counter = 1
        #r['rois'] - массив координат левого нижнего и правого верхнего угла у найденных объектов

        self.imagesFromPreviousFrame = imagesFromCurrentFrame

        cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, filename), image ) #IMAGE, а не masked image
        
        if (cfg.SAVE_COLORMAP):
            heatmap = Heatmap()
            heatmap.createHeatMap(image, filename)

        return r['rois']

    def setIdToObject():
        return NotImplemented

    def uniqueObjects(self, imagesFromPreviousFrame, imagesFromCurrentFrame, r, saveUniqueObjects=False):
        """
            input: 
            imagesFromPreviousFrame - массив объектов на предыдущем кадре \n
            imagesFromCurrentFrame  - массив объектов на текущем кадре \n
            r - информация об объектах, полученная с mask rcnn \n
            output: вернет массив объектов, которые есть на обоих кадрах
        """
        obj = {
            "id": None,
            "type":  None,
            "coordinates": None
        }

        foundedUniqueObjects = []; objectId = 0
        for previousObjects in imagesFromPreviousFrame:
            for currentObjects in imagesFromCurrentFrame: 
                if( sift.compareImages(previousObjects, currentObjects)  ): # то это один объект
                    obj.id = objectId; obj.type = r['class_ids'][objectId]; obj.coordinates = r['rois'][objectId]
                    objectId += 1
                    #imagesFromCurrentFrame.remove(currentObjects) # оптимизация от некита
                    foundedUniqueObjects.append(obj) # все, матрицы можем выкидывать
                    if (saveUniqueObjects):
                        img1 = str(objectId) + ".jpg"; img2 = str(objectId) +  "N" + ".jpg" 
                        cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, img1), previousObjects )

        return foundedUniqueObjects

    def extractObjectsFromR(self, image, boxes, saveImage=False):
        """
            input: image - исходное изображение \n
                boxes - массив найденных объектов на изображении \n 
                дополнительно: сохранять ли полученные изображения
            output: массив изображений объектов
        """

        objects=[]
        for i in boxes:
            y1, x1, y2, x2 = i 
            cropped = image[y1:y2, x1:x2] # вырежет все объекты в отдельные изображения
            objects.append(cropped)
            if (saveImage): 
                cv2.imwrite(join(cfg.OUTPUT_DIR_MASKCNN, f"{i}.jpg"), cropped )
        return objects

    def visualize_detections(self, image, masks, boxes, class_ids, scores, objectId="-"):
        """
            input: исходное изображение, полный объект из нейросети mask cnn, и айдишник объекта, если получилось его получить
            output: объект с указанием найденных объектов на изображении, и само изображение, с выделенными объектами и подписями
        """
        # Create a new solid-black image the same size as the original image
        masked_image = np.zeros(image.shape)

        bgr_image = image[:, :, ::-1]
        font = cv2.FONT_HERSHEY_DUPLEX

        person_count = 0; cars_count = 0; truck_count = 0
        # Loop over each detected person
        for i in range(boxes.shape[0]):
            classID = class_ids[i]

            if not classID in[1, 3, 4]:
                continue 

            if classID == 1: person_count+=1
            if classID == 3: cars_count+=1
            if classID == 4: truck_count+=1
            
            # Get the bounding box of the current person
            y1, x1, y2, x2 = boxes[i]

            mask = masks[:, :, i]
            color = (1.0, 1.0, 1.0) # White
            image = mrcnn.visualize.apply_mask(image, mask, color, alpha=0.6) # рисование маски

            if(classID > len(self.CLASS_NAMES)):
                print(Fore.RED + "Exception: Undefined classId - " + str(classID))
                return -1

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
        """
            input: image - результат работы cv2.imread(<filename>)
            output: r - словарь найденных объектов (r['masks'], r['rois'], r['class_ids'], r['scores']), подробная справка где-то еще
        """
        rgb_image = image[:, :, ::-1]
        r = self.model.detect([rgb_image], verbose=1)[0] #тут вся магия
        # проверить что будет если сюда подать НЕ ОДНО ИЗОБРАЖЕНИЕ, А ПОТОК
        return r, rgb_image

