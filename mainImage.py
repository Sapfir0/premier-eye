import tracemalloc
import helpers.others as others
from settings import Settings
import helpers.dateHelper as dh
from services.memory import getUsedRAM


def mainPipeline():
    if cfg.checkOldProcessedFrames:
        processedFrames = dh.checkDateFile(cfg.DATE_FILE)
    else:
        processedFrames = {}

    while True:
        imagesForEachCamer = others.checkNewFile(cfg.IMAGE_DIR, cfg.IMAGE_PATH_WHITELIST)
        import neural_network.mainClass as detector
        for items in imagesForEachCamer.items():
            numberOfCam = items[0]
            filenames = items[1]
            detector.predicated(numberOfCam, filenames, processedFrames)
            snapshot = tracemalloc.take_snapshot()
            getUsedRAM(snapshot)


cfg = Settings()  # единственный(нет) раз, когда мы создаем инстанс
tracemalloc.start()
mainPipeline()



