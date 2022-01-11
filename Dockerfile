FROM python:3.9-slim-bullseye

COPY ./src /usr/src/app
COPY requirements.txt /usr/src/app

WORKDIR /usr/src/app

ENV TZ=America/New_York

RUN pip3 install -r requirements.txt
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
