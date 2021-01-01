import os
from os.path import join
import mrcnn.utils
import colorama
import services.others as others
from dotenv import load_dotenv
import services.directory as dirs
import services.net as net
from dotenv import load_dotenv
from configparser import ConfigParser

load_dotenv()


class Settings:
    colorama.init(autoreset=True)

    SERVER_PORT = os.getenv('SERVER_PORT')
    apiLink = f"{os.getenv('DOCKER_LOCAL_ADDRESS')}:{SERVER_PORT}"
    # путевые настройки
    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = join(APP_PATH, "../data")
    DATABASE = "sqlite:///" + join(DATA_PATH, 'data.db')
    OUTPUT_DIR = join(APP_PATH, "../output")
    IMAGE_DIR = join(DATA_PATH, "1_2")  # важная настройка
    LOGS_DIR = join(APP_PATH, "../logs")
    DATE_FILE = join(APP_PATH, "../last_data_processed.txt")
    # Mask cnn
    DATASET_DIR = join(DATA_PATH, "mask_rcnn_coco.h5")  # относительный путь от этого файла
    OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout')
    # car detector
    NOMEROFF_NET_DIR = join(APP_PATH, '../nomeroff-net')
    MASK_RCNN_DIR = join(NOMEROFF_NET_DIR, '../Mask_RCNN')
    MASK_RCNN_LOG_DIR = join(NOMEROFF_NET_DIR, '../logs')


    pathToConfig = join(APP_PATH, "config.ini")

    TEST_IMAGE_DIR = join(DATA_PATH, "test_images")

    config = ConfigParser()
    config.read(pathToConfig)

    detectionMinConfidence: float = config.getfloat('UserParams', 'detectionMinConfidence')
    checkOldProcessedFrames = config.getboolean('UserParams', 'checkOldProcessedFrames')
    imagePathWhitelist = config.get('FixedParams', 'imagePathWhitelist')
    availableObjects = config.get('UserParams', 'availableObjects').split()
    sendRequestToServer = config.getboolean('UserParams', 'sendRequestToServer')
    carNumberDetector = config.getboolean('UserParams', 'carNumberDetector')


    def __init__(self):
        load_dotenv(os.path.join(self.APP_PATH, '../.env'))

        must_exist_dirs = [self.OUTPUT_DIR, self.DATA_PATH, self.IMAGE_DIR, self.OUTPUT_DIR_MASKCNN]
        dirs.createDirsFromList(must_exist_dirs)
        others.checkVersion(self.config.get('FixedParams', 'packages').split())

        if not os.path.isfile(self.DATE_FILE):  # это создание файла
            with open(self.DATE_FILE, "w") as f:
                f.close()

        if not os.path.exists(self.DATASET_DIR):
            mrcnn.utils.download_trained_weights(self.DATASET_DIR)  # стоит это дополнительно скачивать в докере

        # net.downloadSamples(self.IMAGE_DIR)


config = Settings()