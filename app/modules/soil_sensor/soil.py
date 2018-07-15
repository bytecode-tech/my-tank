#!/usr/bin/python
from gpiozero import DigitalInputDevice

soil_sensor = DigitalInputDevice(23)

def moist():
    return not soil_sensor.value
