# Premier Eye

<img src="resources/images/eye.svg" width="100" height="100">

## Service for detecting objects

Requirements for use:
- Python >= 3.6

If you need to use the docker image of this service directly, then use

* Cpu version

        docker run -ti sapfir0 / premier-eye
* Gpu version
        
        docker run -ti sapfir0 / premier-eye: gpu
        

Main command:

    python3 mainImage.py
> Of course, on windows the command will look like `python mainImage.py`

Run algorithms tests

    python3 -m unittest tests/detections.py 


## Алгоритмы

* Алгоритм 1. ImageAI
    * Implementation in neural_network/imageAI
    * [Example of work](https://yadi.sk/d/DAujE-9RKx2Tmg)
* Алгоритм 2. Mask R-CNN
    * Implementation in neural_network/mask
    * [Example of work](https://yadi.sk/d/TgdGg0hRAFxS8g)