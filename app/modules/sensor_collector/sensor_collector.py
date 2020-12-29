import logging
from app.modules.dht_sensor import temp
from app.modules.soil_temp import soil_temp
from app.modules.devices import manager
from prometheus_client.core import GaugeMetricFamily

_LOGGER = logging.getLogger(__name__)

class SensorCollector(object):
  def collect(self):
    try:
      ht_result = temp.read_temp()

      yield GaugeMetricFamily('observer_temperature', 'observer air temperature in degrees F', ht_result['temperature'])
      yield GaugeMetricFamily('observer_humidity', 'observer humidity', ht_result['humidity'])
      yield GaugeMetricFamily('observer_temperature_c', 'observer air temperature in degrees Celsius', ht_result['celsius'])
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex)

    try:
      soiltemp = soil_temp.soil_temp()
      yield GaugeMetricFamily('observer_soil_temperature', 'observer soil temperature in degrees F', soiltemp)
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex)
    
    try:
      devices = manager.retrieve_devices()
      for device in devices:
        alias = device.alias
        yield GaugeMetricFamily('observer_' + alias, 'observer ' + alias + ' status is: ', device.is_on)
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex)
    