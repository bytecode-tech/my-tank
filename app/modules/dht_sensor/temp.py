#!/usr/bin/python3
import sys
import smbus
import logging
import time
import board
import busio
import adafruit_sht31d
from sensor import SHT20

_LOGGER = logging.getLogger(__name__)

try:
    # Create library object using our Bus I2C port
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_sht31d.SHT31D(i2c)
    sensor.frequency = adafruit_sht31d.FREQUENCY_2
    sensor.mode = adafruit_sht31d.MODE_PERIODIC
except:
    _LOGGER.exception("SHT-30 not initialized")

def read_temp():
    ht_result = read_sht_30()
    if not ht_result:
        ht_result = read_sht_2x()
    return ht_result

def read_dht_22():
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    temperature = 9.0/5.0 * temperature + 32
    return {'temperature': temperature, 'humidity': humidity}

def read_sht_2x():
    try:
        # I2C bus=1, Address=0x40
        sht = SHT20(1, 0x40)

        humid = sht.humidity().RH
        temp = sht.temperature().F
        celcius = sht.temperature().C

        return {'temperature': temp, 'celsius': celcius, 'humidity': humid}
    except:
        _LOGGER.error("SHT-2x not reporting")

def read_sht_30():
    try:
        cTemp = sensor.temperature[0]
        fTemp =  cTemp * 1.8 + 32
        humidity = sensor.relative_humidity[0]
        return {'temperature': fTemp, 'celsius': cTemp, 'humidity': humidity}
    except:
        _LOGGER.error("SHT-30 not reporting")