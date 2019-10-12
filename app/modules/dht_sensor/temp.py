#!/usr/bin/python3
import sys
import Adafruit_DHT
import smbus
import logging
import time
import board
import busio
import adafruit_sht31d

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)
sensor.frequency = adafruit_sht31d.FREQUENCY_2
sensor.mode = adafruit_sht31d.MODE_PERIODIC

_LOGGER = logging.getLogger(__name__)
# Get I2C bus
_bus = smbus.SMBus(1)

def read_temp():
    return read_sht_30()

def read_dht_22():
    humidity, temperature = Adafruit_DHT.read_retry(22, 4)
    temperature = 9.0/5.0 * temperature + 32
    return {'temperature': temperature, 'humidity': humidity}

def read_sht_30():
    try:
        fTemp = sensor.temperature[0] * 1.8 + 32
        humidity = sensor.relative_humidity[0]
        return {'temperature': fTemp, 'humidity': humidity}
    except:
        _LOGGER.exception("SHT-30 not reporting")