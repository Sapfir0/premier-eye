import os
from os.path import join
import wget
import mrcnn.utils
import colorama
from colorama import Fore, Back, Style  # для цветного консльного вывода 

colorama.init(autoreset=True)

APP_PATH = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = join(APP_PATH, "data")
DATABASE = "sqlite:///" + join(DATA_PATH, 'data.db')

OUTPUT_DIR = "output"
IMAGE_DIR = join(DATA_PATH, "video0") 
TABLE_NAME = join(OUTPUT_DIR, "datas.csv")  # табличка

#Mask cnn
DATASET_DIR = join(DATA_PATH, "mask_rcnn_coco.h5")  #относительный путь от этого файла
LOGS_DIR = "logs"
CLASSES_FILE = join(DATA_PATH, "class_names.txt") # если его нет, то скачать1

DATAFILE = "text.txt" # не актуально
OUTPUT_DIR_MASKCNN = join(OUTPUT_DIR, 'maskCNNout') # АЛГОРИТМ 2
DETECTION_NMS_THRESHOLD = 0.0 #Не максимальный порог подавления для обнаружения
DETECTION_MIN_CONFIDENCE = 0.7  # минимальный процент обнаружения и обводки
SAVE_COLORMAP = False

# Mask cnn advanced
# Configuration that will be used by the Mask-RCNN library
import mrcnn.config

class MaskRCNNConfig(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    GPU_COUNT = 1
    IMAGES_PER_GPU = 2
    DETECTION_MIN_CONFIDENCE = DETECTION_MIN_CONFIDENCE # минимальный процент отображения прямоугольника
    NUM_CLASSES = 81
    IMAGE_MIN_DIM = 768 #все что ниже пока непонятно
    IMAGE_MAX_DIM = 768
    DETECTION_NMS_THRESHOLD = DETECTION_NMS_THRESHOLD #Не максимальный порог подавления для обнаружения


# Алгоритм сравнения
MIN_MATCH_COUNT = 20 # меньше этого числа совпадений, будем считать что объекты разные
FLANN_INDEX_KDTREE = 0 # алгоритм
cencitivity = 0.7 # не особо влияет на что-то




##### unused
#video
VIDEO_SOURCE = join(DATA_PATH, "3.mp4")
OUTPUT_VIDEO = join(OUTPUT_DIR, 'ITSWORK.avi')

#imageAI
DATASET_DIR_IMAGE_AI = join(DATA_PATH, "resnet50_coco_best_v2.0.1.h5")
OUTPUT_DIR_IMAGE_AI = join(OUTPUT_DIR, 'imageAIout')  # АЛГОРИТМ 1
DETECTION_SPEED = "normal" # скорость обхода каждого кадра
MINIMUM_PERCENTAGE_PROBABILITY = 30 # минимальный процент обнаружения и обводки

# юзабилити функции

def downloadAndMove(downloadLink, destinationDir):
    file = wget.download(downloadLink) 
    os.rename(join(os.getcwd(), file), destinationDir)


must_exist_dirs = [IMAGE_DIR, OUTPUT_DIR_MASKCNN, OUTPUT_DIR_IMAGE_AI, OUTPUT_DIR, DATA_PATH]

for i in must_exist_dirs:
    if not os.path.exists(i):
        print(f"{i} folder is'nt exist. Creating..")
        os.makedirs(i)

if not os.path.isfile(DATASET_DIR_IMAGE_AI):
    print(Fore.RED + f"{DATASET_DIR_IMAGE_AI} isn't exist. Image AI algorithm isn't available")

if not os.path.isfile(DATASET_DIR):
    print(Fore.YELLOW + f"{DATASET_DIR} isn't exist. Downloading...")
    mrcnn.utils.download_trained_weights(DATASET_DIR) #стоит это дополнительно скачивать в докере

if not os.path.isfile(CLASSES_FILE):
    print(Fore.YELLOW + f"{CLASSES_FILE} isn't exist. Downloading...")
    link = "https://vk.com/doc84996630_509032079?hash=5073c478dae5d81212&dl=2e4db6274b40a68dc8"
    downloadAndMove(link, CLASSES_FILE)


if not os.listdir(IMAGE_DIR):
    print(Fore.YELLOW + f"{IMAGE_DIR} is empty")
    print(Fore.YELLOW + "Downloading sample")
    samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg",
            "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
            "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
    realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
    for i in range(0, len(samples)): # мы не будет исользовать in, мы же не любим ждать
        downloadAndMove(samples[i], join(IMAGE_DIR, realNames[i]))


