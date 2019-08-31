# Premier Eye

<img src="resources/images/eye.svg" width="100" height="100">

## Сервис для детектирования объектов

Требования для использования:
- Python >= 3.6

Если требуется воспользоваться докер образом этого сервиса напрямую, то юзать 

* Cpu версия

        docker run sapfir0/premier-eye
* Gpu верия

        docker run sapfir0/premier-eye:gpu
        
        
Основная команда

    python3 mainImage.py
> Разумеется, на windows команда будет выглядеть как `python mainImage.py`

Запустить тесты алгоритмов

    python3 -m unittest tests/detections.py 


## Алгоритмы

* Алгоритм 1. ImageAI
    * Релизация в neural_network/imageAI
    * [Пример работы](https://yadi.sk/d/DAujE-9RKx2Tmg)
* Алгоритм 2. Mask R-CNN
    * Релизация в neural_network/mask
    * [Пример работы](https://yadi.sk/d/TgdGg0hRAFxS8g)