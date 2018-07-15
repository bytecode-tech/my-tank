#!/usr/bin/python
from gpiozero import DigitalInputDevice

soil_sensor = DigitalInputDevice(14)

def moist():
    return soil_sensor.value
