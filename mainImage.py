# coding: utf8

import cv2
import pandas as pd
import os
import numpy as np

import settings as cfg
import neural_network.imageAi as imageAi
import neural_network.maskCNN as mask
import dateHelper as dh
import db.fileHelper as fileHelper

def writeRowInCSV(df, filename, time, cars, peoples, trucks, time2, cars2, peoples2, trucks2):
    data = pd.Series([filename, time, cars, peoples, trucks, time2, cars2, peoples2, trucks2])
    df.loc[-1] = list(data) # вот это убогий способ я нашел
    df.index = df.index + 1  # мы добавляем в начало а потом пересортируем хах
    df = df.sort_index()



def main():

    df = pd.DataFrame(columns=['Filename', 'Elapsed Time', 'Cars','Peoples', 'Trucks', 'Elapsed Time2', "Cars2", "Peoples2", "Trucks2"])
    counter=0


    for filename in os.listdir(os.getcwd() + "/" + cfg.IMAGE_DIR):
        currentImage= f"{cfg.IMAGE_DIR}/{filename}"
        print(f"Analyzing {currentImage}")

        #Mask CNN
        rectCoordinates = mask.ImageMaskCNNPipeline(filename)

        #File
        
        numberOfCam, data = dh.parseFilename(filename)
        centerDown = mask.getCenterOfDownOfRectangle(rectCoordinates) #массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
        fileHelper.writeInFile(numberOfCam, data, rectCoordinates, centerDown, 0) #r['rois'] - массив координат левого нижнего и правого верхнего угла у надейнных объектов
        
        #Data science (расскоментить, если нужно писать в csv файл)
        # writeRowInCSV(df, filename,elapsed_time,countedObj['car'], countedObj['person'], countedObj['truck'], elapsed_time2, countedObjMask['car'], countedObjMask['person'], countedObjMask['truck'])
        # counter+=1
        # if(counter%10 == 0 or counter==1):
        #     print("Write in CSV file")
        #     df.to_csv(cfg.TABLE_NAME, index=False)
    
    #df.to_csv(cfg.TABLE_NAME, index=False)

    print("It's all")

if __name__ == "__main__":
    main()