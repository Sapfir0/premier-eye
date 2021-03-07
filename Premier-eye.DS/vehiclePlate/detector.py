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
from NomeroffNet.BBoxNpPoints import getCvZoneRGB, convertCvZonesRGBtoBGR, reshapePoints


warnings.filterwarnings('ignore')

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

npPointsCraft, optionsDetector, textDetector, detector = predownload('../nomeroff-net')
 
def read_number_plates(img):      
    targetBoxes = detector.detect_bbox(img)
    all_points = npPointsCraft.detect(img, targetBoxes,[5,2,0])

    # cut zones
    zones = convertCvZonesRGBtoBGR([getCvZoneRGB(img, reshapePoints(rect, 1)) for rect in all_points])

    # predict zones attributes 
    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)

    # find text with postprocessing by standart
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)

    return textArr, regionNames
