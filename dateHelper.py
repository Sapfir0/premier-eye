import datetime

def parseFilename(filename):
    numberOfCam, date =  filename.split("_")
    date = date.split(".")[0]

    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    hours = int(date[8:10])
    minuts = int(date[10:12])
    seconds = int(date[12:14])
    
    parsedData = datetime.datetime(year, month, day, hours, minuts, seconds)
    return numberOfCam, parsedData
