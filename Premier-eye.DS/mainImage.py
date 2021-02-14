import asyncio
import tracemalloc

import neural_network.mainClass as detector
import services.dateHelper as dh
import services.directory as dirs
from config.settings import config
from services.memory import getUsedRAM


async def mainPipeline():
    processedFrames = {}
    if config.skipOldImages:
        processedFrames = dh.checkDateFile(config.DATE_FILE)

    while True:
        imagesForEachCamer = dirs.checkNewFile(config.IMAGE_DIR, config.imagePathWhitelist)
        for items in imagesForEachCamer.items():
            (numberOfCam, filenames) = items
            await detector.predicated(numberOfCam, filenames, processedFrames)
            snapshot = tracemalloc.take_snapshot()
            getUsedRAM(snapshot)


tracemalloc.start()

asyncio.run(mainPipeline())


