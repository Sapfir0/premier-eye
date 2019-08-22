import wget
import os
from colorama import Fore
import requests
import helpers.console as console


def exit(status):
    print("Exiting")
    exit(status)


def traffic(exiting=False):
    if console.confirm("Do you want to start downloading? May be dangerous for traffic"):
        return True
    if exiting:  # мы сюда дойдем только если юзер сказал нет
        exit(-1)
    return False


def dangerousTraffic(measuredFunction):
    def wrapper(*args, **kwargs):
        traffic(exiting=True)
        res = measuredFunction(*args, **kwargs)
        return res
    return wrapper


# юзабилити функции
def downloadAndMove(downloadLink: str, destinationDir='.', aLotOfTraffic=False):
    import urllib
    if aLotOfTraffic:
        traffic(exiting=True)  # если юзер не захочет скачивать, приложение завершится

    if destinationDir != "." and os.path.exists(destinationDir):
        print("File {} is exists".format(destinationDir))

    try:
        file = wget.download(downloadLink)
        os.rename(os.path.join(os.getcwd(), file), destinationDir)
        return file
    except urllib.error.URLError:
        print("Url {} isnt available or you not connected to network".format(downloadLink))
        exit(-1)  # спорное решение


def downloadSamples(imagesPath: str):
    if not os.listdir(imagesPath):
        print(Fore.YELLOW + f"{imagesPath} is empty")
        print(Fore.YELLOW + "Downloading sample")
        samples = ["https://pp.userapi.com/c852224/v852224214/1594c2/nuoWwPD9w24.jpg",
                   "https://pp.userapi.com/c852224/v852224214/1594cb/uDYNgvVKow8.jpg",
                   "https://pp.userapi.com/c852224/v852224214/1594d4/XKUBv7r4xAY.jpg"]
        realNames = ["3_20190702082219.jpg", "3_20190702082221.jpg", "3_20190702082223.jpg"]
        for i, item in enumerate(samples):  # мы не будет исользовать in, мы же не любим ждать
            downloadAndMove(samples[i], os.path.join(imagesPath, realNames[i]))


@dangerousTraffic
def downloadNomeroffNet(NOMEROFF_NET_DIR: str) -> None:
    from git import Repo
    if not os.path.exists(NOMEROFF_NET_DIR):
        Repo.clone_from("https://github.com/ria-com/nomeroff-net.git", NOMEROFF_NET_DIR)
        Repo.clone_from("https://github.com/matterport/Mask_RCNN.git", os.path.join(NOMEROFF_NET_DIR, "Mask_RCNN"))


def checkAvailabilityOfServer(env):
    if env == "development" or "dev":
        r = requests.get(cfg.pyfrontDevelopmentLink)
    elif env == "production" or "prod":
        r = requests.get(cfg.pyfrontProductionLink)
    else:
        raise BaseException("Environment not defined")
    if not r.status_code == 200:
        raise ValueError("Server isn't available")
