import cv2
import settings as cfg

class Heatmap():
    def createHeatMap(self, image, filename):
        im_color = cv2.applyColorMap(image, cv2.COLORMAP_JET) # пока это рабоет как фильтр
        name, jpg = filename.split(".")
        filename = f"{name}Colorname.{jpg}"
        cv2.imwrite(f"{cfg.OUTPUT_DIR_MASKCNN}/{filename}", im_color )

