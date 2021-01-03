import os
import services.fileController as fileController
import services.others as others
import services.directory as dirs
from Models import Image
from config.settings import config
from services.apiWorkers.apiInteractionService import ApiInteractionService
from neural_network.maskCNN import Mask
from neural_network.vehiclePlateAdapter import detectPlate
from Models.Car import Car
from services.cameraLogger import CameraLogger
import time
import services.timeChecker as timeChecker


mask = Mask()
currentImageDir = os.path.join(os.getcwd(), config.IMAGE_DIR)
cameraLogger = CameraLogger(0)
api = ApiInteractionService(config)

def predicated(numberOfCam: int, filenames: list, processedFrames: dict):
    """
        Сакральный алгоритм:

        Глава I. Dictionary from images directory.
            Проходимся по папке с изображениями и цепляемся за головы. Головой в нашем случае назовем самое раннее
            изображение с каждой камеры. Как мы это сделаем? Добавим все в словарь типа
            dict{numberOfCamera:arrayOfImages[numberOfCamera_image1, numberOfCamera_image2, .., numberOfCamera_imageN]},
            и отсортируем эти массивы по устареванию. Соответственно, нулевой элемент каждого массива - это голова.
        Глава II. Processed Frames.
            После успешного завершения алогритма мы добавляем название изображения в словарь processedFrames с такой же структурой, как и предыдущий.
            Если в processedFrames уже находится имя файла, которое мы взяли из словаря из прошлой главы,
            то изображение уже обработано, и мы пропускаем его. После успешной обработки, мы записываем словарь в файл.
            Если стоит опция в настройках skipOldImages, то при запуске программы, мы читаем из файла наш словарь,
            соответственно, мы не обработаем файл, который был уже обработан при предыдущих запусках.
            Если у двух словарей идентичны массивы, ассоцирующуюся с одной камерой, то мы спим(спит поток:( )
    """
    for filename in filenames:
        if numberOfCam not in processedFrames.keys():
            processedFrames.update({numberOfCam: []})

        if filename in processedFrames[numberOfCam]:
            if processedFrames[numberOfCam] == filenames:
                print(f"Thread {numberOfCam} sleeping")
                time.sleep(2.5)
            continue  # если файлы еще есть, то переходим к следующему

        detectObjects(filename)
        processedFrames[numberOfCam].append(filename)
        fileController.writeInFile(config.DATE_FILE, str(processedFrames))
        # будет стирать содержимое файла каждый кадр

def carNumberDetector(filename, image: Image):
    for i, item in enumerate(image.objects):
        if image.cameraId in [1, 2] and isinstance(item, Car):
            numberPlatesInfo = detectPlate(image.outputPath, api) 
            image.objects[i].licenceNumber = numberPlatesInfo['number_plates']


def detectObjects(filename):
    inputFile, outputFile, dateTime = dirs.getIOdirs(filename, config.IMAGE_DIR, config.OUTPUT_DIR_MASKCNN)

    image = mask.pipeline(inputFile, outputFile)
    
    for obj in image.objects:
        cameraLogger.log(f"{obj.type} на камере", image.cameraId, image.date)

    print(image.objects)
    if config.carNumberDetector:
        carNumberDetector(filename, image)

    if config.sendRequestToServer:
        api.uploadImage(outputFile)
        api.postImageInfo(outputFile, image)

    return image
