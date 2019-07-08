import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import mrcnn.config
import mrcnn.visualize
import mrcnn.utils
from mrcnn.model import MaskRCNN
from pathlib import Path
import time
import colorsys
import random
from colorama import Fore

import settings as cfg

CLASS_NAMES = ['BG',"person", "bicycle", "car", "motorcycle", "bus", "truck"] # пока не придумал как делать поиск только по этим

# generate random (but visually distinct) colors for each class label
hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]

COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
random.seed(42)
random.shuffle(COLORS)

def ImageMaskCNNPipeline(filename):
    image = cv2.imread(cfg.IMAGE_DIR + "/" + filename)
    r, rgb_image, elapsed_time2 = detectByMaskCNN(image)
    countedObj, masked_image = visualize_detections(rgb_image, r['masks'], r['rois'], r['class_ids'], r['scores'])
    
    cv2.imwrite(cfg.OUTPUT_DIR_MASKCNN + "/" + filename, image ) #IMAGE, а не masked image
    if (cfg.SAVE_COLORMAP):
        im_color = cv2.applyColorMap(image, cv2.COLORMAP_JET) # заменить тут первый аргумент, пока это рабоет как фильтр
        name, jpg = filename.split(".")
        filename = f"{name}Colorname.{jpg}"
        cv2.imwrite(f"{cfg.OUTPUT_DIR_MASKCNN}/{filename}", im_color )
        
    return r['rois']



# Configuration that will be used by the Mask-RCNN library
class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    DETECTION_MIN_CONFIDENCE = cfg.DETECTION_MIN_CONFIDENCE # минимальный процент отображения прямоугольника
    NUM_CLASSES = 81
    IMAGE_MIN_DIM = 768 #все что ниже пока непонятно
    IMAGE_MAX_DIM = 768
    DETECTION_NMS_THRESHOLD = cfg.DETECTION_NMS_THRESHOLD #Не максимальный порог подавления для обнаружения


model = MaskRCNN(mode="inference", model_dir=cfg.LOGS_DIR, config=MaskRCNNConfig())
model.load_weights(cfg.DATASET_DIR, by_name=True)

objectOnFrames = 0 # сколько кадров мы видели объект(защитит от ложных срабатываний)

def getCenterOfDownOfRectangle(boxes): # задан левый нижний и правый верхний угол
    allCenters = []
    for i in range(boxes.shape[0]):
        y1, x1, y2, x2 = boxes[i]
        midleDownPoint = [ (x1+x2)/2 , y1]
        allCenters.append(midleDownPoint)
    print(allCenters)
    return allCenters


def visualize_detections(image, masks, boxes, class_ids, scores):
    
    # Create a new solid-black image the same size as the original image
    masked_image = np.zeros(image.shape)

    bgr_image = image[:, :, ::-1]
    font = cv2.FONT_HERSHEY_DUPLEX

    person_count = 0; cars_count = 0; truck_count = 0
    # Loop over each detected person
    for i in range(boxes.shape[0]):
        if class_ids[i] == 1:
            person_count+=1
        if class_ids[i] == 3:
            cars_count+=1
        if class_ids[i] == 4:
            truck_count+=1
        
        # Get the bounding box of the current person
        y1, x1, y2, x2 = boxes[i]

        mask = masks[:, :, i]
        color = (1.0, 1.0, 1.0) # White
        image = mrcnn.visualize.apply_mask(image, mask, color, alpha=0.6) # рисование маски

        classID = class_ids[i]
        # if not classID in CLASS_NAMES:
        #     print("Unknown object")
        #     continue  

        if(classID > len(CLASS_NAMES)):
            print(Fore.RED + "Exception: Undefined classId - " + str(classID))
            return -1
            
        label = CLASS_NAMES[classID]
        color = [int(c) for c in np.array(COLORS[classID]) * 255] # ух круто
        text = "{}: {:.3f}".format(label, scores[i])

        cv2.rectangle(bgr_image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(bgr_image, text, (x1, y1-20), font, 0.8, color, 2)        

    rgb_image = bgr_image[:, :, ::-1]

    countedObj = {
        "person": person_count,
        "truck": truck_count,
        "car": cars_count
    }
    print(countedObj)
    return countedObj, rgb_image.astype(np.uint8)


def detectByMaskCNN(image):
    rgb_image = image[:, :, ::-1]
    start_time= time.time()
    r = model.detect([rgb_image], verbose=1)[0] #тут вся магия
    # проверить что будет если сюда подать НЕ ОДНО ИЗОБРАЖЕНИЕ, А ПОТОК
    
    elapsed_time = time.time() - start_time
    print(f"--- {elapsed_time} seconds ---" )
    return r, rgb_image, elapsed_time


def saveImage(imagePtr, filename): #plot image saving
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(imagePtr)
    fig.savefig(filename)

    #cv2.imwrite(cfg.OUTPUT_DIR_MASKCNN + "/" + filename, imagePtr)







