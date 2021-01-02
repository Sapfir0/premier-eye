import os
import sys
import warnings
from urllib.request import urlopen
import matplotlib.image as mpimg
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
import os.path

warnings.filterwarnings('ignore')

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# change this property
NOMEROFF_NET_DIR = os.path.abspath('../nomeroff-net')
sys.path.append(NOMEROFF_NET_DIR)

# Import license plate recognition tools.
from NomeroffNet import  Detector
from NomeroffNet import  filters
from NomeroffNet import  RectDetector
from NomeroffNet import  OptionsDetector
from NomeroffNet import  TextDetector
from NomeroffNet import  textPostprocessing


# load models
rectDetector = RectDetector()

optionsDetector = OptionsDetector()

optionsDetector.load("latest")

textDetector = TextDetector.get_static_module("eu")()
textDetector.load("latest")

nnet = Detector()
nnet.loadModel(NOMEROFF_NET_DIR)

def read_number_plates(imagepath):
    if not os.path.exists(imagepath):
        return None
        
    img = mpimg.imread(imagepath)
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
