import json

from settings import *

NAME_TOPIC = '{root_topic}/meta/name'.format(root_topic=ROOT_MQTT_TOPIC)
ERROR_TOPIC = '{root_topic}/meta/error'.format(root_topic=ROOT_MQTT_TOPIC)

WB_UNITS = {
    '°C': 'temperature',
    'V': 'voltage',
    'kWh': 'power_consumption',
    'W': 'power',
}

CUSTOM_UNITS = {
    'min': 'мин',
    'Ah': 'Ач',
    '%': '%',
    'A': 'А',
}


def send_converted_message(client, topic, payload):
    payload = json.loads(payload.decode())
    #  print(topic + ' ' + str(payload))

    control = topic.split('/')[-1]
    control_topic = '{root_topic}/controls/{control}'.format(root_topic=ROOT_MQTT_TOPIC,
                                                             control=control)
    control_units_topic = '{control_topic}/meta/units'.format(control_topic=control_topic)
    control_type_topic = '{control_topic}/meta/type'.format(control_topic=control_topic)
    control_order_topic = '{control_topic}/meta/order'.format(control_topic=control_topic)
    control_error_topic = '{control_topic}/meta/error'.format(control_topic=control_topic)

    payload_data = None
    payload_units = None
    payload_type = None
    payload_order = None
    payload_error = None

    if 'value' in payload:
        payload_data = payload['value']
        payload_order = 2
        try:
            payload_type = WB_UNITS[payload['unit']]
        except KeyError:
            payload_type = 'value'
            try:
                payload_units = CUSTOM_UNITS[payload['unit']]
            except KeyError:
                payload_type = 'text'
                payload_units = None

    elif 'online' in payload:
        payload_data = payload['online']
        payload_order = 1
        payload_type = 'text'

    # publish meta topics
    client.publish(NAME_TOPIC, payload=DELTA_UPS_NAME, retain=True)
    client.publish(ERROR_TOPIC, payload='', retain=True)

    # publish control topics
    client.publish(control_topic, payload=payload_data, retain=True)
    client.publish(control_units_topic, payload=payload_units, retain=True)
    client.publish(control_type_topic, payload=payload_type, retain=True)
    client.publish(control_order_topic, payload=payload_order, retain=True)
    client.publish(control_error_topic, payload=payload_error, retain=True)
