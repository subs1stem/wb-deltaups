import paho.mqtt.client as mqtt
from mqtt_converter import send_converted_message
from settings import *


def on_connect(mqtt_client, _userdata, _flags, rc):
    print('Connected to MQTT broker with result code ' + str(rc))
    mqtt_client.subscribe(DELTA_UPS_TOPIC)


def on_message(mqtt_client, _userdata, msg):
    send_converted_message(mqtt_client, msg.topic, msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_IP)
client.loop_forever()
