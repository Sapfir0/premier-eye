from datetime import datetime
import re
import os

datetimePattern = '%Y%m%d%H%M%S.jpg'


def parseFilename(filename: str, getNumberOfCamera=False, getDate=True):
    checkCorrectness(filename)
    numberOfCam, date = filename.split("_")
    parsedData = datetime.strptime(date, datetimePattern)
    if getNumberOfCamera and getDate:
        return parsedData, numberOfCam
    elif getDate:
        return parsedData
    elif getNumberOfCamera:
        return numberOfCam
    else:
        raise Exception("No parsed data, check arguments")


def checkDateFile(dateFile: str):
    import json
    if os.path.isfile(dateFile):
        with open(dateFile, 'r') as f:
            last_processed_date = f.read()  # сверимся с древними свитками
            json_acceptable_string = last_processed_date.replace("'", "\"")
            dateFromFile = json.loads(json_acceptable_string)
            return dateFromFile


def checkCorrectness(filename):
    regexp = r'\d_\d{14}\..+'
    result = re.findall(regexp, filename)
    if not result:
        raise ValueError("Wrong date in filename")


def getDateFromFilename(filename):
    checkCorrectness(filename)
    date = filename.split("_")[1]
    dateTime = datetime.strptime(date, datetimePattern)
    return dateTime


def getDate(filename):
    dateTime = getDateFromFilename(filename)
    return dateTime.date()


def getHours(filename):
    dateTime = getDateFromFilename(filename)
    return dateTime.hour
