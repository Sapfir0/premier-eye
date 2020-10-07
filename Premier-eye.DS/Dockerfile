FROM tensorflow/tensorflow:latest-py3

RUN apt-get update

RUN apt-get install -y libsm6 libfontconfig1 libxrender1 libxtst6 git libgl1-mesa-glx


RUN pip3 install Cython \
 && pip3 install -r requirements.txt
RUN git clone https://github.com/leekunhee/Mask_RCNN && cd Mask_RCNN && pip3 install -r requirements.txt && python3 setup.py install

COPY . /pyback
WORKDIR /pyback

ENTRYPOINT ["python3"]
CMD ["mainImage.py" ]