import os
import shutil


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


