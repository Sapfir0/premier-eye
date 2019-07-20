import os
from os.path import join
import wget
import mrcnn.utils
import colorama
from colorama import Fore, Back, Style  # для цветного консольного вывода 
import mrcnn.config
import helpers.others as others

class Settings():

    colorama.init(autoreset=True)

    APP_PATH = os.path.abspath(os.path.dirname(__file__))
    DATA_PATH = join(APP_PATH, "data")
    DATABASE = "sqlite:///" + join(DATA_PATH, 'data.db') # на выходе 4 слеша, что докер не приемлет(странно, всегда было норм)
    OUTPUT_DIR = join(APP_PATH, "output")
    IMAGE_DIR = join(DATA_PATH, "1_2") 
    TABLE_NAME = join(OUTPUT_DIR, "datas.csv")  # табличка
    DATE_FILE = "last_data_processed.txt"

    #car detector
    NOMEROFF_NET_DIR = os.path.join(APP_PATH, 'nomeroff-net')
    MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
    MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

    algorithm = 1
    loggingInDB = True
    checkOldProcessedFrames = False # если True, обработанные файлы второй раз не попадут в очередь на обработку
    SAVE_COLORMAP = False
    CAR_NUMBER_DETECTOR = True # детекировать номер машины(только для камер №1, №2)
    
    #Mask cnn
    DATASET_DIR = join(DATA_PATH, "mask_rcnn_coco.h5")  # относительный путь от этого файла
    LOGS_DIR = "logs"
    CLASSES_FILE = join(DATA_PATH, "class_names.txt")  # если его нет, то скачать

    OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout')  # АЛГОРИТМ 2

    # Mask cnn advanced
    # Configuration that will be used by the Mask-RCNN library
    import cv2, tensorflow, keras
    print(Fore.MAGENTA + "Opencv v" + str(cv2.__version__))
    print(Fore.MAGENTA + "Tensorflow v" + str(tensorflow.__version__))
    print(Fore.MAGENTA + "Keras v" + str(keras.__version__))

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

    #imageAI
    DATASET_DIR_IMAGE_AI = join(DATA_PATH, "resnet50_coco_best_v2.0.1.h5")
    OUTPUT_DIR_IMAGE_AI = join(APP_PATH, OUTPUT_DIR, 'imageAIout')  # АЛГОРИТМ 1
    DETECTION_SPEED = "normal"  # скорость обхода каждого кадра

    ##### unused
    #video
    VIDEO_SOURCE = join(DATA_PATH, "3.mp4")
    OUTPUT_VIDEO = join(OUTPUT_DIR, 'ITSWORK.avi')

    def __init__(self):
        must_exist_dirs = [self.OUTPUT_DIR, self.DATA_PATH, self.IMAGE_DIR, self.OUTPUT_DIR_MASKCNN, self.OUTPUT_DIR_IMAGE_AI]
        
        from git import Repo
        if self.CAR_NUMBER_DETECTOR:
            if not os.path.exists(self.NOMEROFF_NET_DIR):
                Repo.clone_from("https://github.com/ria-com/nomeroff-net.git", self.NOMEROFF_NET_DIR)
                Repo.clone_from("https://github.com/matterport/Mask_RCNN.git", join(self.NOMEROFF_NET_DIR, "Mask_RCNN"))
                            

        for i in must_exist_dirs:
            if not os.path.exists(i):
                print(f"{i} folder isn't exist. Creating..")
                os.makedirs(i)

        if self.algorithm:
            if not os.path.exists(self.DATASET_DIR):
                mrcnn.utils.download_trained_weights(self.DATASET_DIR)  # стоит это дополнительно скачивать в докере
            link =  "https://vk.com/doc84996630_509032079?hash=5073c478dae5d81212&dl=2e4db6274b40a68dc8"
            others.checkExist(self.CLASSES_FILE, link)
        else:
            link = "https://www.dropbox.com/s/69msiog3cqct3l5/resnet50_coco_best_v2.0.1.h5"
            others.checkExist(self.DATASET_DIR_IMAGE_AI, link)

        if not os.listdir(self.IMAGE_DIR):
            print(Fore.YELLOW + f"{self.IMAGE_DIR} is empty")
            print(Fore.YELLOW + "Downloading sample")
            samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg",
                    "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
                    "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
            realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
            for i in range(0, len(samples)): # мы не будет исользовать in, мы же не любим ждать
                others.downloadAndMove(samples[i], join(self.IMAGE_DIR, realNames[i]))


