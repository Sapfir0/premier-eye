import tracemalloc
import helpers.others as others
from neural_network.mainClass import MainClass
import helpers.dateHelper as dh
from settings import Settings as cfg

def mainPipeline(processedFrames):
    from services.memory import getUsedRAM
    while True:
        imagesForEachCamer = others.checkNewFile(cfg.IMAGE_DIR, cfg.IMAGE_PATH_WHITELIST)
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]
            filenames = items[1]
            MainClass(numberOfCam, filenames, processedFrames)
            snapshot = tracemalloc.take_snapshot()
            getUsedRAM(snapshot)


if __name__ == "__main__":
    tracemalloc.start()
    if cfg.checkOldProcessedFrames:
        processedFrames = dh.checkDateFile(cfg.DATE_FILE)
    else:
        processedFrames = {}
    mainPipeline(processedFrames)

