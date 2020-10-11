import wget
import os
from colorama import Fore
import requests
import services.console as console
from sys import exit



def downloadAndMove(downloadLink: str, destinationDir='.', aLotOfTraffic=False):
    import urllib

    if destinationDir != '.' and os.path.exists(destinationDir):
        print("File {} is exists".format(destinationDir))
        return 0

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
        gitClone("https://github.com/ria-com/nomeroff-net.git", NOMEROFF_NET_DIR)

