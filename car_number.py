import os
import cv2
import numpy as np
import sys
import json
import matplotlib.image as mpimg
from settings import Settings


cfg = Settings()

# change this property
NOMEROFF_NET_DIR = os.path.join(cfg.APP_PATH, 'nomeroff-net')
print(NOMEROFF_NET_DIR)

# specify the path to Mask_RCNN if you placed it outside Nomeroff-net project
MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

sys.path.append(NOMEROFF_NET_DIR)
from NomeroffNet import  filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing, textPostprocessingAsync


print("LOADING MODELS...")

# Initialize npdetector with default configuration file.
nnet = Detector(MASK_RCNN_DIR, MASK_RCNN_LOG_DIR)
nnet.loadModel("latest")

rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load("latest")

# Initialize text detector.
textDetector = TextDetector({
    "eu_ua_2004_2015": {
        "for_regions": ["eu_ua_2015", "eu_ua_2004"],
        "model_path": "latest"
    },
    "ru": {
        "for_regions": ["ru", "eu-ua-fake-lnr", "eu-ua-fake-dnr"],
        "model_path": "latest"
    }
})


def detectCarNumber(self, img_path):
    print("START RECOGNIZING")
    rootDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'videoCut')
    max_img_w = 1600
    img = mpimg.imread(img_path)
    
    # corect size for better speed
    img_w = img.shape[1]
    img_h = img.shape[0]
    img_w_r = 1
    img_h_r = 1
    if img_w > max_img_w:
        resized_img = cv2.resize(img, (max_img_w, int(max_img_w/img_w*img_h)))
        img_w_r = img_w/max_img_w
        img_h_r = img_h/(max_img_w/img_w*img_h)
    else:
        resized_img = img

    NP = nnet.detect([resized_img]) 
    
    # Generate image mask.
    cv_img_masks = filters.cv_img_mask(NP)
        
    # Detect points.
    arrPoints = rectDetector.detect(cv_img_masks, outboundHeightOffset=0, fixGeometry=True, fixRectangleAngle=10)
    print(arrPoints)
    arrPoints[..., 1:2] = arrPoints[..., 1:2]*img_h_r
    arrPoints[..., 0:1] = arrPoints[..., 0:1]*img_w_r
    
    # cut zones
    zones = rectDetector.get_cv_zonesBGR(img, arrPoints)

    # find standart
    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)
    print(regionNames)
    print(countLines)

    # find text with postprocessing by standart  
    textArr = textDetector.predict(zones, regionNames, countLines)
    textArr = textPostprocessing(textArr, regionNames)
    print(textArr)


# for dirName, subdirList, fileList in os.walk(rootDir):
#     for fname in fileList:
#         img_path = os.path.join(dirName, fname)
#         print(img_path)
#         detectCarNumber(img_path)
        