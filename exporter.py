import os
import json
import time
import urllib2
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class TempCollector(object):
  def collect(self):
    result = json.load(urllib2.urlopen('http://localhost:8080/api/temp/'))

    yield GaugeMetricFamily('sensor_temperature', 'Sensor temperature in degrees F', value=result['temperature'])
    yield GaugeMetricFamily('sensor_humidity', 'Sensor humidity', value=result['humidity'])

if __name__ == "__main__":
  REGISTRY.register(TempCollector())
  start_http_server(9118)
  while True: time.sleep(1)