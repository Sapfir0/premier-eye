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
    
    #startedFrame = countCamers(currentImageDir)

    rectCoordinates = None

    def checkNewFile(currentImageDir):
        """
            input: Директория в которой будем искать файлы
            output: Хеш, где номеру камеры будет сопоставлен массив изображений из этой камеры
        """
        numbersOfCamers={} # numberOfCam:files

        for filename in os.listdir(currentImageDir):
            _d, numberOfCam = parseFilename(filename, getNumberOfCamera=True)

            if numberOfCam in numbersOfCamers.keys():
                numbersOfCamers[numberOfCam].append(filename)
            else: 
                numbersOfCamers.update({numberOfCam:[filename]})
        print(numbersOfCamers)
        return numbersOfCamers



    imagesForEachCamer = checkNewFile(currentImageDir)


    while True:
        # можно обходить не одним циклом, а n циклами
        # т.е. в начале считать сколько нам будет нужно циклов
        # добавить назвагние кадра с каждой камеры в свой массив, создать столько потоков, сколько у нас камер
        # и проходить так
        # если добавляется новая камера, то нужно перезапустить прогу
        #import threading

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