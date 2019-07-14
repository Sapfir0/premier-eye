import datetime
import re

def parseFilename(filename, getNumberOfCamera=False):
    numberOfCam, date = 0, datetime
    
    result = re.findall(r'\d_\d{14}\..+', filename) 
    if not result:
        raise ValueError("Wrong date in filename")
    numberOfCam, date =  filename.split("_")
    date = date.split(".")[0]
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    hours = int(date[8:10])
    minuts = int(date[10:12])
    seconds = int(date[12:14])
    parsedData = datetime.datetime(year, month, day, hours, minuts, seconds)
    if getNumberOfCamera:
        return  parsedData, numberOfCam
    else:
        return  parsedData



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