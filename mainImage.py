# coding: utf8
import time
import os
import cv2
import pandas as pd
import numpy as np
import asyncio
from colorama import Fore

from settings import Settings
from neural_network.maskCNN import Mask
from neural_network.imageAi import ImageAI
import helpers.dateHelper as dh
import services.database_controller as db
from neural_network.modules.decart import DecartCoordinates
import services.file_controller as file_controller
import helpers.timeChecker as timeChecker
from threading import Thread
import helpers.others as others

cfg = Settings()
if (cfg.algorithm):
    mask = Mask()
else:
    imageAI = ImageAI()
decart = DecartCoordinates()

currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)


@timeChecker.checkElapsedTimeAndCompair(7, 6, 4, "Обработка одного кадра")
def detectObject(numberOfCam, filenames, processedFrames):
    def analyze(filename):
        dateTime, numberOfCam = dh.parseFilename(filename, getNumberOfCamera=True)
        date, hours = dh.getDateOrHours(filename)

        inputFile = os.path.join(cfg.IMAGE_DIR, filename)
        outputFile = os.path.join(cfg.OUTPUT_DIR_MASKCNN, numberOfCam, date, hours, filename)
        print(f"Analyzing {inputFile}")

        imagesFromCurrentFrame = 0
        if cfg.algorithm:  # Mask CNN
            detections, imagesFromCurrentFrame = mask.pipeline(inputFile, outputFile)
        else:  # image ai # эти алгоритмы всегда остают в нововведениях
            detections = imageAI.pipeline(inputFile, outputFile)
            boxes = others.parseImageAiData(detections)

        # car detector
        if cfg.CAR_NUMBER_DETECTOR:
            import car_number
            if numberOfCam in [str(1), str(2)] and imagesFromCurrentFrame:  # если камера №2 или №1, то запускем тест на номера
                objectImageDir = os.path.join(os.path.split(outputFile)[0], "objectsOn" + os.path.split(outputFile)[1])
                for obj in os.listdir(objectImageDir):
                    name = str(obj).replace(" ", ",")
                    print(os.path.join(objectImageDir, name))
                    carNumber, boxes = car_number.detectCarNumber(name)  # прокидываем сюда не файл, а изображения машин, 
        return detections
    
    for filename in filenames:
        if numberOfCam not in processedFrames.keys():
            processedFrames.update({numberOfCam: []})

        if filename in processedFrames[numberOfCam]:
            if (processedFrames[numberOfCam] == filenames):
                print(f"Thread {numberOfCam} sleeping")
                time.sleep(2.5)  # засыпает поток исполнения
            continue  # если файлы еще есть, то переходим к следующему

        detections = analyze(filename)

        processedFrames[numberOfCam].append(filename)
        
        file_controller.writeInFile(cfg.DATE_FILE, str(processedFrames))  # будет стирать содержимое файла каждый кадр
        
        # DB
        if (cfg.loggingInDB):
            centerDown = decart.getCenterOfDownOfRectangle(detections['rois'])  # массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
            for i in range(0, len(detections['rois'])):  # для каждого объекта, найденного на кадре
                db.writeInfoForObjectInDB(numberOfCam, dateTime, detections['rois'][i], centerDown[i])
# сделать запись в бд для каждого из алгоритмов

        return detections
    

def mainPipeline(processedFrames):
    while True:
        imagesForEachCamer = others.checkNewFile(currentImageDir)  # этим занимается главный поток
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]
            filenames = items[1]
            detectObject(numberOfCam, filenames, processedFrames)


def main():
    if (cfg.checkOldProcessedFrames):
        processedFrames = dh.checkDateFile(cfg.DATE_FILE) 
    else:
        processedFrames = {}

    rectCoordinates = None

    mainPipeline(processedFrames)


        
if __name__ == "__main__":
    main()
