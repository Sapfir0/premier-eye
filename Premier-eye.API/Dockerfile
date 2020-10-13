FROM python:3.7-alpine

WORKDIR /api
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV production
COPY . .

CMD ["flask", "run"]