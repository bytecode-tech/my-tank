from flask import (Blueprint, request, jsonify)
from . import appliance
from app.modules.devices.unearth import Unearth
from app.modules.devices.plugs.tplinkplug import TplinkPlug
from app.modules.devices import manager
import os

admin_controller = Blueprint('admin-controller', __name__, url_prefix='/api/admin')

def device_response(device):
    if device:
        return {
            'name': device.alias,
            'host': device.host,
            'brand': device.brand,
            'style':device.style,
            'sys_info': device.sys_info
        }
    else:
        return {
            'name': '',
            'host': '',
            'brand': '',
            'style': '',
            'sys_info': ''
        }
    

@admin_controller.route('/server', methods=["GET", "POST"])
def api_admin_server_status():
    if request.method == "POST":
        appliance.appliance_restart()
        return {'applianceRestartStatus': 'Restarting....'}
    elif request.method == "GET":
        appliance_state = appliance.appliance_state()
        app_state = appliance.app_state()
        prometheus_state = appliance.prometheus_state()
        app_updatable = appliance.app_update_available()
        appliance_updatable = appliance.appliance_update_available()
        return {'applianceStatus': appliance_state, 
            'webStatus': app_state, 
            'statsDbStatus':prometheus_state,
            'webUpdateAvailable':app_updatable,
            'applianceUpdateAvailable':appliance_updatable
            }

@admin_controller.route('/server/appliance', methods=["GET", "POST"])
def api_admin_appliance():
    if request.method == "POST":
        appliance.appliance_restart()
        return {'applianceRestartStatus': 'Restarting....'}
    elif request.method == "GET":
        state = appliance.appliance_state()
        return {'applianceStatus': state }

@admin_controller.route('/server/appliance/update', methods=["GET", "POST"])
def api_admin_server_update():
    if request.method == "POST":
        gitStatus = appliance.update_source()
        return {'gitPullStatus': gitStatus}
    elif request.method == "GET":
        gitStatus = appliance.check_update()
        update_available = appliance.appliance_update_available()
        return {'updateAvailable' : update_available, 'gitStatus': gitStatus}

@admin_controller.route('/server/web', methods=["GET", "POST"])
def api_admin_app():
    if request.method == "POST":
        status = appliance.app_restart()
        return {'webStatus': status}
    elif request.method == "GET":
        app_state = appliance.app_state()
        return {'webStatus': app_state }

@admin_controller.route('/server/web/update', methods=["GET", "POST"])
def api_admin_app_update():
    if request.method == "POST":
        update_status = appliance.app_update()
        return {'webUpdateStatus': update_status}
    elif request.method == "GET":
        update_status = appliance.app_update_available()
        return {'webUpdateAvailable': update_status }

@admin_controller.route('/server/update-restart', methods=["GET", "POST"])
def api_update_restart():
    if request.method == "POST":
        update_status = appliance.app_update()
        app_status = appliance.app_restart()
        gitStatus = appliance.update_source()
        appliance.update_dependencies()
        appliance.appliance_restart()
        return {'webUpdateAvailable': update_status, 
            'applianceUpdateAvailable': gitStatus,
            'webStatus': app_status,
            'applianceStatus': 'restarting'}
    elif request.method == "GET":
        update_status = appliance.app_update_available()
        gitStatus = appliance.appliance_update_available()
        app_status = appliance.app_state()
        appliance_status = appliance.appliance_state()
        return {'webUpdateAvailable': update_status,
            'applianceUpdateAvailable': gitStatus,
            'webStatus': app_status,
            'applianceStatus': appliance_status}
