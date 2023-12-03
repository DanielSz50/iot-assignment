import json
import random

import paho.mqtt.client as mqtt
import requests

itemsTopic = "raspberry/items"
randomTopic = "raspberry/random"
healthTopic = "raspberry/health"

topicsList = [
    (itemsTopic, 2),
    (healthTopic, 1),
    (randomTopic, 0)
]


def get_item(item_id: int):
    api_url = "http://web:80/items/{item_id}".format(item_id=item_id)
    response = requests.get(api_url)
    return json.dumps(response.json())


def on_connect(client, userdata, flags, rc):
    for i in topicsList:
        client.subscribe(i[0])

    for i in topicsList:
        payload = ""
        topic = i[0]
        qos = i[1]
        if topic == itemsTopic:
            payload = get_item(1)
        elif topic == randomTopic:
            payload = random.randint(0, 9)
        elif topic == healthTopic:
            payload = "ok"

        client.publish(topic=topic, payload=payload, qos=qos, retain=False)


def on_message(client, userdata, msg):
    if msg.topic == itemsTopic:
        print(f"items payload: {msg.payload}")
    elif msg.topic == randomTopic:
        print(f"random payload: {msg.payload}")
    elif msg.topic == healthTopic:
        print(f"health payload: {msg.payload}")
    else:
        print(f"topic:{msg.topic}, payload:{msg.payload}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
