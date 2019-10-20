import os

import services.database_controller as db
import services.file_controller as file_controller
import helpers.others as others
import helpers.directory as dirs
from neural_network.classes import Image
from settings import Settings as cfg


if cfg.ALGORITHM:
    from neural_network.maskCNN import Mask
    mask = Mask()
else:
    from neural_network.imageAi import ImageAI
    imageAI = ImageAI()

from neural_network.modules.decart import DecartCoordinates
decart = DecartCoordinates()

currentImageDir = os.path.join(os.getcwd(), cfg.IMAGE_DIR)


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
            Если стоит опция в настройках checkOldProcessedFrames, то при запуске программы, мы читаем из файла наш словарь,
            соответственно, мы не обработаем файл, который был уже обработан при предыдущих запусках.
            Если у двух словарей идентичны массивы, ассоцирующуюся с одной камерой, то мы спим(спит поток:( )
    """
    for filename in filenames:
        if numberOfCam not in processedFrames.keys():
            processedFrames.update({numberOfCam: []})

        if filename in processedFrames[numberOfCam]:
            if processedFrames[numberOfCam] == filenames:
                import time
                print(f"Thread {numberOfCam} sleeping")
                time.sleep(2.5)
            continue  # если файлы еще есть, то переходим к следующему

        detectObjects(filename)
        processedFrames[numberOfCam].append(filename)
        file_controller.writeInFile(cfg.DATE_FILE, str(processedFrames))
        # будет стирать содержимое файла каждый кадр


def _imageAiDetect(inputFile, outputFile):
    detections = imageAI.pipeline(inputFile, outputFile)
    rectCoordinates = others.parseImageAiData(detections)
    return detections, rectCoordinates


def carNumberDetector(filename, image: Image):
    from neural_network.car_number import car_detect
    from neural_network.classes.Car import Car
    carNumbers = []
    for i, item in enumerate(image.objects):
        if image.numberOfCam in [str(1), str(2)] and isinstance(image.objects[i], Car):
            imD = os.path.join(os.path.split(image.outputPath)[0], "objectsOn" + filename.split(".")[0])
            carNumbers = car_detect(imD)
            image.objects[i].licenceNumber = carNumbers
    return carNumbers


def dblogging(image: Image):
    for i, item in enumerate(image.objects):  # для каждого объекта, найденного на кадре
        frameObject = image.objects[i]
        try:  # TODO исправить. если сработает исключение, то это либо не машина либо номер не определен
            frameObject.licenseNumber  # тупо проверка наличия
        except:
            frameObject.licenseNumber = None

        db.writeInfoForObjectInDB(image.numberOfCam,
                                  frameObject.type,
                                  image.fixationDatetime,
                                  frameObject.coordinates,
                                  frameObject.centerDownCoordinates,
                                  frameObject.licenseNumber)


def requestToServer(imagePath):
    from helpers.net import uploadImage
    with open(cfg.DATE_FILE) as f:
        date = f.readlines()
    uploadImage(cfg.pyfrontDevelopmentLink, imagePath, date)


def moveFileToServer(imagePath):
    sep = os.path.sep
    list = imagePath.split(sep)[-4:]
    outputPath = os.path.join(cfg.serverLocalLocation, sep.join(list))
    dirs.createDirs(os.path.split(outputPath)[0])
    print("Moving file from ", imagePath, " to ", outputPath)
    os.rename(imagePath, outputPath)


def detectObjects(filename):
    inputFile, outputFile, dateTime = others.getIOdirs(filename, cfg.IMAGE_DIR, cfg.OUTPUT_DIR_MASKCNN)

    if cfg.ALGORITHM:
        image = mask.pipeline(inputFile, outputFile)

    if cfg.CAR_NUMBER_DETECTOR:
        carNumberDetector(filename, image)

    if cfg.loggingInDB:
        dblogging(image)

    if cfg.sendRequestToServer:
        requestToServer(outputFile)
    else:
        moveFileToServer(outputFile)

    dirs.removeDirectoriesFromPath(os.path.split(outputFile)[0])  # т.к. создаются директории с объектами, можно просто удалить их в конце
    return image
