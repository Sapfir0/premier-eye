import os
import sys
import cv2
import numpy as np
import neural_network.modules.feature_matching as sift
import services.timeChecker as timeChecker
import neural_network.modules.extra as extra
import services.directory as dirs
from settings import Settings as cfg
from neural_network.classes.Image import Image
sys.path.append(cfg.MASK_RCNN_DIR)  # To find local version of the library
from mrcnn.model import MaskRCNN


def _parseR(r):
    detections = []
    for i in range(0, len(r['rois'])):  # ужасно, поправить
        obj = {
            'coordinates': r['rois'][i],
            'type': r['class_ids'][i],
            'scores': r['scores'][i],
            'masks': r['masks'][i]
        }
        detections.append(obj)
    return detections


class Mask(object):
    """
        Mask R-CNN
    """
    SAVE_COLORMAP = False
    CLASS_NAMES = None
    COLORS = None
    objectsFromPreviousFrame = None  # objects in the previous frame
    model = None
    hasOldFrame = False

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
        else:
            filename = os.path.split(inputPath)[1]

        img = Image(inputPath, outputPath=outputPath)
        binaryImage = img.read()

        detections = _parseR(self._humanizeTypes(self._detectByMaskCNN(img)))
        img.addDetections(detections)  # detections тоже

        objectsFromCurrentFrame = img.extractObjects(binaryImage, outputImageDirectory=outputPath, filename=filename)
        signedImg = self._visualize_detections(img)
        # запоминаем найденные изображения, а потом сравниваем их с найденными на следующем кадре
        # if self.hasOldFrame:
        #     sift.checkNewFrame(img, rgb_image, objectsFromCurrentFrame, self.hasOldFrame)  # TODO
        # else:
        #     self.hasOldFrame = True

        img.write(outputPath, signedImg)
        return img

    def _visualize_detections(self, image: Image) -> np.ndarray:
        """
            input: the original image, the full object from the mask cnn neural network, and the object ID, if it came out to get it
            output: an object indicating the objects found in the image, and the image itself, with selected objects and captions
        """
        bgr_image = image.read()
        font = cv2.FONT_HERSHEY_DUPLEX
        for i, currentObject in enumerate(image.objects):
            if currentObject.type not in cfg.AVAILABLE_OBJECTS:
                continue

            y1, x1, y2, x2 = currentObject.coordinates

            lineInClassName = self.CLASS_NAMES.index(currentObject.type)
            color = [int(c) for c in np.array(self.COLORS[lineInClassName]) * 255]  # ух круто
            text = "{}: {:.1f} {}".format(currentObject.type, currentObject.scores * 100, i)

            cv2.rectangle(bgr_image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(bgr_image, text, (x1, y1 - 20), font, 0.8, color, 2)

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
        typesList = []
        for i, obj in enumerate(r['class_ids']):
            if r['class_ids'][i] > len(self.CLASS_NAMES):
                raise Exception("Undefined classId - {}".format(r['class_ids'][i]))

            typesList.append(self.CLASS_NAMES[r['class_ids'][i]])
        r.update({'class_ids': typesList})
        return r
