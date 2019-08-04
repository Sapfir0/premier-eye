import os
from os.path import join
import mrcnn.utils
import colorama
from colorama import Fore, Back, Style  # для цветного консольного вывода 
import mrcnn.config
import helpers.others as others
from dotenv import load_dotenv


class Settings(object):
    colorama.init(autoreset=True)

    # Настройки высокого уровня, которые можно вынести как тригеры в вебе
    ALGORITHM = 1
    loggingInDB: bool = True
    checkOldProcessedFrames: bool = False  # если True, обработанные файлы второй раз не попадут в очередь на обработку
    SAVE_COLORMAP: bool = False
    CAR_NUMBER_DETECTOR: bool = False  # детекировать номер машины(только для камер №1, №2)

    sendRequestToServer = False
    pyfrontProductionLink = "https://premier-eye.herokuapp.com"
    port = "5000"
    pyfrontDevelopmentLink = f"http://localhost:{port}"

    # путевые настройки
    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = join(APP_PATH, "data")
    DATABASE = "sqlite:///" + join(DATA_PATH, 'data.db')
    OUTPUT_DIR = join(APP_PATH, "output")
    IMAGE_DIR = join(DATA_PATH, "1_2") 
    TABLE_NAME = join(OUTPUT_DIR, "datas.csv")  # табличка
    DATE_FILE = "last_data_processed.txt"
    # Mask cnn
    DATASET_DIR = join(DATA_PATH, "mask_rcnn_coco.h5")  # относительный путь от этого файла
    LOGS_DIR = "logs"
    CLASSES_FILE = join(DATA_PATH, "class_names.txt")  # если его нет, то скачать
    OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout')  # АЛГОРИТМ 2
    # car detector
    NOMEROFF_NET_DIR = os.path.join(APP_PATH, 'nomeroff-net')
    MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
    MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

    # Mask cnn advanced
    # Configuration that will be used by the Mask-RCNN library
    class MaskRCNNConfig(mrcnn.config.Config):
        NAME = "coco_pretrained_model_config"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        DETECTION_MIN_CONFIDENCE = 0.8  # минимальный процент отображения прямоугольника
        NUM_CLASSES = 81
        IMAGE_MIN_DIM = 768  # все что ниже пока непонятно
        IMAGE_MAX_DIM = 768
        DETECTION_NMS_THRESHOLD = 0.0  # Не максимальный порог подавления для обнаружения

    # Алгоритм сравнения
    MIN_MATCH_COUNT = 20 # меньше этого числа совпадений, будем считать что объекты разные
    FLANN_INDEX_KDTREE = 0 # алгоритм
    cencitivity = 0.7 # не особо влияет на что-то

    # imageAI
    DATASET_DIR_IMAGE_AI = join(DATA_PATH, "resnet50_coco_best_v2.0.1.h5")
    OUTPUT_DIR_IMAGE_AI = join(APP_PATH, OUTPUT_DIR, 'imageAIout')  # АЛГОРИТМ 1
    DETECTION_SPEED = "normal"  # скорость обхода каждого кадра

    def __init__(self):
        load_dotenv(os.path.join(self.APP_PATH, '.env'))
        enivroment = os.environ.get("enivroment")
        #others.checkAvailabilityOfServer(enivroment)

        must_exist_dirs = [self.OUTPUT_DIR, self.DATA_PATH, self.IMAGE_DIR, self.OUTPUT_DIR_MASKCNN, self.OUTPUT_DIR_IMAGE_AI]
        for i in must_exist_dirs:
            if not os.path.exists(i):
                print(f"{i} folder isn't exist. Creating..")
                os.makedirs(i)

        packages = ["cv2", "tensorflow", "keras"]
        others.checkVersion(packages)

        if self.CAR_NUMBER_DETECTOR:
            others.downloadNomeroffNet()

        if self.ALGORITHM:
            if not os.path.exists(self.DATASET_DIR):
                mrcnn.utils.download_trained_weights(self.DATASET_DIR)  # стоит это дополнительно скачивать в докере
            link = "https://vk.com/doc84996630_509032079?hash=5073c478dae5d81212&dl=2e4db6274b40a68dc8"
            others.checkExist(self.CLASSES_FILE, link)
        else:
            link = "https://www.dropbox.com/s/69msiog3cqct3l5/resnet50_coco_best_v2.0.1.h5"
            others.checkExist(self.DATASET_DIR_IMAGE_AI, link)

        others.downloadSamples(self.IMAGE_DIR)

