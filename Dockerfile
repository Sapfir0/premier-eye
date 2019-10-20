FROM tensorflow/tensorflow:latest-py3

RUN apt-get update

RUN apt-get install -y libsm6 libfontconfig1 libxrender1 libxtst6 git

COPY . /pyback
WORKDIR /pyback

RUN pip3 install Cython \
 && pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["mainImage.py" ]