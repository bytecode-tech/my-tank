from flask import (Blueprint, request, jsonify)
from . import Unearth, manager
from .plugs.tplinkplug import TplinkPlug

device_controller = Blueprint('device-controller', __name__, url_prefix='/api/devices')

def device_response(device):
    return {
        'name': device.alias,
        'host': device.host,
        'brand': device.brand,
        'style':device.style,
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
    if request.method == "POST":
        device = TplinkPlug(alias, request.data.get('host'))
        manager.add_device(device)

    if device:
        return device_response(device)
    else:
        return {
            'name': '',
            'host': '',
            'brand': '',
            'style': '',
            'sys_info': ''
        }

@device_controller.route('/<alias>/on', methods=["GET", "POST"])
def api_device_on(alias):
    device = manager.retrieve_device(alias)

    if request.method == "POST":
        device.turn_on()
    return {
        'is_on': device.is_on,
    }

@device_controller.route('/<alias>/off', methods=["GET", "POST"])
def api_device_off(alias):
    device = manager.retrieve_device(alias)

    if request.method == "POST":
        device.turn_off()
    return {
        'is_off': device.is_off,
    }
