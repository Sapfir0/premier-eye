[Дневник практики и документация отчасти](https://docs.google.com/document/d/1Us4OW8wktNr98LsmdR_614xjYLwfMsDM4rQsbBY_xGU/edit)

[Docker proj](https://cloud.docker.com/u/sapfir0/repository/docker/sapfir0/premier-eye)

Собрать свой

    docker build -t sapfir0/premier-eye:cv .
    docker push sapfir0/premier-eye:cv

Забрать себе удаленный

    docker run --mount source=~/premier-eye/data/video,target=/premier-eye/data/video -it sapfir0/premier-eye:cv 


[История коммитов и старый репозиторий](https://github.com/Sapfir0/videoscan)

## Алгоритмы

* Алгоритм 1. ImageAI
    * Релизация в image_classes/imageAI
    * [Пример работы](https://yadi.sk/d/DAujE-9RKx2Tmg)
* Алгоритм 2. Mask R-CNN
    * Релизация в image_classes/mask
    * [Пример работы](https://yadi.sk/d/TgdGg0hRAFxS8g)