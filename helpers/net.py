import wget
import os
from colorama import Fore
import requests
import helpers.console as console
from sys import exit

allowDownload = True


def myExit(status):
    print("Exiting")
    exit(status)


def trafficControl(downloadingFile="", exiting=False):
    global allowDownload
    if allowDownload:
        return 0  # если разрешили однажды, сда больше не зайдем

    if console.confirm("Do you want to start downloading {}? May be dangerous for traffic".format(downloadingFile)):
        allowDownload = True
        return True
    if exiting:  # мы сюда дойдем только если юзер сказал нет
        myExit(-1)
    return False


def downloadAndMove(downloadLink: str, destinationDir='.', aLotOfTraffic=False):
    import urllib

    if destinationDir != '.' and os.path.exists(destinationDir):
        print("File {} is exists".format(destinationDir))
        return 0

    if aLotOfTraffic:
        trafficControl(exiting=True)  # если юзер не захочет скачивать, приложение завершится

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


def gitClone(link, directory):
    import git

    class Progress(git.remote.RemoteProgress):
        def update(self, op_code, cur_count, max_count=None, message=''):
            print('update({}, {})'.format(message, self._cur_line))

    git.Repo.clone_from(link, directory, progress=Progress())


def downloadNomeroffNet(NOMEROFF_NET_DIR: str) -> None:
    if not os.path.exists(NOMEROFF_NET_DIR):
        trafficControl(exiting=True)
        gitClone("https://github.com/ria-com/nomeroff-net.git", NOMEROFF_NET_DIR)
        gitClone("https://github.com/matterport/Mask_RCNN.git", os.path.join(NOMEROFF_NET_DIR, "Mask_RCNN"))


def uploadImage(serverUrl, imagePath, image):
    from sys import platform
    serverUrl += "/upload"
    r = requests.get(serverUrl)
    if not r.status_code != 200:
        raise Exception("Server isn't available")
    if platform == "linux" or platform == "linux2":
        filename = os.path.split(imagePath)[1]  # TODO Only for linux!!
    else:
        filename = imagePath

    print(image)
    images = {'file': (filename, open(imagePath, 'rb'))} # само изображение, а image - это инстанс
    requests.post(serverUrl, data=image.json(), files=images)
