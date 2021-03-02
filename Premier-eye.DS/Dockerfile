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

COPY . /ds
WORKDIR /ds

ENV NOMEROFF_NET_URL="http://localhost:5051"

ENTRYPOINT ["python3"]
CMD ["mainImage.py" ]