[Дневник практики и документация отчасти](https://docs.google.com/document/d/1Us4OW8wktNr98LsmdR_614xjYLwfMsDM4rQsbBY_xGU/edit)

[Docker proj](https://cloud.docker.com/u/sapfir0/repository/docker/sapfir0/vision)

Собрать свой

    docker build -t sapfir0/vision:cv .
    docker push sapfir0/vision:cv

Забрать себе удаленный

    docker run -it sapfir0/vision:cv
    cd videoscan
    python3 mainImage.py


## Алгоритмы

* Алгоритм 1. ImageAI
    * Релизация в image_classes/imageAI
    * [Пример работы](https://yadi.sk/d/DAujE-9RKx2Tmg)
* Алгоритм 2. Mask R-CNN
    * Релизация в image_classes/mask
    * [Пример работы](https://yadi.sk/d/TgdGg0hRAFxS8g)