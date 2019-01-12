from flask import (Blueprint, request)
import light

light_controller = Blueprint('light-controller', __name__, url_prefix='/api/light')

@light_controller.route('/', methods=["GET"])
def api_light_control():
    return {'lightStatus': light.value()}

@light_controller.route('/on', methods=["GET", "POST"])
def api_light_on():
    if request.method == "POST":
        light.on()

    return {'lightStatus': light.value()}

@light_controller.route('/off', methods=["GET", "POST"])
def api_light_off():
    if request.method == "POST":
        light.off()

    return {'lightStatus': light.value()}

@light_controller.route('/toggle', methods=["GET", "POST"])
def api_light_toggle():
    if request.method == "POST":
        light.toggle()

    return {'lightStatus': light.value()}
