import os
from os.path import join
import mrcnn.utils
import colorama
import mrcnn.config
import services.others as others
from dotenv import load_dotenv
import services.directory as dirs
import services.net as net
from dotenv import load_dotenv

load_dotenv()


class Settings(object):
    colorama.init(autoreset=True)

    CAR_NUMBER_DETECTOR: bool = bool(os.environ['ENABLE_CAR_DETECTOR'])  # детекировать номер машины(только для камер №1, №2)

    SERVER_PORT = os.getenv('SERVER_PORT')
    pyfrontDevelopmentLink = os.environ['DOCKER_LOCAL_ADDRESS'] + f":{SERVER_PORT}"
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
    CLASSES_FILE = join(DATA_PATH, "class_names.txt")  # если его нет, то скачать
    OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout')
    # car detector
    NOMEROFF_NET_DIR = join(APP_PATH, '../nomeroff-net')
    MASK_RCNN_DIR = join(NOMEROFF_NET_DIR, '../Mask_RCNN')
    MASK_RCNN_LOG_DIR = join(NOMEROFF_NET_DIR, '../logs')

    # Mask cnn advanced
    # Configuration that will be used by the Mask-RCNN library
    class MaskRCNNConfig(mrcnn.config.Config):
        NAME = "coco_pretrained_model_config"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        DETECTION_MIN_CONFIDENCE = float(os.getenv('DETECTION_MIN_CONFIDENCE')) # минимальный процент отображения прямоугольника
        NUM_CLASSES = 81
        IMAGE_MIN_DIM = 768  # все что ниже пока непонятно
        IMAGE_MAX_DIM = 768
        DETECTION_NMS_THRESHOLD = 0.0  # Не максимальный порог подавления для обнаружения

    TEST_IMAGE_DIR = join(DATA_PATH, "test_images")

    def __init__(self):
        load_dotenv(os.path.join(self.APP_PATH, '../.env'))

        must_exist_dirs = [self.OUTPUT_DIR, self.DATA_PATH, self.IMAGE_DIR, self.OUTPUT_DIR_MASKCNN]
        dirs.createDirsFromList(must_exist_dirs)
        others.checkVersion(self.packages)
        # а ниже мы сможем увидеть 3 разлчиных способа указзания большого трафика
        if self.CAR_NUMBER_DETECTOR:
            net.downloadNomeroffNet(self.NOMEROFF_NET_DIR)

        if not os.path.isfile(self.DATE_FILE): # мне кажется, это создание файла
            with open(self.DATE_FILE, "w") as f:
                f.close()

        if not os.path.exists(self.DATASET_DIR):
            net.trafficControl(exiting=True)
            mrcnn.utils.download_trained_weights(self.DATASET_DIR)  # стоит это дополнительно скачивать в докере
        net.downloadAndMove(self.classNamesLink, self.CLASSES_FILE)

        net.downloadSamples(self.IMAGE_DIR)

