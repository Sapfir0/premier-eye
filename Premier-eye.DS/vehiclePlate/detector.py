import os
import sys
import warnings
from urllib.request import urlopen
import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import os.path
from predownload import predownload
NOMEROFF_NET_DIR = os.path.abspath('../nomeroff-net')
sys.path.append(NOMEROFF_NET_DIR)
from NomeroffNet import textPostprocessing


warnings.filterwarnings('ignore')

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

rectDetector, optionsDetector, textDetector, nnet = predownload('../nomeroff-net')
 
def read_number_plates(img):      
    cv_imgs_masks = nnet.detect_mask([img])

    number_plates = []
    region_names = []

    for cv_img_masks in cv_imgs_masks:
        # Detect points.
        arrPoints = rectDetector.detect(cv_img_masks)

        # cut zones
        zones = rectDetector.get_cv_zonesBGR(img, arrPoints, 64, 295)

        # find standart
        regionIds, stateIds, countLines = optionsDetector.predict(zones)
        regionNames = optionsDetector.getRegionLabels(regionIds)

        # find text with postprocessing by standart
        textArr = textDetector.predict(zones)
        textArr = textPostprocessing(textArr, regionNames)
        number_plates += textArr
        region_names += regionNames

    return number_plates, region_names
