#!/bin/bash

docker build -t sapfir0/premier-eye -f docker/cpu/Dockerfile .
docker push sapfir0/premier-eye