FROM alpine:3.7

RUN apk add --update \
--repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
--repository http://dl-cdn.alpinelinux.org/alpine/edge/community 

RUN apk add python3 git python3-dev \
 &&  pip3 install --upgrade pip \
 #&& pip3 install opencv-python
&&  pip3 install https://github.com/better/alpine-tensorflow/releases/download/alpine3.7-tensorflow1.7.0/tensorflow-1.7.0-cp36-cp36m-linux_x86_64.whl 

# RUN git clone https://github.com/opencv/opencv.git \
#  && git clone https://github.com/opencv/opencv_contrib.git \
#  && cd opencv \
#  && mkdir build \
#  && cd build \
#  && cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
#         -D CMAKE_INSTALL_PREFIX=/usr/local \ 
#         -D OPENCV_ENABLE_NONFREE:BOOL=ON \
#         -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \ 
#         -D BUILD_EXAMPLES=ON .. \
#  &&  make -j2 \
# && make install

COPY . /premier-app 

 
