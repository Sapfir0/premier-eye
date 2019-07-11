# coding: utf8

import cv2
import pandas as pd
import os
import numpy as np

import settings as cfg
#import neural_network.imageAi as imageAi
from neural_network.maskCNN import Mask
import dateHelper as dh
import services.database_controller as db
import services.file_controller as fileHelper
import datetime, time
from colorama import Fore

def main():
    # послдений обработанный файл = "" as ПОФ
    # for filename in os.listdir(os.getcwd() + "/" + cfg.IMAGE_DIR):
    # если filename==ПОФ # мы не будем экономить на младенцах
    # после обработки добавить файл к массиву отработанных файлов
    # или есть варик парсить filename и ПОФ и если ПОФ произошел раньше чем filename, то обабатываем

    processedFrames = []
    neural_network = Mask()
    while True:
        for filename in os.listdir(os.path.join(os.getcwd(), cfg.IMAGE_DIR)):
            currentImage = os.path.join(cfg.IMAGE_DIR, filename)
            currentDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)

            if filename in processedFrames:
                if (processedFrames == os.listdir(currentDir)):
                    print("Ожидаю")
                    time.sleep(2.5)
                continue # если файлы еще есть, то переходим к следующему

            print(f"Analyzing {currentImage}")

            #Mask CNN
            start_time= time.time()

            rectCoordinates = neural_network.ImageMaskCNNPipeline(filename)

            elapsed_time = time.time() - start_time
            print(Fore.YELLOW + f"--- {elapsed_time} seconds by all image work ---" )

            #DB
            data, numberOfCam = dh.parseFilename(filename)
            centerDown = neural_network.getCenterOfDownOfRectangle(rectCoordinates) #массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
            
            for i in range(0, len(rectCoordinates)): # для каждого объекта, найденного на кадре
                LUy, LUx, RDy, RDx = rectCoordinates[i]
                CDx, CDy = centerDown[i]
                objN = db.Objects(numberOfCam, data, int(LUx), int(LUy), int(RDx), int(RDy), int(CDx), int(CDy))
                db.session.add(objN)

            db.session.commit()
            db.session.flush() # можно один раз добавить
            
            processedFrames.append(filename)

    print(Fore.GREEN + "It's all")

if __name__ == "__main__":
    main()