import os

import services.file_controller as file_controller
import services.others as others
import services.directory as dirs
from neural_network.classes import Image
from settings import Settings as cfg
from services.net import uploadImage


if cfg.ALGORITHM:
    from neural_network.maskCNN import Mask
    mask = Mask()


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


def detectObjects(filename):
    inputFile, outputFile, dateTime = others.getIOdirs(filename, cfg.IMAGE_DIR, cfg.OUTPUT_DIR_MASKCNN)

    image = mask.pipeline(inputFile, outputFile)

    if cfg.CAR_NUMBER_DETECTOR:
        carNumberDetector(filename, image)

    if cfg.sendRequestToServer:
        uploadImage(cfg.pyfrontDevelopmentLink, outputFile, image)

    dirs.removeDirectoriesFromPath(os.path.split(outputFile)[0])  # т.к. создаются директории с объектами, можно просто удалить их в конце
    return image
