from matplotlib import pyplot as plt
import colorsys
import random  

def saveImageByPlot(self, imagePtr, filename): #plot image saving
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
