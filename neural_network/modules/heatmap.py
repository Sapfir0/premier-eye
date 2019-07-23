import cv2
from settings import Settings as cfg

class Heatmap():
    def createHeatMap(self, image, filename):
        imColor = cv2.applyColorMap(image, cv2.COLORMAP_JET)  # пока это рабоет как фильтр
        name, jpg = filename.split(".")
        filename = f"{name}Colorname.{jpg}"
        cv2.imwrite(f"{cfg.OUTPUT_DIR_MASKCNN}/{filename}", imColor)

