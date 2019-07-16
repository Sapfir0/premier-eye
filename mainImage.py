# coding: utf8
import time
import os
import cv2
import pandas as pd
import numpy as np

from settings import Settings
from neural_network.maskCNN import Mask
from neural_network.imageAi import ImageAI
import helpers.dateHelper as dh
import services.database_controller as db
from neural_network.modules.decart import DecartCoordinates
import services.file_controller as file_controller
import helpers.timeChecker as timeChecker

def checkNewFile(currentImageDir):
    """
        input: Directory in which we search for files
        output: A dictionary where the camera number will be associated with an array of images from this camera    
    """
    numbersOfCamers={} # numberOfCam:files

    for filename in os.listdir(currentImageDir):
        numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True, getDate=False)

        if numberOfCam in numbersOfCamers.keys():
            numbersOfCamers[numberOfCam].append(filename)
        else: 
            numbersOfCamers.update({numberOfCam:[filename]})
    return numbersOfCamers
     
def main():

    cfg = Settings()
    if (cfg.algorithm): neural_network = Mask()
    else: imageAI = ImageAI()
    decart = DecartCoordinates()

    currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)

    if (cfg.checkOldProcessedFrames):
        processedFrames = dh.checkDateFile(currentImageDir) 
    else:
        processedFrames = {}

    rectCoordinates = None

    def mainPipeline(numberOfCam, filenames, processedFrames):
        for filename in filenames:
            if not numberOfCam in processedFrames.keys():
                processedFrames.update({numberOfCam:[]}) # если этого ключа нет, без этой строчки мы бы вылетели на следующей

            if filename in processedFrames[str(numberOfCam)]: 
                print("Non implemented sleeping", processedFrames[str(numberOfCam)], filenames)

                if (processedFrames[str(numberOfCam)] == filenames):
                    print(f"Thread {numberOfCam} sleeping")
                    time.sleep(2.5) # ЗАСЫПАЕТ ПОТОК ИСПОЛНЕНИЯ, А НЕ ВСЯ ПРОГА!!!!!!!!!!!!!!!!!!!!!!!!
                continue # если файлы еще есть, то переходим к следующему
            # елси все нормально, и мы не обрабатывали этот кадр, то работаем как обычно

            currentImage = os.path.join(cfg.IMAGE_DIR, filename)
            print(f"Analyzing {currentImage}")
            data, numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True)

            if not os.path.isdir(os.path.join(cfg.OUTPUT_DIR_MASKCNN, numberOfCam)): # хех круто что это здесь
                os.mkdir(os.path.join(cfg.OUTPUT_DIR_MASKCNN, numberOfCam))

            #Mask CNN
            if (cfg.algorithm):
                rectCoordinates = neural_network.pipeline(
                    os.path.join(cfg.IMAGE_DIR, filename),
                    os.path.join(cfg.OUTPUT_DIR_MASKCNN, numberOfCam, filename)
                    )
            else:
                rectCoordinates = imageAI.pipeline(filename)
            
 
            processedFrames[numberOfCam].append(filename)
            
            file_controller.writeInFile(cfg.dateFile, str(processedFrames)) # будет стирать содержимое файла каждый кадр
            return rectCoordinates


    while True:        
        imagesForEachCamer = checkNewFile(currentImageDir) # ГЛАВНЫЙ ПОТОК БУДЕТ ЗАНИМАТЬСЯ ЭТИМ
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]; filenames = items[1]
            mainPipeline(numberOfCam, filenames, processedFrames) # вызывать эту функцию в отдельном потоке для каждого filenames



if __name__ == "__main__":
    main()