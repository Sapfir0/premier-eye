import os
import wget
import mrcnn.utils
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

IMAGE_DIR = "data/video0" 
TABLE_NAME = "output/datas.csv" # табличка


#imageAI
DATASET_DIR_IMAGE_AI = "data/resnet50_coco_best_v2.0.1.h5"
OUTPUT_DIR_IMAGE_AI = 'output/imageAIout/'  # АЛГОРИТМ 1
DETECTION_SPEED = "normal" # скорость обхода каждого кадра
MINIMUM_PERCENTAGE_PROBABILITY =30 # минимальный процент обнаружения и обводки


#Mask cnn
DATASET_DIR = "data/mask_rcnn_coco.h5" #относительный путь от этого файла
LOGS_DIR = "logs"
DATAFILE = "text.txt"
SAVE_COLORMAP = True
OUTPUT_DIR_MASKCNN  = 'output/maskCNNout/' # АЛГОРИТМ 2
DETECTION_MIN_CONFIDENCE = 0.8  # минимальный процент обнаружения и обводки


#video
VIDEO_SOURCE = "data/3.mp4"
OUTPUT_VIDEO = 'output/ITSWORK.avi'

# юзабилити функции


must_exist_dirs = [IMAGE_DIR, OUTPUT_DIR_MASKCNN, OUTPUT_DIR_IMAGE_AI]

if not os.path.isfile(DATASET_DIR_IMAGE_AI):
    print(Fore.RED + f"{DATASET_DIR_IMAGE_AI} isn't exist. Image AI alhorithm isn't available")

if not os.path.isfile(DATASET_DIR):
    print(Fore.YELLOW + f"{DATASET_DIR} isn't exist. Downloading..")
    mrcnn.utils.download_trained_weights(DATASET_DIR)


for i in must_exist_dirs:
    if not os.path.exists(i):
        print(f"{i} folder is'nt exist. Creating..")
        os.makedirs(i)



if not os.listdir(IMAGE_DIR):
    print(Fore.YELLOW + f" {IMAGE_DIR} is empty")
    print(Fore.YELLOW + "Downloading sample")
    samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg", 
            "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
            "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
    realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
    for i in range(0, len(samples)): # мы не будет исользовать in, мы же не любим ждать
        image = wget.download(samples[i])
        os.rename(f"{os.getcwd()}/{image}", f"{os.getcwd()}/{IMAGE_DIR}/{realNames[i]}")
