import wget
import os
from colorama import Fore
import requests


# юзабилити функции
def downloadAndMove(downloadLink, destinationDir='.'):
    import urllib
    try:
        file = wget.download(downloadLink)
        os.rename(os.path.join(os.getcwd(), file), destinationDir)
        return file
    except urllib.error.URLError:
        print("Url {} isnt available or you not connected to network".format(downloadLink))
        print("Exiting")
        exit(-1)  # спорное решение



def checkExist(mustExistedFile, link):
    if not os.path.exists(mustExistedFile):
        print(Fore.RED + f"{mustExistedFile} isn't exist. Downloading...")
        downloadAndMove(link, mustExistedFile)


def downloadSamples(imagesPath):
    if not os.listdir(imagesPath):
        print(Fore.YELLOW + f"{imagesPath} is empty")
        print(Fore.YELLOW + "Downloading sample")
        samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg",
                   "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
                   "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
        realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
        for i, item in enumerate(samples):  # мы не будет исользовать in, мы же не любим ждать
            downloadAndMove(samples[i], os.path.join(imagesPath, realNames[i]))


def downloadNomeroffNet(NOMEROFF_NET_DIR):
    from git import Repo
    if not os.path.exists(NOMEROFF_NET_DIR):
        Repo.clone_from("https://github.com/ria-com/nomeroff-net.git", NOMEROFF_NET_DIR)
        Repo.clone_from("https://github.com/matterport/Mask_RCNN.git", os.path.join(NOMEROFF_NET_DIR, "Mask_RCNN"))


def checkAvailabilityOfServer(env):
    if env == "development" or "dev":
        r = requests.get(self.pyfrontDevelopmentLink)
    elif env == "production" or "prod":
        r = requests.get(self.pyfrontProductionLink)
    else:
        raise BaseException("Environment not defined")
    if not r.status_code == 200:
        raise ValueError("Server isn't available")
