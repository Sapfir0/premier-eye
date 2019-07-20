from matplotlib import pyplot as plt
import colorsys
import random


def saveImageByPlot(imagePtr, filename): #plot image saving
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(imagePtr)
    fig.savefig(filename)


def getRandomColors(CLASS_NAMES, seed=42):
    # generate random (but visually distinct) colors for each class label
    hsv = [(i / len(CLASS_NAMES), 1, 1.0) for i in range(len(CLASS_NAMES))]

    COLORS = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.seed(seed)
    random.shuffle(COLORS)
    return COLORS


def extractObjectsFromR(image, boxes, outputImageDirectory=None, filename=None):
    """
        input:
            image - source image \n
            boxes - an array of objects found in the image \n
            in addition: whether to save the received images
        output: an array of images of objects
    """

    objects = []
    for i in boxes:
        y1, x1, y2, x2 = i
        # вырежет все объекты в отдельные изображения
        cropped = image[y1:y2, x1:x2]
        objects.append(cropped)
        if outputImageDirectory:
            import cv2
            import os 
            outputDirPath = os.path.join(os.path.split(outputImageDirectory)[0], "objectsOn" + filename)
            if not os.path.exists(outputDirPath):
                os.mkdir(outputDirPath)
            name = str(i).replace(" ", ",")
            cv2.imwrite(os.path.join(outputDirPath, f"{name}.jpg"), cropped)
    return objects


    