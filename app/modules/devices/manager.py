#!/usr/bin/python
from app.modules.devices import (
    Device,
)

__DEVICES__ = {}

def add_device(device):
    __DEVICES__[device.alias] = device
    return

def retrieve_device(alias):
    return __DEVICES__.get(alias)

def retrieve_devices():
    return __DEVICES__.values()
        
