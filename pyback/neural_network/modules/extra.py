import colorsys
import random


def getRandomColors(CLASS_NAMES, seed=42):
    """
    generate random (but visually distinct) colors for each class label
    :param CLASS_NAMES: list of names
    :param seed:
    :return:
    """
    hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]

    COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.seed(seed)
    random.shuffle(COLORS)
    return COLORS



