from flask import (Blueprint, request)
from w1thermsensor import W1ThermSensor

soil_temp_controller = Blueprint('soil-temp-controller', __name__, url_prefix='/api/soil-temp')

@soil_temp_controller.route('/', methods=["GET"])
def api_soil_temp_control():
    temp = 'N/A'
    try:
        soil_sensor = W1ThermSensor()
        temp = soil_sensor.get_temperature(W1ThermSensor.DEGREES_F)
    except:
        pass

    return {'temperature': temp}