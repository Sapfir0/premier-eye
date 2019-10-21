import datetime
import re
import os


def parseFilename(filename: str, getNumberOfCamera=False, getDate=True):
    result = re.findall(r'\d_\d{14}\..+', filename)
    if not result:
        raise ValueError("Wrong date in filename")
    numberOfCam, date = filename.split("_")
    parsedData = datetime.datetime.strptime(date, '%Y%m%d%H%M%S.jpg')
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


def getDateOrHours(filename: str, getHours=True, getDate=True):
    result = re.findall(r'\d_\d{14}\..+', filename)
    if not result:
        raise ValueError("Wrong date in filename")

    n, date = filename.split("_")
    date = date.split(".")[0]
    parsedData = date[0:8]
    hours = date[8:10]

    if getHours and getDate:
        return parsedData, hours
    elif getDate:
        return parsedData
    elif getHours:
        return hours
    else:
        raise Exception("No parsed data, check arguments")
