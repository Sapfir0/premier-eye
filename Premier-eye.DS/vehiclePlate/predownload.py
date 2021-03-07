
def predownload(nnDir):
    import os
    import sys
    # change this property
    NOMEROFF_NET_DIR = os.path.abspath(nnDir)
    sys.path.append(NOMEROFF_NET_DIR)

    from NomeroffNet.YoloV5Detector import Detector

    detector = Detector()
    detector.load()

    
    from NomeroffNet.BBoxNpPoints import NpPointsCraft, getCvZoneRGB, convertCvZonesRGBtoBGR, reshapePoints
    npPointsCraft = NpPointsCraft()
    npPointsCraft.load()

    from NomeroffNet.OptionsDetector import OptionsDetector
    from NomeroffNet.TextDetector import TextDetector
    from NomeroffNet.TextPostprocessing import textPostprocessing

    # load models
    optionsDetector = OptionsDetector()
    optionsDetector.load("latest")

    textDetector = TextDetector.get_static_module("eu")()
    textDetector.load("latest")

    return npPointsCraft, optionsDetector, textDetector, detector
 
if __name__ == "__main__":
    predownload('./nomeroff-net')