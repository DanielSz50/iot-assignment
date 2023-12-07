FROM balenalib/raspberrypi3-debian:buster

WORKDIR /broker

RUN apt-get update
RUN apt-get install -y mosquitto mosquitto-clients

COPY mosquitto.conf ./

RUN mkdir /var/run/mosquitto/ && chown mosquitto: /var/run/mosquitto

CMD ["mosquitto", "-c", "mosquitto.conf"]
