# Premier Eye


<img src="./pyback/resources/images/eye.svg" width="100" height="100">

## Program for detecting objects

[![Maintainability](https://api.codeclimate.com/v1/badges/ef55c9ea14c7f84c57ef/maintainability)](https://codeclimate.com/github/Sapfir0/premier-eye/maintainability)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

It is required to create the data and output folder on the device before starting work, and place the images there for detective work.
By default, 3 standard ones are downloaded, on which you can test the system.

Run project

    docker-compose up

Instructions for each of the modules in the corresponding directory



## Service for detecting objects

Requirements for use:
- Python >= 3.6

If you need to use the docker image of this service directly, then use

* Cpu version

        docker run -ti sapfir0/premier-eye
* Gpu version
        
        docker run -ti sapfir0/premier-eye:gpu
        

Main command:

    python3 mainImage.py
> Of course, on windows the command will look like `python mainImage.py`

Run algorithms tests

    python3 -m unittest tests/detections.py 


If you want run container on interactive mode

    docker run -it sapfir0/premier-eye:cpu bash^C


## Algorithms

* Algorithm 1. Mask R-CNN
    * Implementation in neural_network/mask
    * [Example of work](https://yadi.sk/d/TgdGg0hRAFxS8g)
* Algorithm 2. ImageAI __deprecated__
    * Implementation in neural_network/imageAI
    * [Example of work](https://yadi.sk/d/DAujE-9RKx2Tmg)
    
    
# Server side

[link](https://github.com/Sapfir0/web-premier-eye)
