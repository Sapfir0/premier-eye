import helpers.others as others
import datetime
import cv2

from neural_network.classes.Car import Car
from neural_network.classes.Person import Person


class Image(object):
    inputPath: str = None
    outputPath: str = None
    numberOfCam: int = None
    fixationDatetime: datetime.datetime = None
    objects: list = []

    def __new__(cls, inputPath, *args, **kwargs):
        if not others.isImage(inputPath):
            print("This is incorrectly image format. Skipping " + inputPath)
            raise Exception
        return object.__new__(cls)

    def __init__(self, inputPath: str, objectsOnFrame=None, outputPath=None):
        self.inputPath = inputPath
        if outputPath:
            self.outputPath = outputPath

        if objectsOnFrame:
            self.saveDetections(objectsOnFrame)

    def __repr__(self):
        return "{} with objects: {}".format(self.inputPath, self.objects)

    def read(self):
        binaryImage = cv2.imread(self.inputPath)
        return binaryImage

    def getRGBImage(self):
        binaryImage = self.read()
        rgbImage = binaryImage[:, :, ::-1]
        return rgbImage

    def write(self, outputPath, image):
        if outputPath:
            cv2.imwrite(outputPath, image)
        else:
            cv2.imwrite(self.outputPath, image)

    def saveDetections(self, detections):
        for obj in detections:  # {'coordinates': array([526, 341, 719, 440], dtype=int32), 'type': 'person', 'scores': 0.99883527}
            if obj['type'] == "car":
                self.objects.append(Car(obj))
            elif obj['type'] == "person":
                self.objects.append(Person(obj))

    def extractObjects(self, binaryImage, outputImageDirectory=None, filename=None):
        """
            input:
                image - source image \n
                boxes - an array of objects found in the image \n
                in addition: whether to save the received images
            output: an array of images of objects
        """
        import os
        objs = []
        for item in self.objects:
            y1, x1, y2, x2 = item.coordinates
            # вырежет все объекты в отдельные изображения
            cropped = binaryImage[y1:y2, x1:x2]
            objs.append(cropped)
            if outputImageDirectory:
                beforePoint, afterPoint = filename.split(".")
                outputDirPath = os.path.join(os.path.split(outputImageDirectory)[0], "objectsOn" + beforePoint)
                if not os.path.exists(outputDirPath):
                    os.mkdir(outputDirPath)
                coordinates = str(item).replace(" ", ",")
                pathToObjectImage = "{}{}.jpg".format(item.type, coordinates)

                cv2.imwrite(os.path.join(outputDirPath, str(pathToObjectImage)), cropped)
        return objs
