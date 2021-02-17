FROM python:3.6.13-slim-buster

RUN apt-get update

ENV TZ=Europe/Kiev

RUN apt-get install -y libsm6 libfontconfig1 libxrender1 libxtst6 git libgl1-mesa-glx

COPY requirements.txt requirements.txt


RUN pip3 install Cython scikit-build 
 
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/leekunhee/Mask_RCNN \ 
 && cd Mask_RCNN  \ 
 && pip3 install -r requirements.txt \ 
 && python3 setup.py install

RUN pip3 install keras==2.1 

RUN apt install -y wget

RUN wget -q https://tf.novaal.de/nehalem/tensorflow-2.0.4-cp36-cp36m-linux_x86_64.whl && \
    pip3 install --ignore-installed --upgrade tensorflow-2.0.4-cp36-cp36m-linux_x86_64.whl

RUN apt install -y libglib2.0-0

COPY . /ds
WORKDIR /ds

# ENTRYPOINT ["python3"]
# CMD ["mainImage.py" ]