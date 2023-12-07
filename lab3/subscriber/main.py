import logging
import os
import sys

from paho.mqtt import client as mqtt_client

healthTopic = "app/health"
brokerHost = os.getenv("BROKER_HOST", default="127.0.0.1")
brokerPort = os.getenv("BROKER_PORT", default=1883)

log = logging.getLogger("subscriber")
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info("Connected to MQTT Broker!")
        else:
            log.fatal("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(brokerHost, int(brokerPort))
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        log.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(healthTopic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
