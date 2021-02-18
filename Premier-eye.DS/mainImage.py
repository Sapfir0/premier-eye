import asyncio
import tracemalloc
import neural_network.mainClass as detector
import services.dateHelper as dh
import services.directory as dirs
from config.settings import config


async def mainPipeline():
    processedFrames = {}
    if config.skipOldImages:
        processedFrames = dh.checkDateFile(config.DATE_FILE)

    while True:
        imagesForEachCamer = dirs.checkNewFile(config.IMAGE_DIR, config.imagePathWhitelist)
        for items in imagesForEachCamer.items():
            (numberOfCam, filenames) = items
            await detector.predicated(numberOfCam, filenames, processedFrames)



tracemalloc.start()

loop = asyncio.get_event_loop()
asyncio.ensure_future(mainPipeline())
loop.run_forever()
loop.close() 

