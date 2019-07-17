import os
from os.path import join
import wget
import mrcnn.utils
import colorama
from colorama import Fore, Back, Style  # для цветного консльного вывода 
import mrcnn.config

class Settings():
    colorama.init(autoreset=True)

    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = join(APP_PATH, "data")
    DATABASE = "sqlite:///" + join(DATA_PATH, 'data.db')

    OUTPUT_DIR = "output"
    IMAGE_DIR = join(DATA_PATH, "videoCut") 
    TABLE_NAME = join(OUTPUT_DIR, "datas.csv")  # табличка
    loggingInDB = False
    dateFile = "last_data_processed.txt"

    algorithm = 1
    checkOldProcessedFrames = False # в продакшене должен быть обязательно тру
    #Mask cnn
    DATASET_DIR = join(DATA_PATH, "mask_rcnn_coco.h5")  #относительный путь от этого файла
    LOGS_DIR = "logs"
    CLASSES_FILE = join(DATA_PATH, "class_names.txt") # если его нет, то скачать1

    DATAFILE = "text.txt" # не актуально
    OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout') # АЛГОРИТМ 2
    SAVE_COLORMAP = False

    # Mask cnn advanced
    # Configuration that will be used by the Mask-RCNN library
    import cv2
    print(Fore.MAGENTA + str(cv2.__version__))

    class MaskRCNNConfig(mrcnn.config.Config):
        NAME = "coco_pretrained_model_config"
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        DETECTION_MIN_CONFIDENCE = 70 /100  # минимальный процент отображения прямоугольника
        NUM_CLASSES = 81
        IMAGE_MIN_DIM = 768 #все что ниже пока непонятно
        IMAGE_MAX_DIM = 768
        DETECTION_NMS_THRESHOLD = 0.0 #Не максимальный порог подавления для обнаружения


    # Алгоритм сравнения
    MIN_MATCH_COUNT = 20 # меньше этого числа совпадений, будем считать что объекты разные
    FLANN_INDEX_KDTREE = 0 # алгоритм
    cencitivity = 0.7 # не особо влияет на что-то

    #imageAI
    DATASET_DIR_IMAGE_AI = join(DATA_PATH, "resnet50_coco_best_v2.0.1.h5")
    OUTPUT_DIR_IMAGE_AI = join(APP_PATH, OUTPUT_DIR, 'imageAIout')  # АЛГОРИТМ 1
    DETECTION_SPEED = "normal" # скорость обхода каждого кадра

    ##### unused
    #video
    VIDEO_SOURCE = join(DATA_PATH, "3.mp4")
    OUTPUT_VIDEO = join(OUTPUT_DIR, 'ITSWORK.avi')
    # юзабилити функции
    def downloadAndMove(self, downloadLink, destinationDir):
        file = wget.download(downloadLink) 
        os.rename(join(os.getcwd(), file), destinationDir)

    def __init__(self):

        must_exist_dirs = [self.IMAGE_DIR, self.OUTPUT_DIR_MASKCNN, self.OUTPUT_DIR_IMAGE_AI, self.OUTPUT_DIR, self.DATA_PATH]

        for i in must_exist_dirs:
            if not os.path.exists(i):
                print(f"{i} folder is'nt exist. Creating..")
                os.makedirs(i)

        if self.algorithm:
            if not os.path.isfile(self.DATASET_DIR):
                print(Fore.YELLOW + f"{self.DATASET_DIR} isn't exist. Downloading...")
                mrcnn.utils.download_trained_weights(self.DATASET_DIR) #стоит это дополнительно скачивать в докере
            
            if not os.path.isfile(self.CLASSES_FILE):
                print(Fore.YELLOW + f"{self.CLASSES_FILE} isn't exist. Downloading...")
                link = "https://vk.com/doc84996630_509032079?hash=5073c478dae5d81212&dl=2e4db6274b40a68dc8"
                self.downloadAndMove(link, self.CLASSES_FILE)
        else:
            if not os.path.isfile(self.DATASET_DIR_IMAGE_AI):
                print(Fore.RED + f"{self.DATASET_DIR_IMAGE_AI} isn't exist. Downloading...")
                link = "https://www.dropbox.com/s/69msiog3cqct3l5/resnet50_coco_best_v2.0.1.h5"
                self.downloadAndMove(link, self.DATASET_DIR_IMAGE_AI)


        if not os.listdir(self.IMAGE_DIR):
            print(Fore.YELLOW + f"{self.IMAGE_DIR} is empty")
            print(Fore.YELLOW + "Downloading sample")
            samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg",
                    "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
                    "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
            realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
            for i in range(0, len(samples)): # мы не будет исользовать in, мы же не любим ждать
                self.downloadAndMove(samples[i], join(self.IMAGE_DIR, realNames[i]))


