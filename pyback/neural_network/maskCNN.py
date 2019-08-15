import os
import sys
from os.path import join
import cv2
from colorama import Fore
import numpy as np

import neural_network.modules.feature_matching as sift
import helpers.timeChecker as timeChecker
import neural_network.modules.extra as extra
from neural_network.neural_network import Neural_network
import helpers.others as others
import helpers.directory as dirs

from settings import Settings as cfg
sys.path.append(cfg.MASK_RCNN_DIR)  # To find local version of the library
import mrcnn.visualize
import mrcnn.utils
from mrcnn.model import MaskRCNN

from neural_network.classes.Image import Image

class Mask(Neural_network):
    """
        Mask R-CNN
    """
    objectOnFrames = 0  # сколько кадров мы видели объект(защитит от ложных срабатываний)
    SAVE_COLORMAP = False

    CLASS_NAMES = None
    COLORS = None
    objectsFromPreviousFrame = None  # objects in the previous frame
    model = None
    counter = 0

    def __init__(self):
        with open(cfg.CLASSES_FILE, 'rt') as file:
            self.CLASS_NAMES = file.read().rstrip('\n').split('\n')

        self.COLORS = extra.getRandomColors(self.CLASS_NAMES)
        self.model = MaskRCNN(mode="inference", model_dir=cfg.LOGS_DIR, config=cfg.MaskRCNNConfig())
        self.model.load_weights(cfg.DATASET_DIR, by_name=True)

    @timeChecker.checkElapsedTimeAndCompair(7, 5, 3, "Mask detecting")
    def pipeline(self, inputPath: str, outputPath: str = None):
        """
            almost main
        """
        if outputPath:
            dirs.createDirs(os.path.split(outputPath)[0])
            filename = os.path.split(outputPath)[1]

        img = Image(inputPath, outputPath=outputPath)
        binaryImage = img.read()

        r, rgb_image = self.detectByMaskCNN(binaryImage)
        # r['rois'] - array of lower left and upper right corner of founded objects
        humanizedTypes = self._humanizeTypes(r['class_ids'])

        detections = self.parseR(r, humanizedTypes)

        img.saveDetections(detections)

        if not outputPath:
            filename = os.path.split(inputPath)[1]
        objectsFromCurrentFrame = img.extractObjectsFromR(
            binaryImage, outputImageDirectory=outputPath, filename=filename)
        # запоминаем найденные изображения, а потом сравниваем их с найденными на следующем кадре
        self._checkNewFrame(r, rgb_image, objectsFromCurrentFrame)

        img.write()
        return img

    def parseR(self, r, humanizedTypes):
        detections = []
        for i in range(0, len(r['rois'])):  # ужасно, поправить
            obj = {
                'coordinates': r['rois'][i],
                'type': humanizedTypes[i],
                'scores': r['scores'][i]
            }
            detections.append(obj)
        return detections

    def _checkNewFrame(self, r, rgb_image, objectsFromCurrentFrame):
        if self.counter:
            foundedDifferentObjects = self._uniqueObjects(self.objectsFromPreviousFrame, objectsFromCurrentFrame, r)
            self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'], objectId=foundedDifferentObjects)
        else:
            self.visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'])
            self.counter = 1

        self.objectsFromPreviousFrame = objectsFromCurrentFrame

    def _uniqueObjects(self, objectsFromPreviousFrame: np.ndarray, objectsFromCurrentFrame: np.ndarray, r: np.ndarray, saveUniqueObjects=False) -> np.ndarray:
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
                        "type": r['class_ids'][objectId],
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

    def _visualize_detections(self, image: np.ndarray, masks: np.ndarray, boxes: np.ndarray, class_ids: np.ndarray, scores: np.ndarray, objectId="-") -> np.ndarray:
        """
            input: the original image, the full object from the mask cnn neural network, and the object ID, if it came out to get it
            output: an object indicating the objects found in the image, and the image itself, with selected objects and captions
        """
        # Create a new solid-black image the same size as the original image
        #masked_image = np.zeros(image.shape)
        bgr_image = image[:, :, ::-1]
        font = cv2.FONT_HERSHEY_DUPLEX

        # Loop over each detected person
        for i in range(boxes.shape[0]):
            classID = class_ids[i]

            if not classID in[1, 3, 4]:
                continue

            # Get the bounding box of the current person
            y1, x1, y2, x2 = boxes[i]

            mask = masks[:, :, i]
            color = (1.0, 1.0, 1.0)  # White
            image = mrcnn.visualize.apply_mask(image, mask, color, alpha=0.6)  # рисование маски

            if classID > len(self.CLASS_NAMES):
                print(Fore.RED + "Exception: Undefined classId - " + str(classID))
                return -1

            #id = sift.setIdToObject(objectId, i)
            label = self.CLASS_NAMES[classID]
            color = [int(c) for c in np.array(self.COLORS[classID]) * 255]  # ух круто
            text = "{}: {:.1f} {}".format(label, scores[i] * 100, i)

            cv2.rectangle(bgr_image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(bgr_image, text, (x1, y1 - 20), font, 0.8, color, 2)

        rgb_image = bgr_image[:, :, ::-1]

        return rgb_image.astype(np.uint8)

    def detectByMaskCNN(self, image: np.ndarray) -> dict: # и еще один, но чет не получается указать два возвращаемых аргумента
        """
            input: image - the result of cv2.imread (<filename>)
            output: r - dictionary of objects found (r ['masks'], r ['rois'], r ['class_ids'], r ['scores']), detailed help somewhere else
        """
        rgb_image = image[:, :, ::-1]
        r = self.model.detect([rgb_image], verbose=1)[0]  # тут вся магия
        # проверить что будет если сюда подать НЕ ОДНО ИЗОБРАЖЕНИЕ, А ПОТОК
        return r, rgb_image

    def _humanizeTypes(self, integerTypes):
        typeOfObject = []
        for i, item in enumerate(integerTypes):
            convertType = self.CLASS_NAMES[integerTypes[i]]
            typeOfObject.append(convertType)
        return typeOfObject