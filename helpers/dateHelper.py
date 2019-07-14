import datetime
import re

def parseFilename(filename):
    numberOfCam, date = 0, datetime
    result = re.findall(r'\d_\d{14,14}\..+', filename) 
    if not result:
        print("Strong check arguments")
        return ValueError("Wrong arguments")
    try:
        numberOfCam, date =  filename.split("_")
    except ValueError:
        return ValueError("Wrong arguments")

    else:
        date = date.split(".")[0]
        year = int(date[0:4])
        month = int(date[4:6])
        day = int(date[6:8])
        hours = int(date[8:10])
        minuts = int(date[10:12])
        seconds = int(date[12:14])
        parsedData = datetime.datetime(year, month, day, hours, minuts, seconds)
        return  parsedData, numberOfCam
