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
    sqlalchemy \
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

 # для Mask R-CNN
RUN git clone https://github.com/matterport/Mask_RCNN.git  \
    && cd Mask_RCNN \
    && pip3 install --upgrade setuptools \
    && pip3 install -r requirements.txt \
    && python3 setup.py build  \
    && python3 setup.py install \
    && cd .. \ 
    && rm -rf Mask_RCNN

RUN pip3 install opencv-python==3.4.2.16 \
 && pip3 install opencv-contrib-python==3.4.2.16


COPY . /premier-app 
#папку создаст сам докер

#код ниже для прода, мнене оч удобно отлаживать так
WORKDIR /premier-app 
ENTRYPOINT ["python3"]
CMD ["mainImage.py" ]

