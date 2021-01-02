import os
import shutil
from premier_eye_common.filename import parseFilename, getDate, getHours


def createDir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)


def createDirs(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def createDirsFromList(listOfDirs: list):
    for dir in listOfDirs:
        if not os.path.exists(dir):
            print(f"{dir} folder isn't exist. Creating..")
            os.makedirs(dir)


def removeDirectoriesFromPath(pathToDir: str):
    for file in os.listdir(pathToDir):
        subdir = os.path.join(pathToDir, file)
        if os.path.isdir(subdir):
            shutil.rmtree(subdir)


def getIOdirs(filename, IMAGE_DIR, OUTPUT_DIR_MASKCNN):
    dateTime, numberOfCam = parseFilename(filename, getNumberOfCamera=True)
    date = getDate(filename)
    hours = getHours(filename)
    inputFile = os.path.join(IMAGE_DIR, filename)
    outputFile = os.path.join(OUTPUT_DIR_MASKCNN, numberOfCam, str(date), str(hours), filename)
    print(f"Analyzing {inputFile}")
    return inputFile, outputFile, dateTime


def checkNewFile(currentImageDir: str, IMAGE_PATH_WHITELIST) -> dict:
    """
        input: Directory in which we search for files
        output: A dictionary where the camera number will be associated with an array of images from this camera
        files in whitelist will be ignored
    """
    numbersOfCamers: dict[int, list] = {}  # numberOfCam:files #уточнение: номер камеры обычно идет строкой

    for filename in os.listdir(currentImageDir):
        if filename in IMAGE_PATH_WHITELIST:
            continue
        else:
            numberOfCam = parseFilename(filename, getNumberOfCamera=True, getDate=False)

        if numberOfCam in numbersOfCamers.keys():
            numbersOfCamers[numberOfCam].append(filename)
        else:
            numbersOfCamers.update({numberOfCam: [filename]})

    for i in numbersOfCamers.keys():
        numbersOfCamers.update({i: sorted(numbersOfCamers[i])})

    return numbersOfCamers
