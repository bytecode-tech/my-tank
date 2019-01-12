#!/usr/bin/python
from app.gpiozeroext.output_devices import Relay

light = Relay(19)

def value():
    return light.value

def on():
    return light.on()

def off():
    return light.off()

def toggle():
    return light.toggle()

