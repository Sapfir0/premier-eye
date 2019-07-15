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


def main():
    def countCamers(currentImageDir):
        existedCams = []; counterOfCamers = 0
        for filename in os.listdir(currentImageDir): # пробежимся первый раз и определим сколько у нас камер
            date, numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True)
            if not numberOfCam in existedCams:
                existedCams.append(numberOfCam)
                counterOfCamers+=1
        return counterOfCamers

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
    processedFrames = checkDateFile(currentImageDir)  # парсим filename и ПОФ и если ПОФ произошел раньше чем filename, то обабатываем
    
    threadCount = countCamers(currentImageDir)

    rectCoordinates = None

    while True:
        for filename in os.listdir(currentImageDir):
            currentImage = os.path.join(cfg.IMAGE_DIR, filename)

            if filename in processedFrames:
                if (processedFrames == os.listdir(currentImageDir)):
                    print("Sleeping")
                    time.sleep(2.5)
                continue # если файлы еще есть, то переходим к следующему

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
            
            file_controller.writeInFile(cfg.dateFile, str(data)) # будет стирать содержимое файла каждый кадр

            #DB
            if (cfg.loggingInDB):
                centerDown = decart.getCenterOfDownOfRectangle(rectCoordinates) #массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
                
                for i in range(0, len(rectCoordinates)): # для каждого объекта, найденного на кадре
                    LUy, LUx, RDy, RDx = rectCoordinates[i]
                    CDx, CDy = centerDown[i]
                    objN = db.Objects(numberOfCam, data, int(LUx), int(LUy), int(RDx), int(RDy), int(CDx), int(CDy))
                    db.session.add(objN)

                db.session.commit()
                db.session.flush() # можно один раз добавить
                
            processedFrames.append(filename)


if __name__ == "__main__":
    main()