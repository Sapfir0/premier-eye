import os
from config import Config as cfg
from datetime import datetime

datetimePattern = '%Y%m%d%H%M%S.jpg'


def recursiveSearch(directory, listOfImages=None):
    if listOfImages is None:
        listOfImages = []
    for files in os.listdir(directory):
        path = os.path.join(directory, files)
        if os.path.isdir(path):
            recursiveSearch(path, listOfImages)
        else:
            listOfImages.append(files)
    return listOfImages


def getOutputDir(filename):
    numberOfCam, dateTime = filename.split("_")
    try:
        dateTime = datetime.strptime(dateTime, datetimePattern)
    except ValueError:
        raise ValueError("Uncorrected filename")
    date = dateTime.date()
    hours = dateTime.hour
    outputFile = os.path.join(cfg.UPLOAD_FOLDER, numberOfCam, str(date), str(hours), filename)
    return outputFile
