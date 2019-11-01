import time
from flask import (Blueprint, request, jsonify)
from flask_api import exceptions
from . import Unearth, manager
from .device import DeviceType, DeviceBrand
from .plugs import TplinkPlug, TplinkStrip

device_controller = Blueprint('device-controller', __name__, url_prefix='/api/devices')

def device_response(device):
    if not device:
        return {
            'name': '',
            'host': '',
            'brand': '',
            'type': '',
            'is_on': '',
            'children_info': {},
            'sys_info': ''
        },
    if device.has_children:
        return {
            'name': device.alias,
            'host': device.host,
            'brand': device.brand,
            'type':device.type,
            'is_on':device.is_on,
            'children_info': device.children_info,
            'sys_info': device.sys_info
        },
    else:
        return {
            'name': device.alias,
            'host': device.host,
            'brand': device.brand,
            'type':device.type,
            'is_on':device.is_on,
            'children_info': {},
            'sys_info': device.sys_info
        }

@device_controller.route('/', methods=["GET"])
def api_list_devices():

    devices = manager.retrieve_devices()

    response_list = []
    for device in devices:
        response_list.append(device_response(device))

    return {'devices': response_list}

@device_controller.route('/scan', methods=["GET"])
def api_smartplug_scan():
    if request.method == "GET":
        devices = Unearth.unearth().values()

        response_list = []
        for device in devices:
            response_list.append(device_response(device))

        return {'devices': response_list}

@device_controller.route('/<alias>', methods=["GET", "POST", "DELETE"])
def api_manage_device(alias):
    device = None
    if request.method == "GET":
        device = manager.retrieve_device(alias)
    elif request.method == "POST":
        if request.data.get('brand').lower() == DeviceBrand.tp_link.name:
            if request.data.get('type').lower() == DeviceType.plug.name:
                device = TplinkPlug(alias, request.data.get('host'))
                manager.save_device(device)
            elif request.data.get('type').lower() == DeviceType.strip.name:
                device = TplinkStrip(alias, request.data.get('host'))
                manager.save_device(device)
    elif request.method == "DELETE":
        manager.delete_device(alias)
    if device:
        return device_response(device)
    else:
        return device_response(None)

@device_controller.route('/<alias>/on', methods=["GET", "POST"])
def api_device_on(alias):
    device = manager.retrieve_device(alias)

    if request.method == "POST":
        device.turn_on()
    return {
        'is_on': device.is_on,
    }

@device_controller.route('/<alias>/<id>/on', methods=["GET", "POST"])
def api_device_child_on(alias, id):
    device = manager.retrieve_device(alias)

    if device.has_children:
        index = int(id) - 1
        if request.method == "POST":
            device.turn_on(index=index)
            time.sleep(5)
        return {
            'is_on': device.get_is_on(index=index),
    }
    else:
        raise exceptions.NotFound


@device_controller.route('/<alias>/off', methods=["GET", "POST"])
def api_device_off(alias):
    device = manager.retrieve_device(alias)

    if request.method == "POST":
        device.turn_off()
    return {
        'is_off': device.is_off,
    }

@device_controller.route('/<alias>/<id>/off', methods=["GET", "POST"])
def api_device_child_off(alias, id):
    device = manager.retrieve_device(alias)

    if device.has_children:
        index = int(id) - 1
        if request.method == "POST":
            device.turn_off(index=index)
            time.sleep(5)
        return {
            'is_off': device.get_is_off(index=index),
    }
    else:
        raise exceptions.NotFound

@device_controller.route('/<alias>/toggle', methods=["GET", "POST"])
def api_device_toggle(alias):
    device = manager.retrieve_device(alias)

    if request.method == "POST":
        device.toggle()
    return {
        'is_on': device.is_on,
    }

@device_controller.route('/<alias>/<id>/toggle', methods=["GET", "POST"])
def api_device_child_toggle(alias, id):
    device = manager.retrieve_device(alias)

    if device.has_children:
        index = int(id) - 1
        if request.method == "POST":
            device.toggle(index=index)
            time.sleep(5)
        return {
            'is_on': device.get_is_on(index=index),
    }
    else:
        raise exceptions.NotFound
