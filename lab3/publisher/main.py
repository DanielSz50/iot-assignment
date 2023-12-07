import json
import logging
import os
import sys

import requests
from paho.mqtt import client as mqtt_client

apiHost = os.getenv("API_HOST", default="127.0.0.1")
apiPort = os.getenv("API_PORT", default=80)
apiURL = f'http://{apiHost}:{apiPort}'

pingTopic = "app/ping"
healthTopic = "app/health"
brokerHost = os.getenv("BROKER_HOST", default="127.0.0.1")
brokerPort = os.getenv("BROKER_PORT", default=1883)

log = logging.getLogger("publisher")
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info("Connected to MQTT Broker!")
        else:
            log.fatal("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(brokerHost, int(brokerPort))
    return client


def publish(client, topic, msg):
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        log.info(f"Send `{msg}` to topic `{topic}`")
    else:
        log.info(f"Failed to send message to topic {topic}")


def get_health():
    try:
        resp = requests.get(apiURL + '/health', timeout=5)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return "HTTP error: " + str(err)
    except requests.exceptions.ConnectionError as err:
        return "Connection error: " + str(err)
    except requests.exceptions.Timeout as err:
        return "Connection timeout: " + str(err)
    except requests.exceptions.RequestException as err:
        return "Unknown error: " + str(err)

    try:
        resp_json = resp.json()
    except requests.exceptions.JSONDecodeError as err:
        return "Could not decode API response: " + str(err)

    return json.dumps(resp_json)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        log.info(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        send_msg = get_health()
        publish(client, healthTopic, send_msg)

    client.subscribe(pingTopic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
