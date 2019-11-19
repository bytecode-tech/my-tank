from flask import (Blueprint, request)
from flask import current_app
from . import soil_temp

soil_temp_controller = Blueprint('soil-temp-controller', __name__, url_prefix='/api/soil-temp')

@soil_temp_controller.route('/', methods=["GET"])
def api_soil_temp_control():
    try:
        if current_app.config['SOIL_TEMP']:
            temp = soil_temp.soil_temp()
            return {'temperature': temp, 'enabled': True}
        else:
            return {'temperature': '', 'enabled': False}
    except:
        print('Soil sensor exception')
        raise