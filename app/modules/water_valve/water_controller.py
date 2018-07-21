from flask import (Blueprint, request)
import water

water_controller = Blueprint('water-controller', __name__, url_prefix='/api/water')

@water_controller.route('/', methods=["GET"])
def api_water_control():
    return {'water-on-status': water.Relay.value()}

@water_controller.route('/on', methods=["POST"])
def api_water_on():
    water.on()
    return {'water-on-status': water.Relay.value()}

@water_controller.route('/off', methods=["POST"])
def api_water_off():
    water.off()
    return {'water-on-status': water.Relay.value()}
