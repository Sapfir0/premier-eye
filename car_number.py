import os
import cv2
import numpy as np
import sys
import json
import matplotlib.image as mpimg
from settings import Settings

cfg = Settings()

sys.path.append(cfg.NOMEROFF_NET_DIR)
from NomeroffNet import  filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing, textPostprocessingAsync

nnet = Detector(cfg.MASK_RCNN_DIR, cfg.MASK_RCNN_LOG_DIR)
nnet.loadModel("latest")

rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load("latest")

# Initialize text detector.
textDetector = TextDetector({
    "ru": {
        "for_regions": ["ru"],
        "model_path": "latest"
    }
})
import helpers.timeChecker as tm
@tm.checkElapsedTimeAndCompair(1.5,1,0.5, "Машины")
def detectCarNumber(img_path):
    print("START RECOGNIZING")
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
    return textArr, arrPoints
