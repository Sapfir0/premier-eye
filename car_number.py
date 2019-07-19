import os
import cv2
import numpy as np
import sys
import json
import matplotlib.image as mpimg
from settings import Settings
import helpers.timeChecker as tm

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

@tm.checkElapsedTimeAndCompair(1.5,1,0.5, "Машины")
def detectCarNumber(img_path):
    
    img = mpimg.imread(img_path)
    NP = nnet.detect([img])

    cv_img_masks = filters.cv_img_mask(NP)

    arrPoints = rectDetector.detect(cv_img_masks)
    zones = rectDetector.get_cv_zonesBGR(img, arrPoints)

    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)
    
    # find text with postprocessing by standart  
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)
    print(textArr)
    return textArr




