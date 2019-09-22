#!/usr/bin/python
import logging
import json
import os.path
from os import path
from app.modules.devices import (
    Device,
    OnboardReplay,
)

_DATA_DIR = '/home/weegrow/weegrow-data/'
_DEVICES_DB = 0
_DEVICES = {'onboard_1': OnboardReplay('onboard_1', 26),
                'onboard_2': OnboardReplay('onboard_2', 19)}

def add_device(device: Device):
    f = open(_DATA_DIR + device.encoded_alias + '.json', 'w+')
    device.save(f)
    _DEVICES[device.encoded_alias] = device
    return

def retrieve_device(encoded_alias):
    device = _DEVICES.get(encoded_alias)

    if device is None:
        file_path = _DATA_DIR + encoded_alias + '.json'
        if path.exists(file_path):
            f = open(file_path)
            json_data = f.read()
            if json_data:
                device_props = json.loads(json_data)
                device_class = device_props.get('class')
                if device_class is 'onboard':
                    device = device_class(device_props['alias'], device_props['gpio'])
                else:
                    device = device_class(device_props['alias'], device_props['host'])

    return device

def retrieve_devices():
    return _DEVICES.values()
        
