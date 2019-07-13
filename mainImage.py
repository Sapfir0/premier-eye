# coding: utf8
import time
import os
import cv2
import pandas as pd
import numpy as np

import settings as cfg
from neural_network.maskCNN import Mask
from neural_network.imageAi import ImageAI
import helpers.dateHelper as dh
import services.database_controller as db
from neural_network.modules.decart import DecartCoordinates
def main():
    # или есть варик парсить filename и ПОФ и если ПОФ произошел раньше чем filename, то обабатываем
    processedFrames = []
    neural_network = Mask(); imageAI = ImageAI()
    decart = DecartCoordinates()
    while True:
        for filename in os.listdir(os.path.join(os.getcwd(), cfg.IMAGE_DIR)):
            currentImage = os.path.join(cfg.IMAGE_DIR, filename)
            currentDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)

            if filename in processedFrames:
                if (processedFrames == os.listdir(currentDir)):
                    print("Sleeping")
                    time.sleep(2.5)
                continue # если файлы еще есть, то переходим к следующему

            print(f"Analyzing {currentImage}")

            #Mask CNN
            #rectCoordinates = neural_network.pipeline(filename)
            imageAI.pipeline(filename)
            

            #DB
            #data, numberOfCam = dh.parseFilename(filename)
            #centerDown = decart.getCenterOfDownOfRectangle(rectCoordinates) #массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
            
            # for i in range(0, len(rectCoordinates)): # для каждого объекта, найденного на кадре
            #     LUy, LUx, RDy, RDx = rectCoordinates[i]
            #     CDx, CDy = centerDown[i]
            #     objN = db.Objects(numberOfCam, data, int(LUx), int(LUy), int(RDx), int(RDy), int(CDx), int(CDy))
            #     db.session.add(objN)

            # db.session.commit()
            # db.session.flush() # можно один раз добавить
            
            processedFrames.append(filename)

    print(Fore.GREEN + "It's all")

if __name__ == "__main__":
    main()