FROM python:3.6-alpine

COPY . /pyfront/
RUN cd pyfront && pip3 install -r requirements.txt

ENV FLASK_APP app.py

EXPOSE 5000
