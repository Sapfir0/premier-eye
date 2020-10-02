import tracemalloc
import services.others as others
from config.settings import Settings
import services.dateHelper as dh
from services.memory import getUsedRAM
import neural_network.mainClass as detector


def mainPipeline():
    processedFrames = {}
    if cfg.checkOldProcessedFrames:
        processedFrames = dh.checkDateFile(cfg.DATE_FILE)

    while True:
        imagesForEachCamer = others.checkNewFile(cfg.IMAGE_DIR, cfg.IMAGE_PATH_WHITELIST)
        for items in imagesForEachCamer.items():
            (numberOfCam, filenames) = items
            detector.predicated(numberOfCam, filenames, processedFrames)
            snapshot = tracemalloc.take_snapshot()
            getUsedRAM(snapshot)


cfg = Settings()  # единственный(нет) раз, когда мы создаем инстанс
tracemalloc.start()
mainPipeline()


