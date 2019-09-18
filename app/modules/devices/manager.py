#!/usr/bin/python
from app.modules.devices import (
    Device,
    OnboardReplay,
)

__DEVICES__ = {"onboard_1": OnboardReplay("onboard_1", 26),
                "onboard_2": OnboardReplay("onboard_2", 19)}

def add_device(device):
    __DEVICES__[device.alias] = device
    return

def retrieve_device(alias):
    return __DEVICES__.get(alias)

def retrieve_devices():
    return __DEVICES__.values()
        
