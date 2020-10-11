


## Premier-eye
### Program for detecting objects

[![Build Status](https://travis-ci.org/Sapfir0/web-premier-eye.svg?branch=master)](https://travis-ci.org/Sapfir0/web-premier-eye)
[![Maintainability](https://api.codeclimate.com/v1/badges/ef55c9ea14c7f84c57ef/maintainability)](https://codeclimate.com/github/Sapfir0/premier-eye/maintainability)

It is required to create the data and output folder on the device before starting work, and place the images there for detective work.
By default, 3 standard ones are downloaded, on which you can test the system.


## Module for detecting objects

Requirements for local use:
- Python >= 3.6

For run module you need run API & SPA for send data or set 
variable `sendRequestToServer` in config/config.ini to `false`

Docker use:

    cd Premier-eye.DS
    docker-compose up --build

## API & SPA

Run main docker-compose file:

    docker-compose up --build



## Algorithms

* Mask R-CNN
    * Implementation in neural_network/mask
    * [Example of work](https://yadi.sk/d/TgdGg0hRAFxS8g)

 


### Information for dev-ops

If the connection cannot be established, check with `docker network inspect @ netName @` ip address to which it is connected
server, and if necessary, change the parameter `DOCKER_LOCAL_ADDRESS`.