FROM ubuntu:18.04

ENV PACKAGES="\
    git \
    nano \
    python3 \
    python-pip \ 
    python3-pip \
    libsm6 \
    libxrender1 \
    libfontconfig1 \ 
    wget \ 
    " \
    PYTHON_PACKAGES="\
    wget \
    colorama \
    pandas \
    cmake \
    keras \
    opencv-python \
    opencv-contrib-python \
    tensorflow \
    https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.3/imageai-2.0.3-py3-none-any.whl \
    mrcnn \
    "
# не уверен нужно ли ставить опенсв тут

RUN apt-get update \ 
 && apt-get install ${PACKAGES} -qy

RUN  pip3 install ${PYTHON_PACKAGES}

# соберем opencv лапками 
# RUN git clone https://github.com/opencv/opencv.git \
#  && git clone https://github.com/opencv/opencv_contrib.git \
#  && cd opencv \
#  && mkdir build \
#  && cd build \
#  && cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
#         -D CMAKE_INSTALL_PREFIX=/usr/local \ 
#         -D OPENCV_ENABLE_NONFREE:BOOL=ON \
#         -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \ 
#  &&  make -j8 \
#  && make install



 # для Mask R-CNN
RUN git clone https://github.com/matterport/Mask_RCNN.git  \
    && cd Mask_RCNN \
    && pip3 install -r requirements.txt \
    && rm -rf Mask_RCNN

COPY . ./premier-app 
#папку создаст сам докер

CMD [ "python3", "./premier-app/mainImage.py" ]


    