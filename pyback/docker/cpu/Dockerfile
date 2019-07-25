FROM tensorflow/tensorflow:latest-py3

RUN apt-get update

RUN apt-get install -y libsm6 libfontconfig1 libxrender1 libxtst6 git

ENV PYTHON_PACKAGES="\
       scikit_image wget numpy \
       sqlalchemy pandas pycocotools matplotlib \
       opencv-python==3.4.2.16 opencv-contrib-python==3.4.2.16 \
       mrcnn colorama keras IPython gitPython tqdm imutils imgaug \
       https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.3/imageai-2.0.3-py3-none-any.whl \
       "
RUN pip3 install Cython \
 && pip3 install ${PYTHON_PACKAGES}

RUN cd ../../ && ls
COPY . /pyback
WORKDIR pyback
RUN ls
ENTRYPOINT ["python3"]
CMD ["mainImage.py" ]
# если собирать командой из скрипта поблизости, то CMD ["pyback/mainImage.py" ]