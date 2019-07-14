import settings as cfg

def writeInFile(filename, *args):
    f = open(filename, 'w')
    for params in args:
        f.write(params + " ")
    f.close()



def writeDatabaseInFile(numberOfCam, fixationTime, rectCoordinates, GPScoordinates, objectId=0 ): #gps - это середина нижней стороны
    f = open(cfg.DATAFILE, 'w')
    print("START ", numberOfCam, fixationTime, rectCoordinates, GPScoordinates, "END")
    f.write(numberOfCam + " ")
    f.write(str(fixationTime) + " ")
    f.write(str(rectCoordinates)+ " ") # запишется не в одну строчку, тут будет перенос
    f.write(str(objectId) + " ")
    f.write(str(GPScoordinates) + " \n")
    f.close()



