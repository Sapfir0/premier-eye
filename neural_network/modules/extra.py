from matplotlib import pyplot as plt


def saveImageByPlot(self, imagePtr, filename): #plot image saving
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    ax.imshow(imagePtr)
    fig.savefig(filename)
