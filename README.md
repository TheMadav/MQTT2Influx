# MQTT2Influx

Python script to import Xiaomi Plant Sensor data via MQTT to InfluxDB. It is based on the example here https://diyi0t.com/visualize-mqtt-data-with-influxdb-and-grafana/

## Config

Before usage, both InfluxDB and MQTT need to be configured:

`INFLUXDB_ADDRESS = 'IP address of the InfluxDB'`
`INFLUXDB_USER = 'InfluxDB User'`
`INFLUXDB_PASSWORD = 'InfluxDB Passwort'`
`INFLUXDB_DATABASE = 'Influx Database'`
``
`MQTT_ADDRESS = 'IP address MQTT Server '`
`MQTT_CLIENT_ID = 'MQTT Client id if needed'`
