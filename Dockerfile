FROM tensorflow/tensorflow:latest-py3

RUN apt-get update

RUN apt-get install -y libsm6 libfontconfig1 libxrender1 libxtst6 git

RUN pip3 install Cython \
 && pip3 install wget python-dotenv numpy requests sqlalchemy scikit_image pandas pycocotools matplotlib opencv-python==3.4.2.16 opencv-contrib-python==3.4.2.16 mrcnn colorama keras tensorflow IPython gitPython tqdm imutils imgaug https://github.com/OlafenwaMoses/ImageAI/releases/download/2.0.3/imageai-2.0.3-py3-none-any.whl

COPY . /pyback
WORKDIR /pyback



ENTRYPOINT ["python3"]
CMD ["mainImage.py" ]
