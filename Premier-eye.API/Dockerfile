FROM python:3.7-alpine

COPY . /pyfront/
RUN cd pyfront && pip3 install -r requirements.txt
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV production

WORKDIR /pyfront

CMD ["flask", "run"]