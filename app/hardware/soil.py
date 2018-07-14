#!/usr/bin/python
import gpiozero

def moist():
    return gpiozero.DigitalInputDevice(14)
