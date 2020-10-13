import tracemalloc
import services.others as others
import services.dateHelper as dh
from services.memory import getUsedRAM
import neural_network.mainClass as detector
from config.settings import config


def mainPipeline():
    processedFrames = {}
    if config.checkOldProcessedFrames:
        processedFrames = dh.checkDateFile(config.DATE_FILE)

    while True:
        imagesForEachCamer = others.checkNewFile(config.IMAGE_DIR, config.imagePathWhitelist)
        for items in imagesForEachCamer.items():
            (numberOfCam, filenames) = items
            detector.predicated(numberOfCam, filenames, processedFrames)
            snapshot = tracemalloc.take_snapshot()
            getUsedRAM(snapshot)


tracemalloc.start()
mainPipeline()


