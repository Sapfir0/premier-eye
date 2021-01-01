import requests as _

def detectPlate(fullImagePath):
    return _.get('http://localhost:' + "8080" + "/read" + "?url=" + fullImagePath)