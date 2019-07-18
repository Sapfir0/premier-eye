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
from threading import Thread

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



def main():

    cfg = Settings()
    if (cfg.algorithm):
        neural_network = Mask()
    else:
        imageAI = ImageAI()
    decart = DecartCoordinates()

    currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)

    if (cfg.checkOldProcessedFrames):
        processedFrames = dh.checkDateFile(currentImageDir) 
    else:
        processedFrames = {}

    rectCoordinates = None

    @timeChecker.checkElapsedTimeAndCompair(7, 6, 4, "Обработка одного кадра")
    def mainPipeline(numberOfCam, filenames, processedFrames):
        for filename in filenames:
            if numberOfCam not in processedFrames.keys():
                processedFrames.update({numberOfCam: []})

            if filename in processedFrames[numberOfCam]:
                if (processedFrames[numberOfCam] == filenames):
                    print(f"Thread {numberOfCam} sleeping")
                    time.sleep(2.5)  # засыпает поток исполнения
                continue  # если файлы еще есть, то переходим к следующему

            currentImage = os.path.join(cfg.IMAGE_DIR, filename)
            print(f"Analyzing {currentImage}")
            date, numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True)

            # Mask CNN
            if (cfg.algorithm):
                print(f"Поток {numberOfCam} имеет на входе {os.path.join(cfg.IMAGE_DIR, filename)} и на выходе {os.path.join(cfg.OUTPUT_DIR_MASKCNN, numberOfCam, filename)}")

                rectCoordinates = neural_network.pipeline(
                    os.path.join(cfg.IMAGE_DIR, filename),
                    os.path.join(cfg.OUTPUT_DIR_MASKCNN, numberOfCam, filename)
                )
            else: #image ai
                rectCoordinates = imageAI.pipeline(
                    os.path.join(cfg.IMAGE_DIR, filename),
                    os.path.join(cfg.OUTPUT_DIR_IMAGE_AI, numberOfCam, filename)
                )
                rectCoordinates = parseImageAiData(rectCoordinates)

            # car detector                 
            if cfg.CAR_NUMBER_DETECTOR:
                import car_number
                if numberOfCam in [str(1), str(2)]:  # если камера №2 или №1, то запускем тест на номера
                    carNumber, boxes = car_number.detectCarNumber(os.path.join(cfg.IMAGE_DIR, filename))

            processedFrames[numberOfCam].append(filename)
           
            file_controller.writeInFile(cfg.dateFile, str(processedFrames))  # будет стирать содержимое файла каждый кадр
           
            # DB
            if (cfg.loggingInDB):
                centerDown = decart.getCenterOfDownOfRectangle(rectCoordinates)  # массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
                for i in range(0, len(rectCoordinates)):  # для каждого объекта, найденного на кадре
                    db.writeInfoForObjectInDB(numberOfCam, date, rectCoordinates[i], centerDown[i])
 
            return rectCoordinates


    while True:
        imagesForEachCamer = checkNewFile(currentImageDir)  # этим занимается главный поток
        arrayOfThreads = []
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]
            filenames = items[1]
            mainPipeline(numberOfCam, filenames, processedFrames)
            #threadI = Thread(target=mainPipeline, args=(numberOfCam, filenames, processedFrames), name=numberOfCam)
            #arrayOfThreads.append(threadI)

        # for i in arrayOfThreads:
        #     print(i)
        #     i.start()

       # break
            # странно, если написать и потоковую версию и обычную, то все будет выполняться в 2 потока
        
if __name__ == "__main__":
    main()
