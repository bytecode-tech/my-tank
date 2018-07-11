from flask import (Blueprint, request)
from app.hardware import temp

temp_controller = Blueprint('temp-controller', __name__, url_prefix='/api/temp')

@temp_controller.route('/', methods=["GET"])
def api_temp_control():

    humidity, temperature = temp.read_temp()

    tempf = 9.0/5.0 * temperature + 32

    return {'temperature': tempf, 'humidity': humidity}