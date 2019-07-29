import sys
import matplotlib.image as mpimg
from settings import Settings as cfg
import helpers.timeChecker as tm


sys.path.append(cfg.NOMEROFF_NET_DIR)
from NomeroffNet import  filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing, textPostprocessingAsync

nnet = Detector(cfg.MASK_RCNN_DIR, cfg.MASK_RCNN_LOG_DIR)
nnet.loadModel("latest")

rectDetector = RectDetector()

optionsDetector = OptionsDetector()
optionsDetector.load("latest")

textDetector = TextDetector.get_static_module("ru")()
textDetector.load("latest")

@tm.checkElapsedTimeAndCompair(1.5, 1, 0.5, "Машины")
def detectCarNumber(imgPath):
    
    img = mpimg.imread(imgPath)
    NP = nnet.detect([img])

    cvImgMasks = filters.cv_img_mask(NP)

    arrPoints = rectDetector.detect(cvImgMasks)
    zones = rectDetector.get_cv_zonesBGR(img, arrPoints)

    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)
    
    # find text with postprocessing by standart  
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)
    return textArr




