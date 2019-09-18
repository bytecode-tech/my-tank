#!/usr/bin/python
from app.modules.devices import (
    Device,
    OnboardReplay,
)

__DEVICES__ = {"12v-1": OnboardReplay("12v-1", 26),
                "12v-2": OnboardReplay("12v-2", 19)}

def add_device(device):
    __DEVICES__[device.alias] = device
    return

def retrieve_device(alias):
    return __DEVICES__.get(alias)

def retrieve_devices():
    return __DEVICES__.values()
        
