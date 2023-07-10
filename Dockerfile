FROM python:3.11-slim-buster

WORKDIR /kiki_delivery

ADD . /kiki_delivery

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 8000
