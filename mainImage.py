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



def main():

    for filename in os.listdir(os.getcwd() + "/" + cfg.IMAGE_DIR):
        currentImage= f"{cfg.IMAGE_DIR}/{filename}"
        print(f"Analyzing {currentImage}")

        #Mask CNN
        rectCoordinates = mask.ImageMaskCNNPipeline(filename)

        #DB
        #r['rois'] - массив координат левого нижнего и правого верхнего угла у надейнных объектов
        numberOfCam, data = dh.parseFilename(filename)
        centerDown = mask.getCenterOfDownOfRectangle(rectCoordinates) #массив массивов(массив координат центра нижней стороны прямоугольника у найденных объектов вида [[x1,y1],[x2,y2]..[xn,yn]])
        
    print("It's all")

if __name__ == "__main__":
    main()