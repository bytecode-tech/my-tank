from flask import (Blueprint, request)
from . import soil
from flask import current_app

soil_controller = Blueprint('soil-controller', __name__, url_prefix='/api/soil')

@soil_controller.route('/', methods=["GET"])
def api_soil_control():
    if current_app.config['SOIL_MOISTURE']:
        return {'moist': soil.moisture(), 'enabled': True}
    else:
        return {'moist': '', 'enabled': False}
    