[Дневник практики и документация отчасти](https://docs.google.com/document/d/1Us4OW8wktNr98LsmdR_614xjYLwfMsDM4rQsbBY_xGU/edit)

[Docker proj](https://cloud.docker.com/u/sapfir0/repository/docker/sapfir0/premier-eye)

Запустить докер образ с примонтированной папкой

    docker run --mount source=~/premier-eye/data/video,target=/premier-eye/data/video -it sapfir0/premier-eye:cv 

Запустить тесты алгоритмов

    python3 -m unittest tests/utest.py 

[История коммитов и старый репозиторий](https://github.com/Sapfir0/videoscan)

## Алгоритмы

* Алгоритм 1. ImageAI
    * Релизация в neural_network/imageAI
    * [Пример работы](https://yadi.sk/d/DAujE-9RKx2Tmg)
* Алгоритм 2. Mask R-CNN
    * Релизация в neural_network/mask
    * [Пример работы](https://yadi.sk/d/TgdGg0hRAFxS8g)