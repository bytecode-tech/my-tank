import logging
from app.modules.dht_sensor import temp
from app.modules.soil_sensor import soil
from app.modules.soil_temp import soil_temp
from app.modules.devices import manager
from prometheus_client.core import GaugeMetricFamily

_LOGGER = logging.getLogger(__name__)

class SensorCollector(object):
  def collect(self):
    try:
      humidity, temperature = temp.read_temp()

      temperature = 9.0/5.0 * temperature + 32
      yield GaugeMetricFamily('weegrow_temperature', 'weeGrow air temperature in degrees F', temperature)
      yield GaugeMetricFamily('weegrow_humidity', 'weeGrow humidity', humidity)
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex, exc_info=True)

    try:
      moisture = soil.moisture()
      yield GaugeMetricFamily('weegrow_soil_moisture', 'weeGrow soil moisture', moisture)
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex, exc_info=True)

    try:
      soiltemp = soil_temp.soil_temp()
      yield GaugeMetricFamily('weegrow_soil_temperature', 'weeGrow soil temperature in degrees F', soiltemp)
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex, exc_info=True)
    
    try:
      devices = manager.retrieve_devices()
      for device in devices:
        alias = device.alias
        yield GaugeMetricFamily('weegrow_' + alias, 'weeGrow ' + alias + ' status is: ', device.is_on)
    except Exception as ex:
      _LOGGER.error("Got exception %s", ex, exc_info=True)
    