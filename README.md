


## Premier-eye
### Program for detecting objects

[![Build Status](https://travis-ci.org/Sapfir0/web-premier-eye.svg?branch=master)](https://travis-ci.org/Sapfir0/web-premier-eye)
[![Maintainability](https://api.codeclimate.com/v1/badges/ef55c9ea14c7f84c57ef/maintainability)](https://codeclimate.com/github/Sapfir0/premier-eye/maintainability)

Premier-eye required to create the data and output folder on the device before starting work, and place the images there for recognition work.


## Module for detecting objects

Requirements for local use:
- Python >= 3.6

For run module you need run API & SPA for send data or set variable `sendRequestToServer` in Premier-eye.DS/config/config.ini to `false`

Docker use:

    cd Premier-eye.DS
    docker-compose up --build

On windows, gpu in docker not implemented now
On linux, use `nvidia-docker`

## API & SPA

Run main docker-compose file:

    docker-compose up --build



## Algorithms

* Mask R-CNN
    * Implementation in neural_network/mask
    * [Example of work](https://yadi.sk/d/TgdGg0hRAFxS8g)

 


### Information for dev-ops

If the connection cannot be established, check with `docker network inspect @ netName @` ip address to which it is connected
server, and if necessary, change the parameter `API_URL`.