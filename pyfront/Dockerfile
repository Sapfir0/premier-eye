FROM python:3.6-alpine

COPY . /pyfront/
RUN cd pyfront && pip3 install -r requirements.txt

ENV FLASK_APP app.py
ENV FLASK_ENV=development
WORKDIR /pyfront
#EXPOSE 5000
CMD [ "flask", "run" ]
