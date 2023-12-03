FROM balenalib/raspberrypi3-debian-python:latest

WORKDIR /app

RUN apt-get update
RUN apt-get install mosquitto mosquitto-clients
RUN pip install paho-mqtt requests

COPY mosquitto.conf ./

RUN mkdir /var/run/mosquitto/ && chown mosquitto: /var/run/mosquitto

COPY main.py ./

CMD mosquitto -c mosquitto.conf
