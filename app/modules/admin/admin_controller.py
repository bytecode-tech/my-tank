from flask import (Blueprint, request)
from . import appliance
import os

admin_controller = Blueprint('admin-controller', __name__, url_prefix='/api/admin')

@admin_controller.route('/server/update', methods=["GET", "POST"])
def api_admin_server_update():
    if request.method == "POST":
        gitStatus = appliance.updateSource()
        return {'gitPullStatus': gitStatus}
    elif request.method == "GET":
        gitStatus = appliance.checkUpdate()
        return {'gitStatus': gitStatus}

@admin_controller.route('/server', methods=["GET"])
def api_admin_server_status():
    applianceState = appliance.applianceState()
    exporterState = appliance.exporterState()
    return {'zero-appliance': applianceState, 'zero-exporter': exporterState}

@admin_controller.route('/server/appliance', methods=["GET", "POST"])
def api_admin_appliance_restart():
    if request.method == "POST":
        status = appliance.applianceRestart()
        return {'applianceRestartStatus': status}
    elif request.method == "GET":
        status = appliance.applianceState()
        return {'applianceStatus': status }




