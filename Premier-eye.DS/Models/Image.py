import services.others as others
import datetime
import cv2
import services.dateHelper as dh
import os
from Models.Car import Car
from Models.Person import Person
from premier_eye_common.filename import getDateFromFilename
import matplotlib.pyplot as plt


class Image(object):
    inputPath: str = ""
    filename: str = ""
    date = None
    outputPath: str = ""
    objects: list = []
    cameraId: int = 0

    def __new__(cls, inputPath, *args, **kwargs):
        if not others.isImage(inputPath):
            raise Exception("This is incorrectly image format. Skipping " + inputPath)
        return object.__new__(cls)

    def __init__(self, inputPath: str, camerasId: int, objectsOnFrame=None, outputPath=None):
        self.filename = os.path.split(inputPath)[1]
        self.date = getDateFromFilename(self.filename)
        self.cameraId = camerasId
        self.inputPath = inputPath
        if outputPath:
            self.outputPath = outputPath

        if objectsOnFrame:
            self.addDetections(objectsOnFrame)

    def __repr__(self):
        return f"{self.inputPath}  with objects: {self.objects}"

    def json(self):
        return [obj.json() for obj in self.objects]

    def read(self):
        return cv2.imread(self.inputPath)

    def getRGBImage(self):
        binaryImage = self.read()
        return binaryImage[:, :, ::-1]

    def write(self, outputPath, image):
        if outputPath:
            cv2.imwrite(outputPath, image)
        else:
            cv2.imwrite(self.outputPath, image)

    def addDetections(self, detections):
        self.objects = []
        for obj in detections:  # {'coordinates': array([526, 341, 719, 440], dtype=int32), 'type': 'person', 'scores': 0.99883527}
            if obj['type'] == "car":
                self.objects.append(Car(obj))
            elif obj['type'] == "person":
                self.objects.append(Person(obj))

    def saveImageByPlot(self, outputPath, image):
        """
        plot image saving
        """
        fig = plt.figure(frameon=False)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(image)

        if outputPath:
            fig.savefig(outputPath)
        else:
            fig.savefig(self.outputPath)
