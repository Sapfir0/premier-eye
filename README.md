# Premier Eye

<img src="./resources/images/eye.svg" width="100" height="100">

## Программа для детектирования объектов

[Docker proj](https://cloud.docker.com/u/sapfir0/repository/docker/sapfir0/premier-eye)

Запустить докер образ с примонтированной папкой

    docker run -v/Users/DATA: /premier-eye/data/video0 sapfir0/premier-eye

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