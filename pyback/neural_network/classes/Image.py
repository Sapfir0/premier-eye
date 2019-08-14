import helpers.others as others
import datetime

from neural_network.classes.Car import Car
from neural_network.classes.Person import Person
from neural_network.classes.Object import Object

class Image(object):
    inputPath: str = None
    numberOfCam: int = None
    fixationDatetime: datetime.datetime = None
    objects: list = []

    def __new__(cls, inputPath, objectsOnFrames):
        if not others.isImage(inputPath):
            print("This is incorrectly image format. Skipping " + inputPath)
            raise Exception
        return object.__new__(cls)

    def __init__(self, inputPath, objectsOnFrame: list):
        self.inputPath = inputPath
        for obj in objectsOnFrame:
            if obj.type == "car":
                Car()
            else if obj.type == "person":
                Person()

