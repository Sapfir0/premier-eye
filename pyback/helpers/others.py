import os
import helpers.dateHelper as dh 
from colorama import Fore
import wget


def checkNewFile(currentImageDir: str) -> dict:
    """
        input: Directory in which we search for files
        output: A dictionary where the camera number will be associated with an array of images from this camera    
    """
    numbersOfCamers: dict[int, list] = {}  # numberOfCam:files #уточнение: номер камеры обычно идет строкой

    for filename in os.listdir(currentImageDir):
        numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True, getDate=False)

        if numberOfCam in numbersOfCamers.keys():
            numbersOfCamers[numberOfCam].append(filename)
        else:
            numbersOfCamers.update({numberOfCam: [filename]})

    for i in numbersOfCamers.keys():
        numbersOfCamers.update({i: sorted(numbersOfCamers[i])})

    return numbersOfCamers


def parseImageAiData(rectCoordinates: list) -> list:
    boxes = [diction['box_points'] for diction in rectCoordinates]
    return boxes


def existingOutputDir(functionToDecorate):
    def wrapper(fakearg, inputPath, outputPathWithFile):
        outputPath = os.path.split(outputPathWithFile)[0]
        if not os.path.isdir(outputPath):
            os.makedirs(outputPath)
        return functionToDecorate(fakearg, inputPath, outputPathWithFile)
    return wrapper


# юзабилити функции
def downloadAndMove(downloadLink, destinationDir):
    file = wget.download(downloadLink) 
    os.rename(os.path.join(os.getcwd(), file), destinationDir)


def checkExist(mustExistedFile, link):
    if not os.path.exists(mustExistedFile):
        print(Fore.RED + f"{mustExistedFile} isn't exist. Downloading...")
        downloadAndMove(link, mustExistedFile)


def checkVersion(package):
    """
        return version of the package and print it in color
        input: string as name of package OR
               list of string as names of packages
        return dictionary [package: version]
    """
    def checkVersionFromString(stringPackage: str) -> int:
        currentPackage = importlib.import_module(stringPackage)
        version = currentPackage.__version__
        print(Fore.MAGENTA + f"{stringPackage} {version}")
        return version

    import importlib
    if isinstance(package, str):
        version = checkVersionFromString(package)
    elif isinstance(package, list):
        version = {}
        for pkg in package:
            version.update({pkg: checkVersionFromString(pkg)})
    else:
        version = Exception

    return version
