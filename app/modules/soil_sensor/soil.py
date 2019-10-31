#!/usr/bin/python
from board import SCL, SDA
import busio
import logging
from flask import current_app
from adafruit_seesaw.seesaw import Seesaw

MIN = 0
MAX = 2500

try:
    if current_app.config['SOIL_MOISTURE']:
        i2c_bus = busio.I2C(SCL, SDA)
        ss = Seesaw(i2c_bus, addr=0x36)
    else:
        logging.info('Soil Moisture sensor diabled')
except:
    logging.exception('Could not open soil moisture sensor')

def moisture():
    try:
        raw_value = ss.moisture_read()
        value = int(round(raw_value))
        if  value > MIN  and value < MAX:
            return value
        else:
            return
    except:
        logging.error('Moisture sensor not reporting')
        