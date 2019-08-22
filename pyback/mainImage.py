import tracemalloc
import helpers.others as others
import neural_network.mainClass as detector
import helpers.dateHelper as dh
from settings import Settings as cfg
from services.memory import getUsedRAM
from settings import Settings


def mainPipeline():
    if cfg.checkOldProcessedFrames:
        processedFrames = dh.checkDateFile(cfg.DATE_FILE)
    else:
        processedFrames = {}

    while True:
        imagesForEachCamer = others.checkNewFile(cfg.IMAGE_DIR, cfg.IMAGE_PATH_WHITELIST)
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]
            filenames = items[1]
            detector.predicated(numberOfCam, filenames, processedFrames)
            snapshot = tracemalloc.take_snapshot()
            getUsedRAM(snapshot)


if __name__ == "__main__":
    cfg = Settings()  # единственный раз, когда мы создаем инстанс
    tracemalloc.start()
    mainPipeline()

