import datetime
import re
import os
from settings import Settings as cfg

def parseFilename(filename, getNumberOfCamera=False, getDate=True):
    numberOfCam, date = 0, datetime

    result = re.findall(r'\d_\d{14}\..+', filename)
    if not result:
        raise ValueError("Wrong date in filename")
    numberOfCam, date = filename.split("_")
    date = date.split(".")[0]
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    hours = int(date[8:10])
    minuts = int(date[10:12])
    seconds = int(date[12:14])
    parsedData = datetime.datetime(year, month, day, hours, minuts, seconds)
    if getNumberOfCamera and getDate:
        return parsedData, numberOfCam
    elif getDate:
        return parsedData
    elif getNumberOfCamera:
        return numberOfCam
    else:
        raise Exception("No parsed data, check arguments")


def checkDateFile(currentImageDir):
    import json
    if os.path.isfile(cfg.dateFile):
        with open(cfg.dateFile, 'r') as f:
            last_processed_date = f.read()  # сверимся с древними свитками
            json_acceptable_string = last_processed_date.replace("'", "\"")
            dateFromFile = json.loads(json_acceptable_string)
            return dateFromFile


def parseDateFromFile(dateFromFile):
    dateFromFile = dateFromFile.strip()
    regexp = r"^\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}"
    result = re.findall(regexp, dateFromFile)
    if not result:
        raise ValueError("Wrong dateFromFile from file")
    date, time = dateFromFile.split(" ")

    year, month, day = date.split("-")
    hours, minuts, seconds = time.split(":")

    parsedData = datetime.datetime(int(year), int(month), int(day),
                                   int(hours), int(minuts), int(seconds))
    return parsedData
