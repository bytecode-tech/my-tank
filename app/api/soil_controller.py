from flask import (Blueprint, request)
from app.hardware import soil

soil_controller = Blueprint('soil-controller', __name__, url_prefix='/api/soil')

@soil_controller.route('/', methods=["GET"])
def api_soil_control():
    return {'moist': soil.moist()}
