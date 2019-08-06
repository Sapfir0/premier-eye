import os
import helpers.dateHelper as dh 
from colorama import Fore
import wget
import requests
import shutil

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


def removeDirectorysFromPath(pathToDir):
    for file in os.listdir(pathToDir):
        subdir = os.path.join(pathToDir, file)
        if os.path.isdir(subdir):
            shutil.rmtree(subdir)


def existingOutputDir(functionToDecorate):
    def wrapper(fakearg, inputPath, outputPathWithFile):
        outputPath = os.path.split(outputPathWithFile)[0]
        if not os.path.isdir(outputPath):
            os.makedirs(outputPath)
        return functionToDecorate(fakearg, inputPath, outputPathWithFile)
    return wrapper


# юзабилити функции
def downloadAndMove(downloadLink, destinationDir='.'):
    file = wget.download(downloadLink) 
    os.rename(os.path.join(os.getcwd(), file), destinationDir)
    return file


def checkExist(mustExistedFile, link):
    if not os.path.exists(mustExistedFile):
        print(Fore.RED + f"{mustExistedFile} isn't exist. Downloading...")
        downloadAndMove(link, mustExistedFile)


def downloadSamples(imagesPath):
    if not os.listdir(imagesPath):
        print(Fore.YELLOW + f"{imagesPath} is empty")
        print(Fore.YELLOW + "Downloading sample")
        samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg",
                   "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
                   "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
        realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
        for i, item in enumerate(samples):  # мы не будет исользовать in, мы же не любим ждать
            downloadAndMove(samples[i], os.path.join(imagesPath, realNames[i]))


def downloadNomeroffNet(NOMEROFF_NET_DIR):
    from git import Repo
    if not os.path.exists(NOMEROFF_NET_DIR):
        Repo.clone_from("https://github.com/ria-com/nomeroff-net.git", NOMEROFF_NET_DIR)
        Repo.clone_from("https://github.com/matterport/Mask_RCNN.git", os.path.join(NOMEROFF_NET_DIR, "Mask_RCNN"))


def checkAvailabilityOfServer(env):
    if env == "development" or "dev":
        r = requests.get(self.pyfrontDevelopmentLink)
    elif env == "production" or "prod":
        r = requests.get(self.pyfrontProductionLink)
    else:
        raise BaseException("Environment not defined")
    if not r.status_code == 200:
        raise ValueError("Server isn't available")


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

def createMustExistedDirs(listOfDirs):
    for dir in listOfDirs:
        if not os.path.exists(dir):
            print(f"{dir} folder isn't exist. Creating..")
            os.makedirs(dir)