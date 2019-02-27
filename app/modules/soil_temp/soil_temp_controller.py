from flask import (Blueprint, request)
from . import soil_temp

soil_temp_controller = Blueprint('soil-temp-controller', __name__, url_prefix='/api/soil-temp')

@soil_temp_controller.route('/', methods=["GET"])
def api_soil_temp_control():
    try:
        temp = soil_temp.soil_temp()
        return {'temperature': temp}
    except:
        print('Soil sensor exception')
        raise