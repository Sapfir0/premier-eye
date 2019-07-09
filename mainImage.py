# coding: utf8

import cv2
import pandas as pd
import os
import numpy as np

import settings as cfg
#import neural_network.imageAi as imageAi
import neural_network.maskCNN as mask
import dateHelper as dh
import db.fileHelper as fileHelper


import datetime, time
def main():
    # послдений обработанный файл = "" as ПОФ
    # for filename in os.listdir(os.getcwd() + "/" + cfg.IMAGE_DIR):
    # если filename==ПОФ # мы не будем экономить на младенцах
    # после обработки добавить файл к массиву отработанных файлов
    # или есть варик парсить filename и ПОФ и если ПОФ произошел раньше чем filename, то обабатываем
    last_date_rendered_frame = datetime.datetime(1970, 1, 1)
    processedFrames = []
    while True:
        for filename in os.listdir(os.path.join(os.getcwd(), cfg.IMAGE_DIR)):
            currentImage= f"{cfg.IMAGE_DIR}/{filename}"
            currentDir = f"{os.getcwd()}/{cfg.IMAGE_DIR}"

            if filename in processedFrames:
                if (processedFrames == os.listdir(os.path.join(os.getcwd(), cfg.IMAGE_DIR))):
                    print("Ожидаю")
                    time.sleep(2.5)
                continue

            print(f"Analyzing {currentImage}")

            #Mask CNN
            rectCoordinates = mask.ImageMaskCNNPipeline(filename)

            #DB
            #r['rois'] - массив координат левого нижнего и правого верхнего угла у надейнных объектов
            data, numberOfCam = dh.parseFilename(filename)
            centerDown = mask.getCenterOfDownOfRectangle(rectCoordinates) #массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
            

            processedFrames.append(filename)
    print("It's all")

if __name__ == "__main__":
    main()