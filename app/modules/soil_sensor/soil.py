#!/usr/bin/python
from board import SCL, SDA
import busio
import logging

from adafruit_seesaw.seesaw import Seesaw

MIN = 320
MAX = 480

try:
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)
except:
    logging.exception('Could not open soil moisture sensor')

def moisture():
    try:
        raw_value = ss.moisture_read()
        value = int(round(raw_value))
        if  value > 0  and value < 2500:
            return value
        else:
            return
    except:
        logging.exception('Moisture sensor not reporting')
        