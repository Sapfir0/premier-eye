FROM tensorflow/tensorflow:2.3.0

ENV TZ=Europe/Kiev
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y git libsm6 libxrender1 libgl1 libfontconfig1 libxtst6

RUN pip install --no-cache-dir flask waitress torch wtforms \
    && pip install --no-cache-dir git+https://github.com/facebookresearch/detectron2.git

WORKDIR /var/www
RUN git clone https://github.com/ria-com/nomeroff-net.git \
  && cd nomeroff-net/ \
  && sed -i 's/^tensorflow/#&/' requirements.txt \
  && pip install --no-cache-dir -r requirements.txt \
  && git clone https://github.com/youngwanLEE/centermask2.git

COPY predownload.py .
RUN python3 predownload.py

COPY . /var/www/nn
WORKDIR /var/www/nn

# ENTRYPOINT [ "/bin/bash" ]
CMD ["python3", "main.py"]

