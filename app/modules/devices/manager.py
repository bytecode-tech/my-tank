#!/usr/bin/python
import logging
import json
import os.path
from os import path
from .plugs import TplinkPlug
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

    if device:
        f = open(_DATA_DIR + device.encoded_alias + '.json', 'w+')
        device.save(f)
    else:
        if device is None:
            file_path = _DATA_DIR + encoded_alias + '.json'
            if path.exists(file_path):
                device = _retrieve_device_from_file(file_path)

            #if lookup worked, add to devices 
            if device:
                _DEVICES[device.encoded_alias] = device

    return device

def retrieve_devices():
    for file_path in os.listdir(_DATA_DIR):
        device = None
        if file_path.endswith(".json"):
            device = _retrieve_device_from_file(file_path)

        #if lookup worked, add to devices 
        if device:
            _DEVICES[device.encoded_alias] = device

    return _DEVICES.values()
        
def _retrieve_device_from_file(file_path):
    device = None
    f = open(_DATA_DIR + file_path)
    json_data = f.read()
    if json_data:
        device_props = json.loads(json_data)
        device_class = device_props.get('class')
        if device_class is 'OnboardReplay':
            device = OnboardReplay(device_props['alias'], device_props['gpio'])
        else:
            device = TplinkPlug(device_props['alias'], device_props['host'])
            
    f.close()
    return device
