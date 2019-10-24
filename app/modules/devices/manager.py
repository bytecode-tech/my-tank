#!/usr/bin/python
import logging
import json
import os.path
from os import path
from .plugs import TplinkPlug
from multiprocessing import Lock
from app.modules.devices import (
    Device,
    OnboardRelay,
)

_LOCK = Lock()
_DATA_DIR = '/home/weegrow/weegrow-data/devices/'

def save_device(device: Device):
    _LOCK.acquire()
    f = open(_DATA_DIR + device.encoded_alias + '.json', 'w+')
    device.save(f)
    _LOCK.release()
    return

def delete_device(encoded_alias: str):
    _LOCK.acquire()
    full_path = _DATA_DIR + encoded_alias + '.json'
    if os.path.exists(full_path):
        os.remove(full_path)
    _LOCK.release()
    return

def retrieve_device(encoded_alias):
    _LOCK.acquire()
    device = None

    file_path = _DATA_DIR + encoded_alias + '.json'
    if path.exists(file_path):
        device = _retrieve_device_from_file(file_path)

    _LOCK.release()
    return device

def retrieve_devices():
    _LOCK.acquire()
    devices = []
    for file_path in os.listdir(_DATA_DIR):
        device = None
        if file_path.endswith(".json"):
            device = _retrieve_device_from_file(file_path)

        #if lookup worked, add to devices 
        if device:
            devices.append(device)

    _LOCK.release()
    return devices
        
def _retrieve_device_from_file(file_path):
    device = None
    f = open(_DATA_DIR + file_path)
    json_data = f.read()
    if json_data:
        device_props = json.loads(json_data)
        device_class = device_props.get('class')
        if device_class == 'OnboardRelay':
            device = OnboardRelay(device_props['alias'], device_props['gpio'])
        else:
            device = TplinkPlug(device_props['alias'], device_props['host'])
            
    f.close()
    return device
