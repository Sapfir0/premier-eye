import os
import sys
import cv2
import numpy as np
import services.timeChecker as timeChecker
import services.others as extra
import services.directory as dirs
import mrcnn.config
from config.settings import config
from Models.Image import Image
# sys.path.append(cfg.MASK_RCNN_DIR)  # To find local version of the library
from mrcnn.model import MaskRCNN
from services.classNames import classes
from colorama import Fore
from typing import List
import mrcnn.visualize

def _parseR(r):
    objectsCount = len(r['rois'])
    return [{'coordinates': r['rois'][i],
             'type': r['class_ids'][i],
             'scores': r['scores'][i]} for i in range(objectsCount)]


# Mask cnn advanced
# Configuration that will be used by the Mask-RCNN library
def getMaskConfig(confidence: float):
    class MaskRCNNConfig(mrcnn.config.Config):
        NAME = "coco_pretrained_model_config"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        # минимальный процент отображения прямоугольника
        DETECTION_MIN_CONFIDENCE = confidence
        NUM_CLASSES = len(classes)
        IMAGE_MIN_DIM = 768  # все что ниже пока непонятно
        IMAGE_MAX_DIM = 768
        DETECTION_NMS_THRESHOLD = 0.0  # Не максимальный порог подавления для обнаружения

    return MaskRCNNConfig()


class Mask(object):
    """
        Mask R-CNN
    """
    CLASS_NAMES: List[str] = []
    COLORS: List[str] = []
    model: MaskRCNN = None

    def __init__(self):
        self.CLASS_NAMES = classes
        self.COLORS = extra.getRandomColors(self.CLASS_NAMES)
        model = getMaskConfig(float(config.detectionMinConfidence))
        self.model = MaskRCNN(
            mode="inference", model_dir=config.LOGS_DIR, config=model)
        self.model.load_weights(config.DATASET_DIR, by_name=True)

    @timeChecker.checkElapsedTimeAndCompair(4, 2, 1, "Mask detecting")
    def pipeline(self, inputPath: str, outputPath: str = None):
        """
            almost main
        """
        if outputPath:
            dirs.createDirs(os.path.split(outputPath)[0])
            filename = os.path.split(outputPath)[1]
        else:
            filename = os.path.split(inputPath)[1]

        cameraId = filename.split('_')[0]
        img = Image(inputPath, int(cameraId), outputPath=outputPath)
        binaryImage = img.read()

        rowDetections = self._detectByMaskCNN(img)
        detections = _parseR(self._humanizeTypes(rowDetections))

        img.addDetections(detections) 

        signedImg = self._visualize_detections(img, rowDetections['masks'], drawMask=False)

        img.write(outputPath, signedImg)
        return img

    def _visualize_detections(self, image: Image, masks, drawMask=False) -> np.ndarray:
        """
            input: the original image, the full object from the mask cnn neural network, and the object ID, if it came out to get it
            output: an object indicating the objects found in the image, and the image itself, with selected objects and captions
        """
        bgr_image = image.read()
        font = cv2.FONT_HERSHEY_DUPLEX
        fontScale = 0.8
        thickness = 2

        for i, currentObject in enumerate(image.objects):
            if currentObject.type not in config.availableObjects:
                continue
            y1, x1, y2, x2 = currentObject.coordinates

            lineInClassName = self.CLASS_NAMES.index(currentObject.type)
            color = [int(c)
                     for c in np.array(self.COLORS[lineInClassName]) * 255]
            text = "{}: {:.1f}".format(
                currentObject.type, currentObject.scores * 100)

            if (drawMask):
                mask = masks[:, :, i]   # берем срез
                bgr_image = mrcnn.visualize.apply_mask(bgr_image, mask, color, alpha=0.6) # рисование маски

            cv2.rectangle(bgr_image, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(bgr_image, text, (x1, y1 - 20), font, fontScale, color, thickness)

        return bgr_image.astype(np.uint8)

    def _detectByMaskCNN(self, image: Image):
        """
            input: image - the result of cv2.imread (<filename>)
            output: r - dictionary of objects found (r ['masks'], r ['rois'], r ['class_ids'], r ['scores']), detailed help somewhere else
        """
        rgbImage = image.getRGBImage()
        r = self.model.detect([rgbImage], verbose=1)[0]  # тут вся магия
        # проверить что будет если сюда подать НЕ ОДНО ИЗОБРАЖЕНИЕ, А ПОТОК
        return r

    def _humanizeTypes(self, r: dict) -> dict:
        typesList = [self.CLASS_NAMES[objectClass]
                     for objectClass in r['class_ids']]
        r.update({'class_ids': typesList})
        return r
