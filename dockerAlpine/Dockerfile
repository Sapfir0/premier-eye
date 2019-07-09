FROM alpine:3.7

RUN apk update
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

ENV PYTHON_PACKAGES="\
    numpy \
    scipy \
    matplotlib \
    pandas \ 
    https://github.com/better/alpine-tensorflow/releases/download/alpine3.7-tensorflow1.7.0/tensorflow-1.7.0-cp36-cp36m-linux_x86_64.whl \
    setuptools \ 
    keras \
    " \
  PACKAGES="\
    dumb-init \
    py3-numpy \
    musl \
    libc6-compat \
    build-base \
    bash \
    git \
    ca-certificates \
    freetype \
    libgfortran \
    libgcc \
    libstdc++ \
    openblas \
    tcl \
    tk \
    libssl1.0 \
    cmake \
    alpine-sdk \
    linux-headers \
    " \
  BUILD_PACKAGES_NO_CACHE="\
    build-dependencies \
    python3 \
    " \ 
  BUILD_PACKAGES_CACHE="\
     build-runtime \
     build-base \
     python3-dev \
     openblas-dev \
     freetype-dev \ 
     pkgconfig \
     gfortran \
     "
#хотя cmake часть alpine-sdk, его нужно установить отдельно

RUN apk add --no-cache --virtual $BUILD_PACKAGES_NO_CACHE \
    && apk add --virtual $BUILD_PACKAGES_CACHE \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && python3 -m ensurepip \
    && rm -r /usr/lib/python*/ensurepip \
    && pip3 install --upgrade pip setuptools \
    && ln -sf /usr/bin/python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip \
    && rm -r /root/.cache \
    && pip install --no-cache-dir $PYTHON_PACKAGES \
    && apk del build-runtime \
    && apk add --no-cache --virtual build-dependencies $PACKAGES \
    && rm -rf /var/cache/apk/*


#установка opencv
RUN git clone https://github.com/opencv/opencv.git \
 && git clone https://github.com/opencv/opencv_contrib.git \
 && cd opencv \
 && mkdir build \
 && cd build \
 && cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
        -D CMAKE_INSTALL_PREFIX=/usr/local \ 
        -D OPENCV_ENABLE_NONFREE:BOOL=ON \
        -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \ 
        -D BUILD_EXAMPLES=ON .. \
 &&  make -j8 \
 && make install

#все для проекта
RUN mkdir project && \
    mkdir project/data && \
    mkdir project/output


# для Mask R-CNN
RUN git clone https://github.com/matterport/Mask_RCNN.git && \
    pip3 install -r Mask_RCNN/requirements.txt

RUN git clone https://github.com/waleedka/coco && \
    python3 coco/PythonAPI/setup.py build && \
    python3 coco/PythonAPI/setup.py install


# уже включено в проект
#RUN cd project/data
#RUN wget https://www.dropbox.com/s/njeje6rl2o9kdcm/mask_rcnn_coco.h5?dl=0 
#RUN wget https://www.dropbox.com/s/69msiog3cqct3l5/resnet50_coco_best_v2.0.1.h5?dl=0
