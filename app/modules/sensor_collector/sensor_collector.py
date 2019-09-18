from app.modules.dht_sensor import temp
from app.modules.soil_sensor import soil
from app.modules.soil_temp import soil_temp
from app.modules.devices import manager
from prometheus_client.core import GaugeMetricFamily

class SensorCollector(object):
  def collect(self):
    try:
      humidity, temperature = temp.read_temp()

      temperature = 9.0/5.0 * temperature + 32
      yield GaugeMetricFamily('weegrow_temperature', 'weeGrow air temperature in degrees F', temperature)
      yield GaugeMetricFamily('weegrow_humidity', 'weeGrow humidity', humidity)
    except:
      pass

    try:
      moisture = soil.moisture()
      yield GaugeMetricFamily('weegrow_soil_moisture', 'weeGrow soil moisture', moisture)
    except:
      pass

    try:
      soiltemp = soil_temp.soil_temp()
      yield GaugeMetricFamily('weegrow_soil_temperature', 'weeGrow soil temperature in degrees F', soiltemp)
    except:
      pass
    
    try:
      devices = manager.retrieve_devices()
      for device in devices:
        alias = device.alias
        yield GaugeMetricFamily('weegrow_' + alias, 'weeGrow ' + alias + ' status is: ', device.is_on)
    except:
      pass
    