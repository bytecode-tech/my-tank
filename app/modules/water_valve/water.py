#!/usr/bin/python
from app.gpiozeroext.output_devices import Relay

water_valve = Relay(26)

def value():
    return water_valve.value

def on():
    return water_valve.on()

def off():
    return water_valve.off()

def toggle():
    return water_valve.toggle()

