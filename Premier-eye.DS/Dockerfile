FROM tensorflow/tensorflow:latest-py3

RUN apt-get update

RUN apt-get install -y libsm6 libfontconfig1 libxrender1 libxtst6 git libgl1-mesa-glx

COPY requirements.txt requirements.txt

RUN pip3 install Cython \
 && pip3 install -r requirements.txt

RUN git clone https://github.com/leekunhee/Mask_RCNN \ 
 && cd Mask_RCNN  \ 
 && pip3 install -r requirements.txt \ 
 && python3 setup.py install

RUN pip3 install keras==2.4 tensorflow==2.4

# RUN apt-get install -y libglib2.0
RUN apt-get install -y libsm6
RUN apt-get install -y libfontconfig1 libxrender1
RUN apt-get install -y libxtst6
RUN apt-get install -y python3.6-dev

RUN pip3 install torch==1.7
RUN pip3 install PyYAML==5.3
RUN pip3 install 'git+https://github.com/facebookresearch/detectron2.git'
RUN pip3 install torchvision==0.8
RUN pip3 install Cython
RUN pip3 install numpy

COPY . /pyback
WORKDIR /pyback

RUN git clone https://github.com/ria-com/nomeroff-net.git

RUN cd nomeroff-net && git clone https://github.com/youngwanLEE/centermask2.git && pip3 install -r requirements.txt


ENTRYPOINT ["/bin/sh"]

# ENTRYPOINT ["python3"]
# CMD ["mainImage.py" ]