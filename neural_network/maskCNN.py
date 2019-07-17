import os
from os.path import join
import numpy as np
import matplotlib.pyplot as plt
import cv2
import mrcnn.visualize
import mrcnn.utils
from mrcnn.model import MaskRCNN

import time
from colorama import Fore

from settings import Settings as cfg
import neural_network.modules.feature_matching as sift
from neural_network.modules.heatmap import Heatmap
from neural_network.modules.decart import DecartCoordinates
import services.database_controller as db
import helpers.timeChecker as timeChecker
import neural_network.modules.extra as extra
from neural_network.neural_network import Neural_network


class Mask(Neural_network):
    """
        Mask R-CNN
    """
    objectOnFrames = 0  # сколько кадров мы видели объект(защитит от ложных срабатываний)
    SAVE_COLORMAP = False

    CLASS_NAMES = None
    COLORS = None
    imagesFromPreviousFrame = None  # objects in the previous frame
    model = None
    counter = 0

    def __init__(self):
        with open(cfg.CLASSES_FILE, 'rt') as file:
            self.CLASS_NAMES = file.read().rstrip('\n').split('\n')

        self.COLORS = extra.getRandomColors(self.CLASS_NAMES)
        self.model = MaskRCNN(
            mode="inference",
            model_dir=cfg.LOGS_DIR,
            config=cfg.MaskRCNNConfig())
        self.model.load_weights(cfg.DATASET_DIR, by_name=True)

    @timeChecker.checkElapsedTimeAndCompair(10, 5, 3)
    def pipeline(self, inputPath, outputPath):
        """
            almost main
        """
        if not os.path.isdir(os.path.split(outputPath)[0]):  
            os.mkdir(os.path.split(outputPath)[0])

        image = cv2.imread(inputPath)
        # r['rois'] - array of lower left and upper right corner of founded objects
        r, rgb_image = self.detectByMaskCNN(image)
        imagesFromCurrentFrame = extra.extractObjectsFromR(
            image, r['rois'], saveImage=False)  # почему-то current иногда бывает пустым
        # запоминаем найденные изображения, а потом сравниваем их с найденными
        # на следующем кадре

        self.checkNewFrame(r, rgb_image, imagesFromCurrentFrame)

        cv2.imwrite(outputPath, image)  # IMAGE, а не masked image

        if (self.SAVE_COLORMAP):
            heatmap = Heatmap()
            heatmap.createHeatMap(image, outputPath)

        return r['rois']

    def checkNewFrame(self, r, rgb_image, imagesFromCurrentFrame):
        foundedDifferentObjects = None
        if (self.counter):
            foundedDifferentObjects = self.uniqueObjects(self.imagesFromPreviousFrame, imagesFromCurrentFrame, r)
            print("Столько у нас одниковых обхектов с пердыщуим кадром", len(foundedDifferentObjects))
            countedObj, masked_image = self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'], objectId=foundedDifferentObjects)
        else:
            countedObj, masked_image = self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'])
            self.counter = 1

        self.imagesFromPreviousFrame = imagesFromCurrentFrame

    def uniqueObjects(self, imagesFromPreviousFrame, imagesFromCurrentFrame, r, saveUniqueObjects=False):
        """
            input:
                imagesFromPreviousFrame - an array of objects in the previous frame \n
                imagesFromCurrentFrame - an array of objects on the current frame \n
                r - information about objects obtained with mask rcnn \n
            output: returns an array of objects in both frames.
        """


        foundedUniqueObjects = []
        objectId = 0
        for previousObjects in imagesFromPreviousFrame:
            for currentObjects in imagesFromCurrentFrame:
                if(sift.compareImages(previousObjects, currentObjects)):  # то это один объект
                    obj = {
                        "id": objectId,
                        "type": r['class_ids'][objectId],
                        "coordinates": r['rois'][objectId]
                    }
                    objectId += 1
                    # imagesFromCurrentFrame.remove(currentObjects) #
                    # оптимизация от некита
                    # все, матрицы можем выкидывать
                    foundedUniqueObjects.append(obj)
                    if (saveUniqueObjects):
                        img1 = str(objectId) + ".jpg"
                        img2 = str(objectId) + "N" + ".jpg"
                        cv2.imwrite(
                            join(
                                cfg.OUTPUT_DIR_MASKCNN,
                                img1),
                            previousObjects)

        return foundedUniqueObjects

    def visualize_detections(self, image, masks, boxes, class_ids, scores, objectId="-"):
        """
            input: the original image, the full object from the mask cnn neural network, and the object ID, if it came out to get it
            output: an object indicating the objects found in the image, and the image itself, with selected objects and captions
        """
        # Create a new solid-black image the same size as the original image
        masked_image = np.zeros(image.shape)

        bgr_image = image[:, :, ::-1]
        font = cv2.FONT_HERSHEY_DUPLEX

        person_count = 0
        cars_count = 0
        truck_count = 0
        # Loop over each detected person
        for i in range(boxes.shape[0]):
            classID = class_ids[i]

            if not classID in[1, 3, 4]:
                continue

            if classID == 1:
                person_count += 1
            if classID == 3:
                cars_count += 1
            if classID == 4:
                truck_count += 1

            # Get the bounding box of the current person
            y1, x1, y2, x2 = boxes[i]

            mask = masks[:, :, i]
            color = (1.0, 1.0, 1.0)  # White
            image = mrcnn.visualize.apply_mask(image, mask, color, alpha=0.6)  # рисование маски

            if(classID > len(self.CLASS_NAMES)):
                print(Fore.RED + "Exception: Undefined classId - " + str(classID))
                return -1

            #id = sift.setIdToObject(objectId, i)
            label = self.CLASS_NAMES[classID]
            color = [int(c) for c in np.array(self.COLORS[classID]) * 255]  # ух круто
            text = "{}: {:.1f} {}".format(label, scores[i] * 100, i)

            cv2.rectangle(bgr_image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(bgr_image, text, (x1, y1 - 20), font, 0.8, color, 2)

        rgb_image = bgr_image[:, :, ::-1]

        countedObj = {
            "person": person_count,
            "truck": truck_count,
            "car": cars_count
        }
        # print(countedObj)
        return countedObj, rgb_image.astype(np.uint8)

    def detectByMaskCNN(self, image):
        """
            input: image - the result of cv2.imread (<filename>)
            output: r - dictionary of objects found (r ['masks'], r ['rois'], r ['class_ids'], r ['scores']), detailed help somewhere else
        """
        rgb_image = image[:, :, ::-1]
        r = self.model.detect([rgb_image], verbose=1)[0]  # тут вся магия
        # проверить что будет если сюда подать НЕ ОДНО ИЗОБРАЖЕНИЕ, А ПОТОК
        return r, rgb_image
