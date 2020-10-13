import os
from Common.services.filename import parseFilename, getDate, getHours
from colorama import Fore


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


def parseImageAiData(rectCoordinates: list) -> list:
    boxes = [diction['box_points'] for diction in rectCoordinates]
    return boxes


def isImage(filepath):
    allowed_extension = [".jpg", ".png", ".jpeg"]
    for ext in allowed_extension:
        if filepath.endswith(ext):
            return True
    return False


def getIOdirs(filename, IMAGE_DIR, OUTPUT_DIR_MASKCNN):
    dateTime, numberOfCam = parseFilename(filename, getNumberOfCamera=True)
    date = getDate(filename)
    hours = getHours(filename)
    inputFile = os.path.join(IMAGE_DIR, filename)
    outputFile = os.path.join(OUTPUT_DIR_MASKCNN, numberOfCam, str(date), str(hours), filename)
    print(f"Analyzing {inputFile}")
    return inputFile, outputFile, dateTime
