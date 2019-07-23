import os
import helpers.dateHelper as dh 
from colorama import Fore
import wget

def checkNewFile(currentImageDir):
    """
        input: Directory in which we search for files
        output: A dictionary where the camera number will be associated with an array of images from this camera    
    """
    numbersOfCamers = {}  # numberOfCam:files

    for filename in os.listdir(currentImageDir):
        numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True, getDate=False)

        if numberOfCam in numbersOfCamers.keys():
            numbersOfCamers[numberOfCam].append(filename)
        else:
            numbersOfCamers.update({numberOfCam: [filename]})

    for i in numbersOfCamers.keys():
        numbersOfCamers.update({i: sorted(numbersOfCamers[i])})

    return numbersOfCamers
    
def parseImageAiData(rectCoordinates):
    boxes = []
    for diction in rectCoordinates:
        boxes.append(diction['box_points'])
    return boxes


def existingOutputDir(functionToDecorate):
    def wrapper(fakearg, inputPath, outputPath):
        if not os.path.isdir(os.path.split(outputPath)[0]):  
            os.makedirs(os.path.split(outputPath)[0])
        return functionToDecorate(fakearg, inputPath, outputPath)

    return wrapper


# юзабилити функции
def downloadAndMove(downloadLink, destinationDir):
    file = wget.download(downloadLink) 
    os.rename(os.path.join(os.getcwd(), file), destinationDir)

def checkExist(mustExistedFile, link):
    if not os.path.exists(mustExistedFile):
        print(Fore.RED + f"{mustExistedFile} isn't exist. Downloading...")
        downloadAndMove(link, mustExistedFile)
    