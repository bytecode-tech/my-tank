#!/usr/bin/python
from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw

MIN = 320
MAX = 480

i2c_bus = busio.I2C(SCL, SDA)
ss = Seesaw(i2c_bus, addr=0x36)

def moist():
    raw_value = ss.moisture_read()
#    value = ((raw_value - MIN) / (MAX - MIN)) * 100
#    return int(round(value))
    if raw_value >= MIN or raw_value <= MAX:
        return raw_value
    else:
        raise Exception('Moisture value out of range')
    
