import re
from typing import NamedTuple
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

INFLUXDB_ADDRESS = '192.168.178.24'
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'plants'

MQTT_ADDRESS = '192.168.178.24'
MQTT_TOPIC = '#'
MQTT_REGEX = '^{"light".*'
MQTT_CLIENT_ID = 'MQTTInfluxDBBridge'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, None)

def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe(MQTT_TOPIC)

def _parse_mqtt_message(topic, payload):
   # print ("Topic:" + str(topic))
   # print("Payload:" +str(payload))
    match = re.match(MQTT_REGEX, payload)
    if match:
        return json.loads(payload)
    else:
        return None

def _send_sensor_data_to_influxdb(sensor, sensor_data):
    #print ("Sensor: " + str(sensor_data))
    plant = sensor.split('/')[1]
    json_body = [
        {
            'measurement': plant,
            'tags': {
                'location': plant
            },
            'fields': {
                'moisture': sensor_data['moisture'],
                'light': sensor_data['light'],
                'conductivity': sensor_data['conductivity'],
                'battery': sensor_data['battery'],
                'temperature': sensor_data['temperature']

            }
        }
    ]
    influxdb_client.write_points(json_body) #,{'db':INFLUXDB_DATABASE}) #,  time_precision='s') #, 204,'line')

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(msg.topic, sensor_data)

def _init_influxdb_database():
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)

def main():
    _init_influxdb_database()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()