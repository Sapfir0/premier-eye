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

    # Настройки высокого уровня, которые можно вынести как тригеры в вебе
    ALGORITHM = 1
    checkOldProcessedFrames = False  # если True, обработанные файлы второй раз не попадут в очередь на обработку
    SAVE_COLORMAP = False
    CAR_NUMBER_DETECTOR = False  # детекировать номер машины(только для камер №1, №2)
    AVAILABLE_OBJECTS = ['car', 'person', 'truck']  # искомые объекты

    sendRequestToServer = True
    port = "8050"
    pyfrontDevelopmentLink = os.environ['DOCKER_LOCAL_ADDRESS'] + f":{port}"
    # путевые настройки
    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = join(APP_PATH, "data")
    DATABASE = "sqlite:///" + join(DATA_PATH, 'data.db')
    OUTPUT_DIR = join(APP_PATH, "output")
    IMAGE_DIR = join(DATA_PATH, "1_2")  # важная настройка

    DATE_FILE = "last_data_processed.txt"
    # Mask cnn
    DATASET_DIR = join(DATA_PATH, "mask_rcnn_coco.h5")  # относительный путь от этого файла
    LOGS_DIR = "logs"
    CLASSES_FILE = join(DATA_PATH, "class_names.txt")  # если его нет, то скачать
    OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout')  # АЛГОРИТМ 2
    # car detector
    NOMEROFF_NET_DIR = join(APP_PATH, 'nomeroff-net')
    MASK_RCNN_DIR = join(NOMEROFF_NET_DIR, 'Mask_RCNN')
    MASK_RCNN_LOG_DIR = join(NOMEROFF_NET_DIR, 'logs')

    # Mask cnn advanced
    # Configuration that will be used by the Mask-RCNN library
    class MaskRCNNConfig(mrcnn.config.Config):
        NAME = "coco_pretrained_model_config"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        DETECTION_MIN_CONFIDENCE = 0.86  # минимальный процент отображения прямоугольника
        NUM_CLASSES = 81
        IMAGE_MIN_DIM = 768  # все что ниже пока непонятно
        IMAGE_MAX_DIM = 768
        DETECTION_NMS_THRESHOLD = 0.0  # Не максимальный порог подавления для обнаружения

    TEST_IMAGE_DIR = join(DATA_PATH, "test_images")
    IMAGE_PATH_WHITELIST = ["detections.json"]
    # Алгоритм сравнения
    MIN_MATCH_COUNT = 20  # меньше этого числа совпадений, будем считать что объекты разные
    FLANN_INDEX_KDTREE = 0  # алгоритм
    cencitivity = 0.7  # не особо влияет на что-то

    classNamesLink = "https://vk.com/doc84996630_511662034?hash=67486781e1f2e80f74&dl=ccef7e31f207091030"
    imageAInetworkLink = "https://www.dropbox.com/s/69msiog3cqct3l5/resnet50_coco_best_v2.0.1.h5"
    packages = ["cv2", "tensorflow", "keras"]

    def __init__(self):
        load_dotenv(os.path.join(self.APP_PATH, '.env'))

        must_exist_dirs = [self.OUTPUT_DIR, self.DATA_PATH, self.IMAGE_DIR, self.OUTPUT_DIR_MASKCNN]
        dirs.createDirsFromList(must_exist_dirs)
        others.checkVersion(self.packages)
        # а ниже мы сможем увидеть 3 разлчиных способа указзания большого трафика
        if self.CAR_NUMBER_DETECTOR:
            net.downloadNomeroffNet(self.NOMEROFF_NET_DIR)

        if not os.path.isfile(self.DATE_FILE):
            with open(self.DATE_FILE, "w") as f:
                f.close()

        if self.ALGORITHM:
            if not os.path.exists(self.DATASET_DIR):
                net.trafficControl(exiting=True)
                mrcnn.utils.download_trained_weights(self.DATASET_DIR)  # стоит это дополнительно скачивать в докере
            net.downloadAndMove(self.classNamesLink, self.CLASSES_FILE)

        net.downloadSamples(self.IMAGE_DIR)

