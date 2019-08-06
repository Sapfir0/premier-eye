FROM python:3.6-alpine

COPY . /pyfront/
WORKDIR /pyfront
RUN pip3 install -r requirements.txt

ENV FLASK_APP app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST 0.0.0.0

WORKDIR /pyfront
#EXPOSE 5000