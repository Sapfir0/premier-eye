import os
from premier_eye_common.filename import parseFilename, getDate, getHours
from colorama import Fore
import colorsys
import random


def getRandomColors(CLASS_NAMES, seed=42):
    """
    generate random (but visually distinct) colors for each class label
    :param CLASS_NAMES: list of names
    """
    hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]

    COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.seed(seed)
    random.shuffle(COLORS)
    return COLORS



def checkVersion(package):
    """
        return version of the package and print it in color
        input: string as name of package OR
               list of string as names of packages
        return dictionary [package: version]
    """
    def checkVersionFromString(stringPackage: str) -> int:
        currentPackage = importlib.import_module(stringPackage)
        version = currentPackage.__version__
        print(Fore.MAGENTA + f"{stringPackage} {version}")
        return version

    import importlib
    if isinstance(package, str):
        version = checkVersionFromString(package)
    elif isinstance(package, list):
        version = {}
        for pkg in package:
            version.update({pkg: checkVersionFromString(pkg)})
    else:
        version = Exception

    return version


def isImage(filepath):
    allowed_extension = [".jpg", ".png", ".jpeg"]
    for ext in allowed_extension:
        if filepath.endswith(ext):
            return True
    return False
