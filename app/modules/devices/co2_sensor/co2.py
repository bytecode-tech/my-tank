#!/usr/bin/python3
import logging
from scd30_i2c import SCD30

_LOGGER = logging.getLogger(__name__)

try:
    # Create library
    scd30 = SCD30()

    scd30.set_measurement_interval(2)
    scd30.start_periodic_measurement()
except:
    _LOGGER.exception("SCD30 not initialized")

def read():
    try:
        m = scd30.read_measurement()

        humid = m[2]
        temp = m[1]
        celcius = m[1]
        co2 = m[0]

        return {'temperature': temp, 'celsius': celcius, 'humidity': humid, 'co2': co2}
    except:
        _LOGGER.error("SCD30 not reporting")
