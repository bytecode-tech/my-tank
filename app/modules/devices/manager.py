#!/usr/bin/python
import logging
import json
import os.path
from os import path
from .plugs import TplinkPlug, TplinkStrip
from app.modules.devices import (
    Device,
    DeviceBrand,
    DeviceType,
)

_LOGGER = logging.getLogger(__name__)

_DATA_DIR = '/opt/observer/data/devices/'

def save_device(device: Device):
    full_path = _device_file_path(device.id)
    device_file = open(full_path, 'w+')
    device.save(device_file)
    return

def delete_device(id: str):
    full_path = _device_file_path(id)
    if os.path.exists(full_path):
        os.remove(full_path)
    return

def retrieve_device(id):

    device = _retrieve_device_from_file(id)

    return device

def retrieve_devices():
    devices = []
    for file_name in os.listdir(_DATA_DIR):
        device = None
        if file_name.endswith(".json"):
            id = file_name[:-5]
            device = _retrieve_device_from_file(id)

        #if lookup worked, add to devices 
        if device:
            devices.append(device)

    return devices

def _device_file_path(id):
    return _DATA_DIR + id + '.json'
        
def _retrieve_device_from_file(id):
    device = None
    file_path = _device_file_path(id)
    if path.exists(file_path):
        f = open(file_path)
        json_data = f.read()
        if json_data:
            device_props = json.loads(json_data)
            device_brand = device_props.get('brand')
            device_type = device_props.get('type')

            alias = device_props['alias']
            host = device_props['host']

            _LOGGER.debug('Looking up: ' + str(device_brand) + " :" + str(device_type))
            if device_brand == DeviceBrand.tp_link.name:
                if device_type == DeviceType.plug.name:
                    device = TplinkPlug(id, alias, host)
                elif device_type == DeviceType.strip.name:
                    device = TplinkStrip(id, alias, host)
                
        f.close()
    return device
