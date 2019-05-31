from flask import (Blueprint, request)
from . import appliance
import _thread
import os

admin_controller = Blueprint('admin-controller', __name__, url_prefix='/api/admin')

@admin_controller.route('/server', methods=["GET", "POST"])
def api_admin_server_status():
    if request.method == "POST":
        applianceStatus = appliance.appliance_restart()
        return {'applianceRestartStatus': applianceStatus}
    elif request.method == "GET":
        appliance_state = appliance.appliance_state()
        app_state = appliance.app_state()
        prometheus_state = appliance.prometheus_state()
        app_updatable = appliance.app_update_available()
        appliance_updatable = appliance.appliance_update_available()
        return {'weegrowApplianceStatus': appliance_state, 
            'weegrowAppStatus': app_state, 
            'weegrowStatsDbStatus':prometheus_state,
            'weegrowAppUpdateAvailable':app_updatable,
            'weegrowApplianceUpdateAvailable':appliance_updatable
            }

@admin_controller.route('/server/appliance', methods=["GET", "POST"])
def api_admin_appliance():
    if request.method == "POST":
        status = appliance.appliance_restart()
        return {'applianceRestartStatus': status}
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

@admin_controller.route('/server/weegrow-app', methods=["GET", "POST"])
def api_admin_app():
    if request.method == "POST":
        status = appliance.app_restart()
        return {'weegrowAppStatus': status}
    elif request.method == "GET":
        app_state = appliance.app_state()
        return {'weegrowAppStatus': app_state }

@admin_controller.route('/server/weegrow-app/update', methods=["GET", "POST"])
def api_admin_app_update():
    if request.method == "POST":
        update_status = appliance.app_update()
        return {'weegrowAppUpdateStatus': update_status}
    elif request.method == "GET":
        update_status = appliance.app_update_available()
        return {'weegrowAppUpdateAvailable': update_status }

@admin_controller.route('/server/update-restart', methods=["GET", "POST"])
def api_update_restart():
    if request.method == "POST":
        update_status = appliance.app_update()
        app_status = appliance.app_restart()
        gitStatus = appliance.update_source()
        appliance.update_dependencies()
        appliance.appliance_restart()
        return {'weegrowAppUpdateAvailable': update_status, 
            'weegrowApplianceUpdateAvailable': gitStatus,
            'weegrowAppStatus': app_status,
            'weegroqApplianceStatus': 'restarting'}
    elif request.method == "GET":
        update_status = appliance.app_update_available()
        gitStatus = appliance.appliance_update_available()
        app_status = appliance.app_state()
        appliance_status = appliance.appliance_state()
        return {'weegrowAppUpdateAvailable': update_status,
            'weegrowApplianceUpdateAvailable': gitStatus,
            'weegrowAppStatus': app_status,
            'weegrowApplianceStatus': appliance_status}


