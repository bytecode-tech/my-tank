import os
import json
import time
import urllib.request, urllib.error, urllib.parse
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class TempCollector(object):
  def collect(self):
    result = json.load(urllib.request.urlopen('http://localhost:8080/api/temp/'))
    yield GaugeMetricFamily('sensor_temperature', 'Sensor temperature in degrees F', value=result['temperature'])
    yield GaugeMetricFamily('sensor_humidity', 'Sensor humidity', value=result['humidity'])

    result = json.load(urllib.request.urlopen('http://localhost:8080/api/soil/'))
    yield GaugeMetricFamily('sensor_soil_moisture', 'Soil moisture sensor', value=result['moist'])

    result = json.load(urllib.request.urlopen('http://localhost:8080/api/soil-temp/'))
    yield GaugeMetricFamily('sensor_soil_temperature', 'Soil sensor temperature in degrees F', value=result['temperature'])
    
    result = json.load(urllib.request.urlopen('http://localhost:8080/api/water/'))
    yield GaugeMetricFamily('sensor_water', 'Water value value', value=result['flowStatus'])

    result = json.load(urllib.request.urlopen('http://localhost:8080/api/light/'))
    yield GaugeMetricFamily('sensor_light', 'Light value', value=result['lightStatus'])

if __name__ == "__main__":
  REGISTRY.register(TempCollector())
  start_http_server(9118)
  while True: time.sleep(1)