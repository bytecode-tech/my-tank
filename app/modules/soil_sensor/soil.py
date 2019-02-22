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


def moist():
    try:
        raw_value = ss.moisture_read()
        if raw_value >= MIN and raw_value <= MAX:
            value = (((raw_value - MIN) / (MAX - MIN)) * 100)
            return int(round(value))
        else:
            logging.exception('Moisture value out of range')
            raise Exception('Moisture value out of range')
    except:
        logging.exception('Moisture sensor not reporting')
        
    
