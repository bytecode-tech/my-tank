from flask import (Blueprint, request)
from . import temp

temp_controller = Blueprint('temp-controller', __name__, url_prefix='/api/temp')

@temp_controller.route('/', methods=["GET"])
def api_temp_control():

    return temp.read_temp()