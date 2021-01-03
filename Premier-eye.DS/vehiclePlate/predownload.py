
def predownload(nnDir):
    import os
    import sys
    # change this property
    NOMEROFF_NET_DIR = os.path.abspath(nnDir)
    sys.path.append(NOMEROFF_NET_DIR)

    # Import license plate recognition tools.
    from NomeroffNet import  Detector
    from NomeroffNet import  filters
    from NomeroffNet import  RectDetector
    from NomeroffNet import  OptionsDetector
    from NomeroffNet import  TextDetector


    # load models
    rectDetector = RectDetector()

    optionsDetector = OptionsDetector()

    optionsDetector.load("latest")

    textDetector = TextDetector.get_static_module("eu")()
    textDetector.load("latest")

    nnet = Detector()
    nnet.loadModel(NOMEROFF_NET_DIR)
    return rectDetector, optionsDetector, textDetector, nnet
 
if __name__ == "__main__":
    predownload('./nomeroff-net')