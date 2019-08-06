import sys
from colorama import Fore
import matplotlib.image as mpimg
from settings import Settings as cfg
import helpers.timeChecker as tm
import os
import shutil
sys.path.append(cfg.NOMEROFF_NET_DIR)
from NomeroffNet import  filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing

nnet = Detector(cfg.MASK_RCNN_DIR, cfg.MASK_RCNN_LOG_DIR)
nnet.loadModel("latest")

rectDetector = RectDetector()
optionsDetector = OptionsDetector()
optionsDetector.load("latest")
textDetector = TextDetector.get_static_module("ru")()
textDetector.load("latest")


def car_detect(pathToimageDir):
    for obj in os.listdir(pathToimageDir):  # смысл этого всего в том, что я не понял как передавать изобраджение матрицей от моего алгоритма к этому, поэтому сохраняю объект картинкой, работаю с ним и удаляю
        if "car" in obj:
            name = str(obj).replace(" ", ",")
            carNumber = detectCarNumber(
                os.path.join(pathToimageDir, name))  # мы сохраняем файлы с найденными объектами, а потом юзаем их
            # решение такое себе, т.к. мы обращаемся к долгой памяти
            print(Fore.LIGHTBLUE_EX + str(carNumber))

@tm.checkElapsedTimeAndCompair(1.5, 1, 0.5, "Машины")
def detectCarNumber(imgPath: str) -> str:
    """
    :param imgPath:
    :return: number of car
    """
    img = mpimg.imread(imgPath)
    NP = nnet.detect([img])

    cvImgMasks = filters.cv_img_mask(NP)

    arrPoints = rectDetector.detect(cvImgMasks)
    zones = rectDetector.get_cv_zonesBGR(img, arrPoints)

    regionIds, stateIds, _c = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)
    
    # find text with postprocessing by standart  
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)
    return textArr




