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

def main():
    def checkDateFile(currentImageDir):
        processedFrames = []
        if os.path.isfile(cfg.dateFile):
            with open(cfg.dateFile, 'r') as f:
                last_processed_data = f.read() # сверимся с древними свитками
                dateFromFile = dh.parseDateFromFile(last_processed_data) 
                for filename in os.listdir(currentImageDir):
                    frameDate = dh.parseFilename(filename)
                    if (frameDate < dateFromFile): # мы не обработаем никогда старый кадр
                        processedFrames.append(filename)
        return processedFrames
        
    cfg = Settings()
    if (cfg.algorithm): neural_network = Mask()
    else: imageAI = ImageAI()
    decart = DecartCoordinates()


    currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)
    #processedFrames = checkDateFile(currentImageDir)  # ПЕРЕДЕЛАТЬ ПОД СЛОВАРЬ
    processedFrames = {}


    rectCoordinates = None

    @timeChecker.checkElapsedTime
    def checkNewFile(currentImageDir):
        """
            input: Директория в которой будем искать файлы
            output: Хеш, где номеру камеры будет сопоставлен массив изображений из этой камеры
        """
        numbersOfCamers={} # numberOfCam:files

        for filename in os.listdir(currentImageDir):
            _d, numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True)

            if numberOfCam in numbersOfCamers.keys():
                numbersOfCamers[numberOfCam].append(filename)
            else: 
                numbersOfCamers.update({numberOfCam:[filename]})
        print(numbersOfCamers)
        return numbersOfCamers

    def foo(numberOfCam, filenames):

        for filename in filenames:
            if not numberOfCam in processedFrames.keys():
                processedFrames.update({numberOfCam:[]}) # если этого ключа нет, без этой строчки мы бы вылетели на следующей

            for processedFrames in processedFrames[str(numberOfCam)].values():
                if filename in processedFrames: 
                    print("Non implemented sleeping")


                    if (processedFrames[numberOfCam] == os.listdir(currentImageDir)):
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
            
 
            processedFrames.update({numberOfCam:[filename]})
            
            #file_controller.writeInFile(cfg.dateFile, str(data)) # будет стирать содержимое файла каждый кадр




    while True:        
        imagesForEachCamer = checkNewFile(currentImageDir)
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]; filenames = items[1]
            foo(numberOfCam, filenames) # вызывать эту функцию в отдельном потоке для каждого filenames





if __name__ == "__main__":
    main()